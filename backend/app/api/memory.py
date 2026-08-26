from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.core.database import get_db
from app.models.schemas import MemoryItem, CategoryInfo
from app.models.database_models import Memory, Category, Conversation
from app.services.classifier.category_classifier import classifier

router = APIRouter(prefix="/memory", tags=["Memory"])


@router.get("/stats")
async def get_memory_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas de la memoria del sistema
    """
    total_conversations = db.query(func.count(Conversation.id)).scalar()
    total_memories = db.query(func.count(Memory.id)).scalar()
    
    # Conversaciones por categoría
    category_stats = db.query(
        Conversation.category,
        func.count(Conversation.id).label('count')
    ).group_by(Conversation.category).all()
    
    return {
        "total_conversations": total_conversations,
        "total_memories": total_memories,
        "categories": [
            {"name": cat, "count": count}
            for cat, count in category_stats if cat
        ]
    }


@router.get("/memories", response_model=List[MemoryItem])
async def get_all_memories(
    limit: int = 50,
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    Obtiene lista de memorias guardadas
    """
    query = db.query(Memory).filter(Memory.is_active == True)
    
    if category:
        query = query.filter(Memory.category == category)
    
    memories = query.order_by(Memory.created_at.desc()).limit(limit).all()
    
    return memories


@router.get("/categories", response_model=List[CategoryInfo])
async def get_categories(db: Session = Depends(get_db)):
    """
    Obtiene todas las categorías disponibles
    """
    categories = []
    
    for cat_name in classifier.get_all_categories():
        cat_info = classifier.get_category_info(cat_name)
        
        # Contar conversaciones en esta categoría
        count = db.query(func.count(Conversation.id))\
            .filter(Conversation.category == cat_name)\
            .scalar()
        
        categories.append(CategoryInfo(
            id=hash(cat_name) % 10000,  # ID temporal
            name=cat_name,
            description=f"Categoría de {cat_name}",
            keywords=cat_info.get("keywords", [])[:10],  # Primeras 10
            color=cat_info.get("color"),
            icon=cat_info.get("icon"),
            conversation_count=count
        ))
    
    return categories


@router.delete("/memories/{memory_id}")
async def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina (desactiva) una memoria
    """
    memory = db.query(Memory).filter(Memory.id == memory_id).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail="Memoria no encontrada")
    
    memory.is_active = False
    db.commit()
    
    return {"message": "Memoria eliminada exitosamente"}
