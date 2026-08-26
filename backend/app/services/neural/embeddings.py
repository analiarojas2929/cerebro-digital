from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
from app.core.config import settings
from loguru import logger


class EmbeddingService:
    """Servicio para generar embeddings de texto"""
    
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo de embeddings"""
        try:
            logger.info(f"Cargando modelo de embeddings: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.success("Modelo de embeddings cargado exitosamente")
        except Exception as e:
            logger.error(f"Error al cargar modelo de embeddings: {e}")
            raise
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Genera embeddings para uno o más textos
        
        Args:
            texts: Texto o lista de textos
            
        Returns:
            Array numpy con los embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            return embeddings
        except Exception as e:
            logger.error(f"Error al generar embeddings: {e}")
            raise
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calcula la similitud coseno entre dos embeddings
        
        Args:
            embedding1: Primer embedding
            embedding2: Segundo embedding
            
        Returns:
            Similitud coseno (0-1)
        """
        from numpy.linalg import norm
        
        similarity = np.dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
        return float(similarity)
    
    def get_dimension(self) -> int:
        """Retorna la dimensión del modelo de embeddings"""
        return self.model.get_sentence_embedding_dimension()


# Singleton instance
embedding_service = EmbeddingService()
