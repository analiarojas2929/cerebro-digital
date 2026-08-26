"""
Servicio de Memoria Persistente con PostgreSQL + pgvector
Reemplaza el sistema in-memory por almacenamiento real
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from sqlalchemy import text
from app.core.db_manager import get_db, engine
from app.services.neural.embedding_service import get_embedding_service


class MemoryService:
    """Servicio principal de gestión de memorias"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
    
    def create_memory(
        self,
        content: str,
        user_id: int = 1,
        memory_type: str = "general",
        importance: float = 0.5,
        confidence: float = 1.0
    ) -> int:
        """
        Crea una nueva memoria con su embedding
        
        Args:
            content: Texto de la memoria
            user_id: ID del usuario
            memory_type: Tipo (FACT, OPINION, GOAL, EVENT, etc.)
            importance: Valor 0-1
            confidence: Confianza 0-1
            
        Returns:
            ID de la memoria creada
        """
        # Generar embedding
        embedding = self.embedding_service.generate_embedding(content)
        
        # Crear short_content
        short_content = content[:255] if len(content) > 255 else content
        
        with get_db() as db:
            result = db.execute(
                text("""
                INSERT INTO memories (user_id, content, short_content, embedding, memory_type, importance, confidence)
                VALUES (:user_id, :content, :short_content, :embedding, :memory_type, :importance, :confidence)
                RETURNING id
                """),
                {
                    "user_id": user_id,
                    "content": content,
                    "short_content": short_content,
                    "embedding": str(embedding),  # pgvector acepta string
                    "memory_type": memory_type,
                    "importance": importance,
                    "confidence": confidence
                }
            )
            memory_id = result.fetchone()[0]
            
        return memory_id
    
    def semantic_search(
        self,
        query: str,
        user_id: int = 1,
        limit: int = 5,
        min_similarity: float = 0.3
    ) -> List[Dict]:
        """
        Búsqueda semántica usando embeddings
        
        Args:
            query: Pregunta o búsqueda
            user_id: ID del usuario
            limit: Número máximo de resultados
            min_similarity: Similitud mínima (0-1)
            
        Returns:
            Lista de memorias ordenadas por relevancia
        """
        # Generar embedding de la query
        query_embedding = self.embedding_service.generate_embedding(query)
        
        with get_db() as db:
            # Búsqueda por similitud coseno
            result = db.execute(
                text("""
                SELECT 
                    id,
                    content,
                    short_content,
                    created_at,
                    memory_type,
                    importance,
                    confidence,
                    1 - (embedding <=> :query_embedding) as similarity
                FROM memories
                WHERE user_id = :user_id
                    AND (1 - (embedding <=> :query_embedding)) >= :min_similarity
                ORDER BY similarity DESC
                LIMIT :limit
                """),
                {
                    "query_embedding": str(query_embedding),
                    "user_id": user_id,
                    "min_similarity": min_similarity,
                    "limit": limit
                }
            )
            
            memories = []
            for row in result:
                memories.append({
                    "id": row[0],
                    "content": row[1],
                    "short_content": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                    "memory_type": row[4],
                    "importance": float(row[5]) if row[5] else 0.5,
                    "confidence": float(row[6]) if row[6] else 1.0,
                    "similarity": float(row[7]) if row[7] else 0.0
                })
            
        return memories
    
    def add_entity_to_memory(
        self,
        memory_id: int,
        entity_name: str,
        entity_type: str,
        icon: str = "📌"
    ) -> int:
        """
        Agrega una entidad a una memoria (persona, lugar, evento)
        """
        with get_db() as db:
            # Crear o recuperar entidad
            result = db.execute(
                text("""
                INSERT INTO entities (name, entity_type, icon)
                VALUES (:name, :entity_type, :icon)
                ON CONFLICT (name, entity_type) DO UPDATE SET icon = :icon
                RETURNING id
                """),
                {"name": entity_name, "entity_type": entity_type, "icon": icon}
            )
            entity_id = result.fetchone()[0]
            
            # Asociar memoria-entidad
            db.execute(
                text("""
                INSERT INTO memory_entities (memory_id, entity_id)
                VALUES (:memory_id, :entity_id)
                ON CONFLICT DO NOTHING
                """),
                {"memory_id": memory_id, "entity_id": entity_id}
            )
            
        return entity_id
    
    def add_memory_to_category(
        self,
        memory_id: int,
        category_name: str,
        subcategory_name: str,
        subcategory_icon: str = "📌"
    ):
        """
        Asocia una memoria a una categoría/subcategoría
        """
        with get_db() as db:
            # Obtener ID de categoría
            result = db.execute(
                text("SELECT id FROM categories WHERE name = :name"),
                {"name": category_name}
            )
            row = result.fetchone()
            if not row:
                return
            category_id = row[0]
            
            # Crear o recuperar subcategoría
            result = db.execute(
                text("""
                INSERT INTO subcategories (category_id, name, icon)
                VALUES (:category_id, :name, :icon)
                ON CONFLICT (category_id, name) DO UPDATE SET icon = :icon
                RETURNING id
                """),
                {
                    "category_id": category_id,
                    "name": subcategory_name,
                    "icon": subcategory_icon
                }
            )
            subcategory_id = result.fetchone()[0]
            
            # Asociar memoria-subcategoría
            db.execute(
                text("""
                INSERT INTO memory_subcategories (memory_id, subcategory_id)
                VALUES (:memory_id, :subcategory_id)
                ON CONFLICT DO NOTHING
                """),
                {"memory_id": memory_id, "subcategory_id": subcategory_id}
            )
    
    def get_recent_memories(self, user_id: int = 1, limit: int = 50) -> List[Dict]:
        """Obtiene las memorias más recientes"""
        with get_db() as db:
            result = db.execute(
                text("""
                SELECT id, content, short_content, created_at, memory_type, importance
                FROM memories
                WHERE user_id = :user_id
                ORDER BY created_at DESC
                LIMIT :limit
                """),
                {"user_id": user_id, "limit": limit}
            )
            
            memories = []
            for row in result:
                memories.append({
                    "id": row[0],
                    "content": row[1],
                    "short_content": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                    "memory_type": row[4],
                    "importance": float(row[5]) if row[5] else 0.5
                })
            
        return memories
    
    def add_comment(
        self,
        memory_id: int,
        content: str,
        user_name: str = "Usuario"
    ) -> int:
        """Agrega un comentario a una memoria"""
        with get_db() as db:
            result = db.execute(
                text("""
                INSERT INTO memory_comments (memory_id, content, user_name)
                VALUES (:memory_id, :content, :user_name)
                RETURNING id
                """),
                {
                    "memory_id": memory_id,
                    "content": content,
                    "user_name": user_name
                }
            )
            comment_id = result.fetchone()[0]
            
        return comment_id
    
    def get_memory_thread(self, memory_id: int) -> List[Dict]:
        """Obtiene todos los comentarios de una memoria"""
        with get_db() as db:
            result = db.execute(
                text("""
                SELECT id, content, user_name, created_at, layer
                FROM memory_comments
                WHERE memory_id = :memory_id
                ORDER BY created_at ASC
                """),
                {"memory_id": memory_id}
            )
            
            comments = []
            for row in result:
                comments.append({
                    "id": row[0],
                    "content": row[1],
                    "user": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                    "layer": row[4]
                })
            
        return comments


# Instancia global
_memory_service = None

def get_memory_service() -> MemoryService:
    """Obtiene la instancia global del servicio de memoria"""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
    return _memory_service
