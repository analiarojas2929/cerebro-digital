import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_root():
    """Test endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Cerebro Digital" in response.json()["name"]


def test_health_check():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_send_message():
    """Test envío de mensaje"""
    response = client.post(
        "/chat/message",
        json={"message": "Hola, ¿cómo estás?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert data["session_id"] is not None


def test_get_categories():
    """Test obtención de categorías"""
    response = client.get("/memory/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) > 0


def test_get_memory_stats():
    """Test estadísticas de memoria"""
    response = client.get("/memory/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_conversations" in stats
    assert "total_memories" in stats


def test_search_memories():
    """Test búsqueda en memoria"""
    # Primero enviar un mensaje para tener algo que buscar
    client.post(
        "/chat/message",
        json={"message": "Me gusta programar en Python"}
    )
    
    # Buscar
    response = client.post(
        "/chat/search",
        json={"query": "Python", "limit": 5}
    )
    assert response.status_code == 200
    results = response.json()
    assert isinstance(results, list)
