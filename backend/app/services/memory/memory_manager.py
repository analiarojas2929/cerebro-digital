from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
from loguru import logger

from app.models.database_models import Conversation, Memory
from app.services.neural.vector_store import vector_store
from app.services.classifier.category_classifier import classifier
from app.core.redis_client import get_redis


class MemoryManager:
    """Gestor de memoria de corto y largo plazo"""
    
    def __init__(self):
        self.redis = get_redis()
        self.short_term_prefix = "stm:"  # Short-Term Memory
        self.context_prefix = "ctx:"     # Context
    
    def add_to_short_term(
        self,
        session_id: str,
        user_message: str,
        assistant_message: str,
        ttl: int = 3600
    ):
        """
        Añade una conversación a memoria de corto plazo (Redis)
        
        Args:
            session_id: ID de sesión
            user_message: Mensaje del usuario
            assistant_message: Respuesta del asistente
            ttl: Tiempo de vida en segundos (default: 1 hora)
        """
        try:
            key = f"{self.short_term_prefix}{session_id}"
            
            conversation = {
                'user': user_message,
                'assistant': assistant_message,
                'timestamp': datetime.now().isoformat()
            }
            
            # Añadir a lista en Redis
            self.redis.lpush(key, json.dumps(conversation))
            
            # Limitar tamaño de la lista (últimas 50 conversaciones)
            self.redis.ltrim(key, 0, 49)
            
            # Establecer TTL
            self.redis.expire(key, ttl)
            
            logger.debug(f"Añadido a memoria corto plazo: {session_id}")
            
        except Exception as e:
            logger.error(f"Error al añadir a memoria corto plazo: {e}")
    
    def get_short_term_context(self, session_id: str, limit: int = 10) -> List[Dict]:
        """
        Recupera el contexto de memoria de corto plazo
        
        Args:
            session_id: ID de sesión
            limit: Número máximo de conversaciones a recuperar
            
        Returns:
            Lista de conversaciones recientes
        """
        try:
            key = f"{self.short_term_prefix}{session_id}"
            
            # Obtener últimas conversaciones
            conversations = self.redis.lrange(key, 0, limit - 1)
            
            return [json.loads(conv) for conv in conversations]
            
        except Exception as e:
            logger.error(f"Error al recuperar memoria corto plazo: {e}")
            return []
    
    def save_to_long_term(
        self,
        db: Session,
        content: str,
        category: Optional[str] = None,
        importance_score: float = 0.0,
        metadata: Optional[Dict] = None
    ) -> Memory:
        """
        Guarda información en memoria de largo plazo (PostgreSQL + ChromaDB)
        
        Args:
            db: Sesión de base de datos
            content: Contenido a guardar
            category: Categoría (opcional)
            importance_score: Puntuación de importancia
            metadata: Metadata adicional
            
        Returns:
            Objeto Memory creado
        """
        try:
            # Clasificar si no tiene categoría
            if not category:
                category, confidence = classifier.classify(content)
            
            # Generar resumen (primeras 200 caracteres por ahora)
            summary = content[:200] + "..." if len(content) > 200 else content
            
            # Guardar en ChromaDB
            embedding_id = vector_store.add_memory(
                content=content,
                metadata={
                    "category": category,
                    "importance": importance_score,
                    **(metadata or {})
                }
            )
            
            # Guardar en PostgreSQL
            memory = Memory(
                content=content,
                summary=summary,
                category=category,
                importance_score=importance_score,
                embedding_id=embedding_id,
                metadata=metadata or {},
                last_accessed=datetime.now()
            )
            
            db.add(memory)
            db.commit()
            db.refresh(memory)
            
            logger.info(f"Memoria guardada en largo plazo: {memory.id}")
            return memory
            
        except Exception as e:
            logger.error(f"Error al guardar en memoria largo plazo: {e}")
            db.rollback()
            raise
    
    def search_memories(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca en memoria de largo plazo usando búsqueda semántica
        
        Args:
            query: Consulta de búsqueda
            limit: Número máximo de resultados
            category: Filtrar por categoría
            
        Returns:
            Lista de memorias relevantes
        """
        filter_metadata = {"category": category} if category else None
        
        return vector_store.search_similar(
            query=query,
            limit=limit,
            filter_metadata=filter_metadata
        )
    
    def get_conversation_context(
        self,
        session_id: str,
        current_message: str,
        db: Session
    ) -> str:
        """
        Genera contexto completo para la conversación actual
        Combina memoria de corto plazo + búsqueda semántica de largo plazo
        
        Args:
            session_id: ID de sesión
            current_message: Mensaje actual del usuario
            db: Sesión de base de datos
            
        Returns:
            String con el contexto formateado
        """
        context_parts = []
        
        # 1. Memoria de corto plazo (últimas conversaciones)
        short_term = self.get_short_term_context(session_id, limit=5)
        if short_term:
            context_parts.append("## Conversación Reciente:")
            for conv in reversed(short_term):  # Orden cronológico
                context_parts.append(f"Usuario: {conv['user']}")
                context_parts.append(f"Asistente: {conv['assistant']}\n")
        
        # 2. Memoria de largo plazo (búsqueda semántica)
        relevant_memories = self.search_memories(current_message, limit=3)
        if relevant_memories:
            context_parts.append("\n## Información Relevante de Memoria:")
            for mem in relevant_memories:
                if mem['similarity'] > 0.7:  # Solo memorias muy relevantes
                    context_parts.append(f"- {mem['content']} (relevancia: {mem['similarity']:.2f})")
        
        return "\n".join(context_parts)
    
    def consolidate_memory(self, db: Session, session_id: str):
        """
        Consolida memoria de corto plazo a largo plazo
        (Ejecutar periódicamente o al final de sesiones importantes)
        """
        try:
            # Obtener todas las conversaciones de corto plazo
            conversations = self.get_short_term_context(session_id, limit=50)
            
            if not conversations:
                return
            
            # Combinar en un resumen
            combined_text = "\n".join([
                f"Usuario: {c['user']}\nAsistente: {c['assistant']}"
                for c in reversed(conversations)
            ])
            
            # Guardar en largo plazo con alta importancia
            self.save_to_long_term(
                db=db,
                content=combined_text,
                importance_score=0.8,
                metadata={"type": "consolidated_session", "session_id": session_id}
            )
            
            logger.info(f"Memoria consolidada para sesión: {session_id}")
            
        except Exception as e:
            logger.error(f"Error al consolidar memoria: {e}")


# Singleton instance
memory_manager = MemoryManager()
