from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.schemas import (
    MessageInput, MessageResponse, ConversationHistory,
    SearchQuery, SearchResult
)
from app.services.conversation.conversation_service import conversation_service
from app.services.memory.memory_manager import memory_manager
from app.models.database_models import Conversation

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=MessageResponse)
async def send_message(
    message_input: MessageInput,
    db: Session = Depends(get_db)
):
    """
    Envía un mensaje al cerebro digital y obtiene respuesta
    
    El sistema:
    - Analiza el mensaje y lo clasifica
    - Busca información relevante en memoria
    - Genera una respuesta contextualizada
    - Guarda la conversación en memoria
    """
    try:
        response = conversation_service.process_message(message_input, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}", response_model=List[ConversationHistory])
async def get_conversation_history(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de conversación de una sesión
    """
    conversations = db.query(Conversation)\
        .filter(Conversation.session_id == session_id)\
        .order_by(Conversation.created_at.desc())\
        .limit(limit)\
        .all()
    
    return conversations


@router.post("/search", response_model=List[SearchResult])
async def search_memories(
    search_query: SearchQuery,
    db: Session = Depends(get_db)
):
    """
    Busca en la memoria del cerebro digital usando búsqueda semántica
    """
    try:
        results = memory_manager.search_memories(
            query=search_query.query,
            limit=search_query.limit,
            category=search_query.category
        )
        
        return [
            SearchResult(
                content=r["content"],
                category=r["metadata"].get("category"),
                similarity=r["similarity"],
                metadata=r["metadata"]
            )
            for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consolidate/{session_id}")
async def consolidate_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Consolida la memoria de corto plazo a largo plazo
    """
    try:
        memory_manager.consolidate_memory(db, session_id)
        return {"message": "Memoria consolidada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
