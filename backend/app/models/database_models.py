from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Conversation(Base):
    """Tabla principal de conversaciones"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True, nullable=False)
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    category = Column(String(100), index=True)
    sentiment = Column(String(50))
    importance_score = Column(Float, default=0.0)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Memory(Base):
    """Tabla de memoria a largo plazo"""
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    category = Column(String(100), index=True)
    importance_score = Column(Float, default=0.0)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime(timezone=True))
    embedding_id = Column(String(255), index=True)  # ID en ChromaDB
    metadata = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Category(Base):
    """Categorías aprendidas por el sistema"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    keywords = Column(JSON)  # Lista de palabras clave
    color = Column(String(50))  # Para UI
    icon = Column(String(50))  # Para UI
    conversation_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserPreference(Base):
    """Preferencias y contexto del usuario"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    preferences = Column(JSON)  # Diccionario de preferencias
    context = Column(JSON)  # Contexto personal
    last_interaction = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
