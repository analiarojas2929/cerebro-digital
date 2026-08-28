"""
Sistema de Autenticación y Gestión de Usuarios
Manejo de login, registro y sesiones
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
import hashlib
import uuid
import os
from pydantic import BaseModel
from auth_database import (
    initialize_database, load_session, load_user, load_user_by_email,
    save_session, save_user,
)

# Configuración
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-only-change-this-secret-before-deploying",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 días

# Base de datos simple de usuarios (en memoria)
# En producción, esto debería estar en PostgreSQL
users_db = {}  # username -> user_data
user_sessions = {}  # user_id -> {dynamic_categories, memory_threads, memory_index, conversations}

initialize_database()

def empty_session() -> dict:
    return {
        "dynamic_categories": {},
        "memory_threads": {},
        "memory_index": {},
        "conversations": [],
    }

# Modelos
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str
    user_id: str
    created_at: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

# Funciones de utilidad
def hash_password(password: str) -> str:
    """Hash de contraseña usando SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """Decodificar y verificar token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_user(username: str) -> Optional[UserInDB]:
    """Obtener usuario de la base de datos"""
    if username in users_db:
        user_data = users_db[username]
        return UserInDB(**user_data)
    user_data = load_user(username)
    if user_data:
        users_db[username] = user_data
        return UserInDB(**user_data)
    return None

def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Autenticar usuario"""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(user_data: UserCreate) -> UserInDB:
    """Crear nuevo usuario"""
    # Verificar si el usuario ya existe
    if user_data.username in users_db:
        raise ValueError("El nombre de usuario ya está en uso")
    
    # Verificar si el email ya existe
    for existing_user in users_db.values():
        if existing_user["email"] == user_data.email:
            raise ValueError("El email ya está registrado")
    if load_user_by_email(user_data.email):
        raise ValueError("El email ya está registrado")
    
    # Crear usuario
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name or user_data.username,
        "hashed_password": hashed_password,
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
        "disabled": False
    }
    
    users_db[user_data.username] = new_user
    save_user(new_user)
    
    # Inicializar sesión de usuario
    user_sessions[user_id] = empty_session()
    
    return UserInDB(**new_user)

def get_user_session(user_id: str) -> dict:
    """Obtener sesión del usuario (sus datos aislados)"""
    if user_id not in user_sessions:
        stored_session = load_session(user_id) or {}
        user_sessions[user_id] = {
            **empty_session(),
            **stored_session,
        }
    return user_sessions[user_id]

def get_current_user(token: str) -> Optional[UserInDB]:
    """Obtener usuario actual desde token"""
    payload = decode_token(token)
    if payload is None:
        return None
    
    username: str = payload.get("sub")
    if username is None:
        return None
    
    user = get_user(username)
    if user is None:
        return None
    
    if user.disabled:
        return None
    
    return user

# Inicializar usuarios demo (opcional, para testing)
def initialize_demo_users():
    """Crear usuarios de demostración"""
    demo_users = [
        UserCreate(
            username="demo",
            email="demo@cerebro.digital",
            password="demo123",
            full_name="Usuario Demo"
        ),
        UserCreate(
            username="admin",
            email="admin@cerebro.digital",
            password="admin123",
            full_name="Administrador"
        )
    ]
    
    for user_data in demo_users:
        try:
            create_user(user_data)
            print(f"✅ Usuario demo creado: {user_data.username}")
        except ValueError:
            pass  # Usuario ya existe

# Llamar al inicializar el módulo (opcional)
# initialize_demo_users()
