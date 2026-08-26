"""
Sistema de Embeddings para búsqueda semántica
Usa sentence-transformers para generar vectores de 384 dimensiones
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Tuple
import os

class EmbeddingService:
    """Servicio para generar y buscar embeddings"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Inicializa el modelo de embeddings
        all-MiniLM-L6-v2: 384 dimensiones, rápido, buena calidad
        """
        print(f"📦 Cargando modelo de embeddings: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # Dimensión del modelo
        print(f"✅ Modelo cargado ({self.dimension}D)")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Genera embedding para un texto
        
        Args:
            text: Texto a convertir en vector
            
        Returns:
            Vector de 384 dimensiones
        """
        if not text or not text.strip():
            return [0.0] * self.dimension
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Genera embeddings para múltiples textos (más eficiente)
        
        Args:
            texts: Lista de textos
            
        Returns:
            Lista de vectores
        """
        if not texts:
            return []
        
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings.tolist()
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcula similitud coseno entre dos vectores
        
        Returns:
            Valor entre -1 y 1 (1 = idénticos, 0 = ortogonales, -1 = opuestos)
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def find_most_similar(
        self, 
        query_embedding: List[float], 
        candidate_embeddings: List[List[float]],
        top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Encuentra los embeddings más similares a la query
        
        Args:
            query_embedding: Vector de búsqueda
            candidate_embeddings: Lista de vectores candidatos
            top_k: Número de resultados a retornar
            
        Returns:
            Lista de tuplas (índice, similitud) ordenadas por similitud descendente
        """
        similarities = []
        for idx, candidate in enumerate(candidate_embeddings):
            sim = self.cosine_similarity(query_embedding, candidate)
            similarities.append((idx, sim))
        
        # Ordenar por similitud descendente
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]


# Instancia global del servicio
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    """Obtiene o crea la instancia global del servicio de embeddings"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


# Funciones de conveniencia
def generate_embedding(text: str) -> List[float]:
    """Genera embedding para un texto (función helper)"""
    service = get_embedding_service()
    return service.generate_embedding(text)


def search_similar_texts(
    query: str,
    texts: List[str],
    top_k: int = 5
) -> List[Tuple[int, float, str]]:
    """
    Busca textos similares a una query
    
    Args:
        query: Texto de búsqueda
        texts: Lista de textos donde buscar
        top_k: Número de resultados
        
    Returns:
        Lista de (índice, similitud, texto) ordenados por similitud
    """
    service = get_embedding_service()
    
    # Generar embeddings
    query_emb = service.generate_embedding(query)
    text_embs = service.generate_embeddings_batch(texts)
    
    # Buscar más similares
    results = service.find_most_similar(query_emb, text_embs, top_k)
    
    # Agregar textos a los resultados
    return [(idx, sim, texts[idx]) for idx, sim in results]


if __name__ == "__main__":
    # Test del servicio
    print("🧪 Probando servicio de embeddings...")
    
    service = get_embedding_service()
    
    # Test 1: Embedding simple
    text = "Mi pareja se llama Sebastián"
    emb = service.generate_embedding(text)
    print(f"\n📊 Embedding generado: {len(emb)} dimensiones")
    print(f"   Primeros 5 valores: {emb[:5]}")
    
    # Test 2: Búsqueda semántica
    memories = [
        "Mi pareja es Sebastián Montero",
        "Llevamos 3 años juntos",
        "Fui a Viña del Mar",
        "Mi hermano vive en Santiago",
        "Estoy muy feliz con mi relación"
    ]
    
    query = "información sobre mi pareja"
    results = search_similar_texts(query, memories, top_k=3)
    
    print(f"\n🔍 Búsqueda: '{query}'")
    print("   Resultados:")
    for idx, sim, text in results:
        print(f"   {sim:.3f} - {text}")
