import pytest
from app.services.classifier.category_classifier import classifier


def test_classify_trabajo():
    """Test clasificación de categoría trabajo"""
    text = "Tengo una reunión con el cliente mañana para discutir el proyecto"
    category, confidence = classifier.classify(text)
    
    assert category == "trabajo"
    assert confidence > 0


def test_classify_tecnologia():
    """Test clasificación de categoría tecnología"""
    text = "Necesito arreglar este bug en el código de Python"
    category, confidence = classifier.classify(text)
    
    assert category == "tecnología"
    assert confidence > 0


def test_classify_personal():
    """Test clasificación de categoría personal"""
    text = "Voy a pasar tiempo con mi familia este fin de semana"
    category, confidence = classifier.classify(text)
    
    assert category == "personal"
    assert confidence > 0


def test_get_all_categories():
    """Test obtención de todas las categorías"""
    categories = classifier.get_all_categories()
    
    assert isinstance(categories, list)
    assert len(categories) > 0
    assert "trabajo" in categories
    assert "tecnología" in categories


def test_add_keyword():
    """Test añadir keyword a categoría"""
    classifier.add_keyword_to_category("trabajo", "sprint")
    
    info = classifier.get_category_info("trabajo")
    assert "sprint" in info["keywords"]
