from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MessageInput(BaseModel):
    """Mensaje de entrada del usuario"""
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[str] = None
    user_id: Optional[str] = "default_user"


class MessageResponse(BaseModel):
    """Respuesta del asistente"""
    response: str
    session_id: str
    category: Optional[str] = None
    sentiment: Optional[str] = None
    related_memories: List[Dict[str, Any]] = []
    confidence: float = 0.0


class ConversationHistory(BaseModel):
    """Historial de conversación"""
    id: int
    session_id: str
    user_message: str
    assistant_message: str
    category: Optional[str]
    sentiment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MemoryItem(BaseModel):
    """Item de memoria"""
    id: int
    content: str
    summary: Optional[str]
    category: Optional[str]
    importance_score: float
    access_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CategoryInfo(BaseModel):
    """Información de categoría"""
    id: int
    name: str
    description: Optional[str]
    keywords: List[str] = []
    color: Optional[str]
    icon: Optional[str]
    conversation_count: int
    
    class Config:
        from_attributes = True


class SearchQuery(BaseModel):
    """Query de búsqueda semántica"""
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=50)
    category: Optional[str] = None


class SearchResult(BaseModel):
    """Resultado de búsqueda"""
    content: str
    category: Optional[str]
    similarity: float
    metadata: Dict[str, Any] = {}
