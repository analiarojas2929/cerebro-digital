import pytest
from app.services.neural.embeddings import embedding_service


def test_embedding_generation():
    """Test generación de embeddings"""
    text = "Este es un texto de prueba"
    embedding = embedding_service.encode(text)
    
    assert embedding is not None
    assert len(embedding.shape) == 1
    assert embedding.shape[0] > 0


def test_embedding_similarity():
    """Test cálculo de similitud"""
    text1 = "Me gusta programar en Python"
    text2 = "Python es mi lenguaje favorito"
    text3 = "El clima está muy soleado hoy"
    
    emb1 = embedding_service.encode(text1)
    emb2 = embedding_service.encode(text2)
    emb3 = embedding_service.encode(text3)
    
    # Textos similares deberían tener mayor similitud
    sim_12 = embedding_service.similarity(emb1, emb2)
    sim_13 = embedding_service.similarity(emb1, emb3)
    
    assert sim_12 > sim_13
    assert 0 <= sim_12 <= 1
    assert 0 <= sim_13 <= 1
