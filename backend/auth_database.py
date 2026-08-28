"""Persistencia ligera para usuarios y sesiones de Cerebro Digital."""
import json
import os
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, JSON, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql+psycopg2://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg2://" + url[len("postgresql://"):]
    return url


DATABASE_URL = os.getenv("DATABASE_URL")
_engine = None
_database_error = None

if DATABASE_URL:
    try:
        _engine = create_engine(
            normalize_database_url(DATABASE_URL),
            pool_pre_ping=True,
            pool_recycle=300,
        )
    except Exception as error:
        _database_error = str(error)
        print(f"⚠️ No se pudo configurar PostgreSQL: {_database_error}")


class Base(DeclarativeBase):
    pass


class UserRecord(Base):
    __tablename__ = "cerebro_users"

    username: Mapped[str] = mapped_column(String(80), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class UserSessionRecord(Base):
    __tablename__ = "cerebro_user_sessions"

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)


def initialize_database() -> None:
    global _engine
    if _engine is not None:
        try:
            Base.metadata.create_all(_engine)
        except Exception as error:
            global _database_error
            _database_error = str(error)
            _engine = None
            print(f"⚠️ No se pudo conectar con PostgreSQL: {_database_error}")


def database_status() -> dict:
    if not DATABASE_URL:
        return {"configured": False, "connected": False, "message": "DATABASE_URL no configurada"}
    if _database_error:
        return {"configured": True, "connected": False, "message": "No se pudo conectar a PostgreSQL"}
    return {"configured": True, "connected": True, "message": "PostgreSQL conectado"}


def load_user(username: str) -> Optional[dict]:
    if _engine is None:
        return None
    try:
        with Session(_engine) as db:
            record = db.get(UserRecord, username)
            return record_to_dict(record) if record else None
    except Exception as error:
        mark_database_unavailable(error)
        return None


def load_user_by_email(email: str) -> Optional[dict]:
    if _engine is None:
        return None
    try:
        with Session(_engine) as db:
            record = db.scalar(select(UserRecord).where(UserRecord.email == email))
            return record_to_dict(record) if record else None
    except Exception as error:
        mark_database_unavailable(error)
        return None


def save_user(user_data: dict) -> None:
    if _engine is None:
        return
    try:
        with Session(_engine) as db:
            db.add(UserRecord(**user_data))
            db.add(UserSessionRecord(
                user_id=user_data["user_id"],
                data={
                    "dynamic_categories": {},
                    "memory_threads": {},
                    "memory_index": {},
                    "conversations": [],
                },
            ))
            db.commit()
    except Exception as error:
        mark_database_unavailable(error)


def load_session(user_id: str) -> Optional[dict]:
    if _engine is None:
        return None
    try:
        with Session(_engine) as db:
            record = db.get(UserSessionRecord, user_id)
            return dict(record.data) if record else None
    except Exception as error:
        mark_database_unavailable(error)
        return None


def save_session(user_id: str, data: dict) -> None:
    if _engine is None:
        return
    try:
        with Session(_engine) as db:
            record = db.get(UserSessionRecord, user_id)
            if record is None:
                record = UserSessionRecord(user_id=user_id, data=data)
                db.add(record)
            else:
                record.data = data
            db.commit()
    except Exception as error:
        mark_database_unavailable(error)


def mark_database_unavailable(error: Exception) -> None:
    global _engine, _database_error
    _database_error = str(error)
    _engine = None
    print(f"⚠️ PostgreSQL no disponible: {_database_error}")


def record_to_dict(record: UserRecord) -> dict:
    return {
        "username": record.username,
        "email": record.email,
        "full_name": record.full_name,
        "hashed_password": record.hashed_password,
        "user_id": record.user_id,
        "created_at": record.created_at.isoformat(),
        "disabled": record.disabled,
    }
