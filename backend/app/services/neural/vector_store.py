import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.neural.embeddings import embedding_service
from loguru import logger
import uuid


class VectorStore:
    """Servicio de base de datos vectorial con ChromaDB"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self._initialize_db()
    
    def _initialize_db(self):
        """Inicializa la base de datos vectorial"""
        try:
            logger.info("Inicializando ChromaDB...")
            
            # Crear cliente persistente
            self.client = chromadb.Client(ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIR,
                anonymized_telemetry=False
            ))
            
            # Crear o recuperar colección
            self.collection = self.client.get_or_create_collection(
                name="cerebro_memories",
                metadata={"description": "Memoria semántica del cerebro digital"}
            )
            
            logger.success(f"ChromaDB inicializado. Items: {self.collection.count()}")
            
        except Exception as e:
            logger.error(f"Error al inicializar ChromaDB: {e}")
            raise
    
    def add_memory(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        memory_id: Optional[str] = None
    ) -> str:
        """
        Añade una memoria a la base de datos vectorial
        
        Args:
            content: Contenido de la memoria
            metadata: Metadata adicional
            memory_id: ID opcional (se genera uno si no se proporciona)
            
        Returns:
            ID de la memoria
        """
        try:
            if not memory_id:
                memory_id = str(uuid.uuid4())
            
            # Generar embedding
            embedding = embedding_service.encode(content)
            
            # Añadir a ChromaDB
            self.collection.add(
                embeddings=[embedding.tolist()],
                documents=[content],
                metadatas=[metadata or {}],
                ids=[memory_id]
            )
            
            logger.debug(f"Memoria añadida: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error al añadir memoria: {e}")
            raise
    
    def search_similar(
        self,
        query: str,
        limit: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca memorias similares usando búsqueda semántica
        
        Args:
            query: Texto de búsqueda
            limit: Número máximo de resultados
            filter_metadata: Filtros de metadata
            
        Returns:
            Lista de memorias similares con sus scores
        """
        try:
            # Generar embedding del query
            query_embedding = embedding_service.encode(query)
            
            # Buscar en ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=limit,
                where=filter_metadata
            )
            
            # Formatear resultados
            memories = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    memories.append({
                        'id': results['ids'][0][i],
                        'content': doc,
                        'similarity': 1 - results['distances'][0][i],  # Convertir distancia a similitud
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                    })
            
            return memories
            
        except Exception as e:
            logger.error(f"Error en búsqueda semántica: {e}")
            return []
    
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Recupera una memoria específica por ID"""
        try:
            result = self.collection.get(ids=[memory_id])
            if result['documents']:
                return {
                    'id': result['ids'][0],
                    'content': result['documents'][0],
                    'metadata': result['metadatas'][0] if result['metadatas'] else {}
                }
            return None
        except Exception as e:
            logger.error(f"Error al recuperar memoria: {e}")
            return None
    
    def delete_memory(self, memory_id: str):
        """Elimina una memoria"""
        try:
            self.collection.delete(ids=[memory_id])
            logger.debug(f"Memoria eliminada: {memory_id}")
        except Exception as e:
            logger.error(f"Error al eliminar memoria: {e}")
    
    def count(self) -> int:
        """Retorna el número total de memorias"""
        return self.collection.count()


# Singleton instance
vector_store = VectorStore()
