from typing import List, Dict, Tuple
from collections import Counter
import re
from loguru import logger


class CategoryClassifier:
    """Clasificador de categorías basado en keywords y patrones"""
    
    def __init__(self):
        # Categorías predefinidas con palabras clave
        self.categories = {
            "trabajo": {
                "keywords": ["trabajo", "proyecto", "reunión", "cliente", "tarea", "deadline", 
                           "equipo", "jefe", "oficina", "empresa", "negocio", "productividad"],
                "color": "#3B82F6",
                "icon": "💼"
            },
            "personal": {
                "keywords": ["familia", "amigo", "casa", "personal", "privado", "yo", 
                           "sentimiento", "emoción", "pensar", "vida"],
                "color": "#10B981",
                "icon": "🏠"
            },
            "aprendizaje": {
                "keywords": ["aprender", "estudiar", "curso", "tutorial", "libro", "conocimiento",
                           "entender", "práctica", "habilidad", "mejora", "skill"],
                "color": "#8B5CF6",
                "icon": "📚"
            },
            "tecnología": {
                "keywords": ["código", "programar", "python", "javascript", "api", "database",
                           "servidor", "deploy", "bug", "feature", "framework", "react"],
                "color": "#EF4444",
                "icon": "💻"
            },
            "salud": {
                "keywords": ["salud", "ejercicio", "dormir", "comida", "dieta", "médico",
                           "bienestar", "fitness", "nutrición", "enfermedad"],
                "color": "#F59E0B",
                "icon": "🏥"
            },
            "finanzas": {
                "keywords": ["dinero", "pagar", "comprar", "inversión", "banco", "ahorro",
                           "presupuesto", "gasto", "ingreso", "factura", "precio"],
                "color": "#14B8A6",
                "icon": "💰"
            },
            "entretenimiento": {
                "keywords": ["película", "serie", "juego", "música", "deporte", "hobby",
                           "diversión", "tiempo libre", "vacaciones", "viajar"],
                "color": "#EC4899",
                "icon": "🎮"
            },
            "ideas": {
                "keywords": ["idea", "concepto", "propuesta", "innovación", "creatividad",
                           "brainstorm", "planear", "futuro", "visión", "objetivo"],
                "color": "#F97316",
                "icon": "💡"
            }
        }
    
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Clasifica un texto en una categoría
        
        Args:
            text: Texto a clasificar
            
        Returns:
            Tupla (categoría, confianza)
        """
        text_lower = text.lower()
        
        # Contar coincidencias de keywords por categoría
        scores = {}
        for category, data in self.categories.items():
            score = 0
            for keyword in data["keywords"]:
                # Buscar palabra completa (no substring)
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            scores[category] = score
        
        # Obtener categoría con mayor score
        if max(scores.values()) == 0:
            return "general", 0.0
        
        best_category = max(scores, key=scores.get)
        max_score = scores[best_category]
        
        # Calcular confianza (normalizada)
        total_matches = sum(scores.values())
        confidence = max_score / total_matches if total_matches > 0 else 0.0
        
        return best_category, confidence
    
    def classify_batch(self, texts: List[str]) -> List[Tuple[str, float]]:
        """Clasifica múltiples textos"""
        return [self.classify(text) for text in texts]
    
    def get_category_info(self, category: str) -> Dict:
        """Obtiene información de una categoría"""
        return self.categories.get(category, {
            "keywords": [],
            "color": "#6B7280",
            "icon": "📌"
        })
    
    def get_all_categories(self) -> List[str]:
        """Retorna lista de todas las categorías disponibles"""
        return list(self.categories.keys())
    
    def add_keyword_to_category(self, category: str, keyword: str):
        """Añade una keyword a una categoría (aprendizaje dinámico)"""
        if category in self.categories:
            if keyword.lower() not in self.categories[category]["keywords"]:
                self.categories[category]["keywords"].append(keyword.lower())
                logger.info(f"Keyword '{keyword}' añadida a categoría '{category}'")


# Singleton instance
classifier = CategoryClassifier()
