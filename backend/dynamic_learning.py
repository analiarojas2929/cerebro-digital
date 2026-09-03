"""
Sistema de Aprendizaje Dinámico con Evaluación Inteligente de Memorias
- Extrae automáticamente personas, lugares, eventos y temas
- Califica importancia de 0-100
- Clasifica como MEMORY, TEMPORARY, TRIVIAL, DUPLICATE, UPDATE
- Retorna respuesta estructurada para cada mensaje
"""
import uuid
from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional

# Tipos de decisión de memoria
class MemoryDecision(str, Enum):
    MEMORY = "MEMORY"
    TEMPORARY = "TEMPORARY"
    TRIVIAL = "TRIVIAL"
    DUPLICATE = "DUPLICATE"
    UPDATE = "UPDATE"

# Acciones recomendadas
class MemoryAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    IGNORE = "IGNORE"

# Almacenamiento de categorías dinámicas
dynamic_categories = {}

# Sistema de hilos de conversación (comentarios sobre memorias)
memory_threads = {}  # ID de memoria → lista de comentarios

# Índice de memorias por ID para acceso rápido
memory_index = {}  # ID → {category, subcategory, memory_obj}

# Memorias temporales (sesión actual)
short_term_memory = {}  # ID → {content, expires: 'session_end'}

def add_comment_to_memory(memory_id: str, comment: str, user: str = "Usuario"):
    """Agrega un comentario a una memoria existente"""
    from datetime import datetime
    
    if memory_id not in memory_threads:
        memory_threads[memory_id] = []
    
    timestamp = datetime.now()
    comment_obj = {
        'id': f"{memory_id}_comment_{len(memory_threads[memory_id])}",
        'parent_id': memory_id,
        'text': comment,
        'user': user,
        'timestamp': timestamp.isoformat(),
        'date': timestamp.strftime('%d/%m/%Y'),
        'time': timestamp.strftime('%H:%M:%S'),
        'layer': len(memory_threads[memory_id]) + 2  # Capa 0=categoría, 1=memoria, 2+=comentarios
    }
    
    memory_threads[memory_id].append(comment_obj)
    return comment_obj

def get_memory_thread(memory_id: str):
    """Obtiene el hilo completo de una memoria con todos sus comentarios"""
    return memory_threads.get(memory_id, [])

def extract_entities(text: str):
    """Extrae entidades (personas, lugares, eventos, temas) del texto"""
    text_lower = text.lower()
    entities = {
        'personas': [],
        'lugares': [],
        'eventos': [],
        'temas': []
    }
    
    # Detectar personas y relaciones familiares
    personas_keywords = {
        'papá': '👨', 'padre': '👨', 'papi': '👨',
        'mamá': '👩', 'madre': '👩', 'mami': '👩',
        'hijo': '👦', 'hija': '👧', 'hijos': '👶',
        'hermano': '👦', 'hermana': '👧',
        'abuelo': '👴', 'abuela': '👵',
        'tío': '👨', 'tía': '👩',
        'primo': '👦', 'prima': '👧',
        'esposa': '💑', 'esposo': '💑', 'pareja': '💑',
        'novio': '💑', 'novia': '💑',
        'amigo': '👥', 'amiga': '👥',
        'vecino': '🏘️', 'vecina': '🏘️'
    }
    
    for palabra, icono in personas_keywords.items():
        if palabra in text_lower:
            entities['personas'].append({'name': palabra.capitalize(), 'icon': icono})
    
    # Detectar lugares
    lugares_keywords = {
        'casa': '🏠', 'hogar': '🏠', 'domicilio': '🏠',
        'escuela': '🏫', 'colegio': '🏫', 'universidad': '🎓',
        'trabajo': '💼', 'oficina': '🏢', 'empresa': '🏢',
        'hospital': '🏥', 'clínica': '🏥', 'consultorio': '🏥',
        'iglesia': '⛪', 'templo': '⛪', 'capilla': '⛪',
        'parque': '🌳', 'plaza': '🌳', 'jardín': '🌳',
        'playa': '🏖️', 'mar': '🌊', 'costa': '🏖️',
        'montaña': '⛰️', 'campo': '🌾', 'sierra': '⛰️',
        'ciudad': '🌆', 'pueblo': '🏘️', 'localidad': '🏘️',
        'barrio': '🏘️', 'vecindario': '🏘️', 'colonia': '🏘️',
        'mercado': '🛒', 'tienda': '🏪', 'supermercado': '🛒',
        'restaurante': '🍽️', 'café': '☕', 'fonda': '🍽️',
        'calle': '🛣️', 'avenida': '🛣️', 'carretera': '🛣️',
        'aeropuerto': '✈️', 'terminal': '🚉', 'estación': '🚉',
        'hotel': '🏨', 'motel': '🏨', 'posada': '🏨'
    }
    
    for palabra, icono in lugares_keywords.items():
        if palabra in text_lower:
            entities['lugares'].append({'name': palabra.capitalize(), 'icon': icono})
    
    # Detectar lugares específicos mediante patrones más flexibles
    import re
    
    # Patrón mejorado: detectar nombres propios de lugares
    patrones_lugares = [
        r'(?:fui|voy|iré|estuve|llegué)\s+(?:a|al|a\s+la)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]{2,30})(?:\s|$|,|\.|y|con)',
        r'(?:en|desde|hacia|por)\s+(?:el|la)?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]{2,30})(?:\s|$|,|\.|y|con)',
        r'lugar\s+llamado\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]{2,30})(?:\s|$|,|\.|y|con)',
        r'(?:vivo|vive|vivimos)\s+en\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]{2,30})(?:\s|$|,|\.|y|con)',
        r'(?:de|del)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]{2,30})\s+(?:a|al|hacia)',
    ]
    
    for patron in patrones_lugares:
        matches = re.finditer(patron, text, re.IGNORECASE)  # Usar mensaje original para preservar mayúsculas
        for match in matches:
            lugar_nombre = match.group(1).strip()
            # Filtrar palabras comunes que no son lugares
            palabras_excluir = ['mi', 'el', 'la', 'un', 'una', 'que', 'con', 'por', 'para', 
                               'año', 'día', 'mes', 'vez', 'momento', 'tiempo', 'hora']
            if lugar_nombre.lower() not in palabras_excluir and len(lugar_nombre) > 2:
                entities['lugares'].append({
                    'name': lugar_nombre.strip(), 
                    'icon': '📍'
                })
    
    # Detectar eventos y momentos especiales
    eventos_keywords = {
        'cumpleaños': '🎂', 'cumple': '🎂',
        'boda': '💒', 'matrimonio': '💒',
        'graduación': '🎓', 'graduar': '🎓',
        'viaje': '✈️', 'vacaciones': '🏖️',
        'fiesta': '🎉', 'celebración': '🎉',
        'reunión': '👥', 'junta': '👥',
        'navidad': '🎄', 'año nuevo': '🎆',
        'aniversario': '💝', 'funeral': '⚰️',
        'bautizo': '👶', 'comunión': '⛪',
        'quinceañera': '👸', 'XV años': '👸'
    }
    
    for palabra, icono in eventos_keywords.items():
        if palabra in text_lower:
            entities['eventos'].append({'name': palabra.capitalize(), 'icon': icono})
    
    # Detectar temas emocionales y conceptuales
    temas_patterns = {
        'Alegría': {
            'icon': '😊',
            'keywords': ['feliz', 'alegre', 'contento', 'emocionado', 'celebrar', 'disfrutar']
        },
        'Tristeza': {
            'icon': '😢',
            'keywords': ['triste', 'llorar', 'pena', 'dolor', 'perdida', 'melancolía']
        },
        'Aprendizaje': {
            'icon': '📚',
            'keywords': ['aprender', 'estudiar', 'enseñar', 'lección', 'descubrir', 'conocer']
        },
        'Logro': {
            'icon': '🏆',
            'keywords': ['lograr', 'conseguir', 'éxito', 'ganar', 'alcanzar', 'cumplir']
        },
        'Amor': {
            'icon': '❤️',
            'keywords': ['amor', 'querer', 'amar', 'cariño', 'querido', 'adorar']
        },
        'Consejo': {
            'icon': '💡',
            'keywords': ['consejo', 'recomendación', 'sugerencia', 'recordar que', 'importante']
        },
        'Nostalgia': {
            'icon': '🕰️',
            'keywords': ['recordar', 'recuerdo', 'antes', 'época', 'cuando era']
        },
        'Gratitud': {
            'icon': '🙏',
            'keywords': ['gracias', 'agradecer', 'bendición', 'afortunado', 'suerte']
        }
    }
    
    for tema, info in temas_patterns.items():
        if any(kw in text_lower for kw in info['keywords']):
            entities['temas'].append({'name': tema, 'icon': info['icon']})
    
    return entities


def calculate_memory_score(message: str, entities: dict) -> int:
    """
    Calcula un score de importancia de 0-100 para un mensaje.
    Retorna importancia basada en múltiples criterios.
    """
    score = 0
    text = message.strip().lower()
    
    # Criterio 1: Longitud (hasta 15 puntos)
    # Mensajes muy cortos son generalmente triviales
    if len(text) >= 50:
        score += 15
    elif len(text) >= 30:
        score += 10
    elif len(text) >= 20:
        score += 5
    
    # Criterio 2: Solicitud explícita de recordar (50 puntos) - MÁS PESO
    explicit_memory_keywords = [
        'recuerda', 'memoriza', 'guarda esto', 'guárdalo', 'acuérdate',
        'no olvides', 'quiero conservar', 'esto es importante',
        'mi historia', 'quiero que lo recuerdes', 'graba esto',
    ]
    for keyword in explicit_memory_keywords:
        if keyword in text:
            return 75  # Si hay solicitud explícita, retornar directamente alto
    
    # Criterio 3: Entidades detectadas (hasta 25 puntos) - MÁS PESO
    entity_count = sum(len(entities.get(key, [])) for key in ('personas', 'lugares', 'eventos', 'temas'))
    if entity_count > 0:
        score += min(entity_count * 8, 25)
    
    # Criterio 4: Marcadores personales (hasta 35 puntos) - MÁS PESO
    personal_markers = {
        'mi ': 10, 'mis ': 10, 'me gusta': 14, 'me encanta': 14,
        'prefiero': 14, 'nací': 22, 'viví': 18, 'vivo en': 18,
        'trabajo en': 20, 'trabajo como': 20, 'aprendí': 18, 'estudio': 18,
        'proyecto': 25, 'meta': 18, 'objetivo': 18, 'startup': 22,
        'decisión': 20, 'experiencia': 18, 'recuerdo': 18,
    }
    for marker, points in personal_markers.items():
        if marker in text:
            score += points
    
    # Criterio 5: Palabras de contexto importante (hasta 30 puntos)
    important_keywords = {
        'familia': 20, 'hermano': 20, 'padre': 20, 'madre': 20,
        'amigo': 15, 'relación': 18, 'amor': 20, 'trabajo': 15,
        'carrera': 18, 'salud': 20, 'enfermedad': 20, 'muerte': 25,
        'logro': 20, 'éxito': 18, 'error': 12, 'aprendizaje': 18,
    }
    for keyword, points in important_keywords.items():
        if keyword in text:
            score += points
    
    # Criterio 6: Detectar contenido temporal (penalizar moderadamente)
    temporal_markers = {
        'ahora estoy': -5, 'estoy probando': -8, 'en este momento': -5,
        'hoy quiero': -3, 'solo para': -8, 'temporal': -15,
        'por ahora': -5, 'está siendo': -3,
    }
    for marker, points in temporal_markers.items():
        if marker in text:
            score += points
    
    # Criterio 7: Detectar trivialidad (penalizar fuertemente)
    trivial_phrases = {
        'hola': -50, 'buenos días': -50, 'buenas tardes': -50,
        'gracias': -40, 'ok': -50, 'vale': -50, 'sí': -50, 'no': -50,
        'jaja': -40, 'lol': -40, 'xd': -40, 'qué tal': -50,
        'cómo estás': -50, 'bien y tú': -40, 'muy bien': -30,
    }
    for phrase, points in trivial_phrases.items():
        text_stripped = text.rstrip('!?.,')
        if text_stripped == phrase or (len(text.split()) <= 2 and phrase in text):
            score += points
    
    # Normalizar score entre 0 y 100
    return max(0, min(100, score))


def classify_memory_decision(
    message: str,
    entities: dict,
    importance_score: int
) -> Dict:
    """
    Clasifica el mensaje en una categoría de decisión.
    Retorna: {decision, reason, action}
    """
    text = message.strip().lower()
    
    # 1. Detectar si es información trivial (score < 25)
    if importance_score < 25:
        return {
            'decision': MemoryDecision.TRIVIAL,
            'reason': 'Información casual o de baja relevancia para futuro.',
            'action': MemoryAction.IGNORE
        }
    
    # 2. Detectar si es información temporal (25-59)
    temporal_indicators = [
        'ahora estoy', 'en este momento', 'hoy quiero',
        'estoy probando', 'solo para esta tarea', 'por ahora',
        'está siendo', 'temporal', 'solamente esta vez'
    ]
    if any(indicator in text for indicator in temporal_indicators) and importance_score < 60:
        return {
            'decision': MemoryDecision.TEMPORARY,
            'reason': 'Información útil solo durante la conversación actual.',
            'action': MemoryAction.IGNORE
        }
    
    # 3. Detectar duplicados (información que ya existe en memoria)
    duplicate_check = find_duplicate_memory(message, entities)
    if duplicate_check['is_duplicate']:
        return {
            'decision': MemoryDecision.DUPLICATE,
            'reason': f"Información similar ya existe: {duplicate_check['similar_memory_id']}",
            'action': MemoryAction.IGNORE,
            'similar_memory_id': duplicate_check['similar_memory_id']
        }
    
    # 4. Detectar actualizaciones (modifica una memoria existente)
    update_check = find_memory_to_update(message, entities)
    if update_check['should_update']:
        return {
            'decision': MemoryDecision.UPDATE,
            'reason': 'Nueva información modifica o complementa una memoria existente.',
            'action': MemoryAction.UPDATE,
            'target_memory_id': update_check['target_memory_id'],
            'updated_content': update_check['updated_content']
        }
    
    # 5. Guardar como memoria permanente (score >= 60)
    if importance_score >= 60:
        return {
            'decision': MemoryDecision.MEMORY,
            'reason': f'Información importante/estable con score {importance_score}/100.',
            'action': MemoryAction.CREATE
        }
    
    # 6. Información temporal con valor moderado (25-59)
    if 25 <= importance_score < 60:
        return {
            'decision': MemoryDecision.TEMPORARY,
            'reason': f'Información potencialmente útil pero de naturaleza temporal (score {importance_score}).',
            'action': MemoryAction.IGNORE  # Guardar en short_term_memory, no permanentemente
        }
    
    # Por defecto: trivial
    return {
        'decision': MemoryDecision.TRIVIAL,
        'reason': f'Score insuficiente ({importance_score}/100).',
        'action': MemoryAction.IGNORE
    }


def find_duplicate_memory(message: str, entities: dict) -> Dict:
    """
    Busca si existe una memoria similar (información ya guardada).
    Retorna: {is_duplicate: bool, similar_memory_id: str}
    """
    global memory_index
    
    text = message.strip().lower()
    text_words = set(text.split())
    
    # Buscar memorias similares
    for memory_id, mem_data in memory_index.items():
        existing_text = mem_data['memory']['text'].lower()
        existing_words = set(existing_text.split())
        
        # Calcular similitud (Jaccard)
        if len(text_words) > 0 and len(existing_words) > 0:
            similarity = len(text_words & existing_words) / len(text_words | existing_words)
            if similarity > 0.6:  # Más del 60% similar
                return {
                    'is_duplicate': True,
                    'similar_memory_id': memory_id
                }
    
    return {
        'is_duplicate': False,
        'similar_memory_id': None
    }


def find_memory_to_update(message: str, entities: dict) -> Dict:
    """
    Detecta si la nueva información debería actualizar una memoria existente.
    Retorna: {should_update: bool, target_memory_id: str, updated_content: str}
    """
    global memory_index
    
    text = message.strip().lower()
    
    # Palabras que indican actualización ("ahora también", "además", "pero")
    update_indicators = [
        'ahora también', 'además', 'pero ahora', 'también estoy',
        'luego', 'después', 'cambié a', 'pasé a', 'actualicé',
        'ya no', 'cambié de opinión', 'modificó', 'mejoró'
    ]
    
    has_update_indicator = any(indicator in text for indicator in update_indicators)
    
    if has_update_indicator:
        # Buscar memoria relacionada
        for memory_id, mem_data in memory_index.items():
            existing_text = mem_data['memory']['text'].lower()
            
            # Si hay palabras clave similares, es candidata a actualización
            existing_keywords = set(existing_text.split()[:10])  # Primeras 10 palabras
            new_keywords = set(text.split()[:10])
            
            common = existing_keywords & new_keywords
            if len(common) >= 2:  # Al menos 2 palabras en común
                return {
                    'should_update': True,
                    'target_memory_id': memory_id,
                    'updated_content': f"{mem_data['memory']['text']} Actualización: {message}"
                }
    
    return {
        'should_update': False,
        'target_memory_id': None,
        'updated_content': None
    }


def evaluate_message(message: str) -> Dict:
    """
    FUNCIÓN PRINCIPAL: Evalúa un mensaje y retorna decisión de memoria estructurada.
    
    Retorna:
    {
        'decision': 'MEMORY' | 'TEMPORARY' | 'TRIVIAL' | 'DUPLICATE' | 'UPDATE',
        'importance': 0-100,
        'reason': str,
        'memory': str (contenido si se guarda) | null,
        'action': 'CREATE' | 'UPDATE' | 'IGNORE',
        'similar_memory_id': str (si es DUPLICATE),
        'target_memory_id': str (si es UPDATE),
    }
    """
    entities = extract_entities(message)
    importance_score = calculate_memory_score(message, entities)
    classification = classify_memory_decision(message, entities, importance_score)
    
    result = {
        'decision': classification['decision'].value,
        'importance': importance_score,
        'reason': classification['reason'],
        'memory': message if classification['action'].value == 'CREATE' else None,
        'action': classification['action'].value,
        'entities': entities,
        'timestamp': datetime.now().isoformat()
    }
    
    # Agregar campos específicos según el tipo
    if 'similar_memory_id' in classification:
        result['similar_memory_id'] = classification['similar_memory_id']
    if 'target_memory_id' in classification:
        result['target_memory_id'] = classification['target_memory_id']
        result['updated_content'] = classification.get('updated_content')
    
    return result


def should_store_memory(message: str, entities: dict = None) -> bool:
    """Wrapper de compatibilidad: retorna bool en lugar de diccionario."""
    if entities is None:
        entities = extract_entities(message)
    
    evaluation = evaluate_message(message)
    return evaluation['action'] == 'CREATE'


def update_categories(message: str):
    """
    Actualiza el sistema de categorías dinámicas con nueva información.
    Usa la evaluación inteligente: solo guarda si importancia >= 70 y action == CREATE.
    """
    global dynamic_categories, memory_index
    
    # Inicializar categorías principales si no existen
    if not dynamic_categories:
        dynamic_categories = {
            'Personal': {'icon': '👤', 'color': '#3b82f6', 'subcategories': {}, 'count': 0},
            'Trabajo': {'icon': '💼', 'color': '#ef4444', 'subcategories': {}, 'count': 0},
            'Familia': {'icon': '👨‍👩‍👧‍👦', 'color': '#ec4899', 'subcategories': {}, 'count': 0},
            'Lugares': {'icon': '🏠', 'color': '#10b981', 'subcategories': {}, 'count': 0},
            'Eventos': {'icon': '🎂', 'color': '#f59e0b', 'subcategories': {}, 'count': 0},
            'Emociones': {'icon': '💭', 'color': '#8b5cf6', 'subcategories': {}, 'count': 0}
        }
    
    # Evaluar mensaje con sistema inteligente
    evaluation = evaluate_message(message)
    
    # Solo procesar si se debe crear memoria (action == CREATE)
    if evaluation['action'] != 'CREATE':
        # Si es TEMPORARY, guardar en short_term_memory
        if evaluation['decision'] == MemoryDecision.TEMPORARY.value:
            temp_id = str(uuid.uuid4())
            short_term_memory[temp_id] = {
                'id': temp_id,
                'content': message,
                'importance': evaluation['importance'],
                'expires': 'session_end',
                'timestamp': evaluation['timestamp']
            }
        return evaluation
    
    entities = evaluation['entities']
    
def update_categories(message: str):
    """
    Actualiza el sistema de categorías dinámicas con nueva información.
    Usa la evaluación inteligente: solo guarda si importancia >= 70 y action == CREATE.
    """
    global dynamic_categories, memory_index
    
    # Inicializar categorías principales si no existen
    if not dynamic_categories:
        dynamic_categories = {
            'Personal': {'icon': '👤', 'color': '#3b82f6', 'subcategories': {}, 'count': 0},
            'Trabajo': {'icon': '💼', 'color': '#ef4444', 'subcategories': {}, 'count': 0},
            'Familia': {'icon': '👨‍👩‍👧‍👦', 'color': '#ec4899', 'subcategories': {}, 'count': 0},
            'Lugares': {'icon': '🏠', 'color': '#10b981', 'subcategories': {}, 'count': 0},
            'Eventos': {'icon': '🎂', 'color': '#f59e0b', 'subcategories': {}, 'count': 0},
            'Emociones': {'icon': '💭', 'color': '#8b5cf6', 'subcategories': {}, 'count': 0}
        }
    
    # Evaluar mensaje con sistema inteligente
    evaluation = evaluate_message(message)
    
    # Solo procesar si se debe crear memoria (action == CREATE)
    if evaluation['action'] != 'CREATE':
        # Si es TEMPORARY, guardar en short_term_memory
        if evaluation['decision'] == MemoryDecision.TEMPORARY.value:
            temp_id = str(uuid.uuid4())
            short_term_memory[temp_id] = {
                'id': temp_id,
                'content': message,
                'importance': evaluation['importance'],
                'expires': 'session_end',
                'timestamp': evaluation['timestamp']
            }
        return evaluation
    
    entities = evaluation['entities']
    
    # Crear objeto de memoria con timestamp e ID único
    timestamp = datetime.now()
    memory_id = str(uuid.uuid4())
    memory_obj = {
        'id': memory_id,
        'text': message,
        'short_text': message[:60] + ('...' if len(message) > 60 else ''),
        'timestamp': timestamp.isoformat(),
        'date': timestamp.strftime('%d/%m/%Y'),
        'time': timestamp.strftime('%H:%M:%S'),
        'importance': evaluation['importance'],  # Guardar score
        'important': evaluation['importance'] >= 80,  # Marcar si es muy importante
        'expires_at': None,
        'reminder': None,
        'archived': False
    }
    
    # Variable para rastrear si se clasificó en alguna categoría
    classified = False
    
    # Detectar si es TRABAJO
    text_lower = message.lower()
    trabajo_keywords = ['trabajo', 'proyecto', 'reunión', 'junta', 'oficina', 'jefe', 
                        'compañero', 'cliente', 'presentación', 'informe', 'tarea laboral',
                        'empresa', 'negocio', 'empleo']
    
    if any(kw in text_lower for kw in trabajo_keywords):
        subcategoria = 'General'
        if 'reunión' in text_lower or 'junta' in text_lower:
            subcategoria = 'Reuniones'
        elif 'proyecto' in text_lower:
            subcategoria = 'Proyectos'
        elif 'cliente' in text_lower:
            subcategoria = 'Clientes'
        
        if subcategoria not in dynamic_categories['Trabajo']['subcategories']:
            dynamic_categories['Trabajo']['subcategories'][subcategoria] = {
                'icon': '📋', 'memories': [], 'count': 0
            }
        dynamic_categories['Trabajo']['subcategories'][subcategoria]['memories'].append(memory_obj)
        dynamic_categories['Trabajo']['subcategories'][subcategoria]['count'] += 1
        dynamic_categories['Trabajo']['count'] += 1
        memory_index[memory_id] = {'category': 'Trabajo', 'subcategory': subcategoria, 'memory': memory_obj}
        classified = True
    
    # Actualizar Familia (personas)
    if entities['personas']:
        for persona in entities['personas']:
            nombre = persona['name']
            if nombre not in dynamic_categories['Familia']['subcategories']:
                dynamic_categories['Familia']['subcategories'][nombre] = {
                    'icon': persona['icon'], 'memories': [], 'count': 0
                }
            dynamic_categories['Familia']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Familia']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Familia']['count'] += 1
            memory_index[memory_id] = {'category': 'Familia', 'subcategory': nombre, 'memory': memory_obj}
            classified = True
    
    # Actualizar Lugares
    if entities['lugares']:
        for lugar in entities['lugares']:
            nombre = lugar['name']
            if nombre not in dynamic_categories['Lugares']['subcategories']:
                dynamic_categories['Lugares']['subcategories'][nombre] = {
                    'icon': lugar['icon'], 'memories': [], 'count': 0
                }
            dynamic_categories['Lugares']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Lugares']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Lugares']['count'] += 1
            memory_index[memory_id] = {'category': 'Lugares', 'subcategory': nombre, 'memory': memory_obj}
            classified = True
    
    # Actualizar Eventos
    if entities['eventos']:
        for evento in entities['eventos']:
            nombre = evento['name']
            if nombre not in dynamic_categories['Eventos']['subcategories']:
                dynamic_categories['Eventos']['subcategories'][nombre] = {
                    'icon': evento['icon'], 'memories': [], 'count': 0
                }
            dynamic_categories['Eventos']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Eventos']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Eventos']['count'] += 1
            memory_index[memory_id] = {'category': 'Eventos', 'subcategory': nombre, 'memory': memory_obj}
            classified = True
    
    # Actualizar Emociones/Temas
    if entities['temas']:
        for tema in entities['temas']:
            nombre = tema['name']
            if nombre not in dynamic_categories['Emociones']['subcategories']:
                dynamic_categories['Emociones']['subcategories'][nombre] = {
                    'icon': tema['icon'], 'memories': [], 'count': 0
                }
            dynamic_categories['Emociones']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Emociones']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Emociones']['count'] += 1
            memory_index[memory_id] = {'category': 'Emociones', 'subcategory': nombre, 'memory': memory_obj}
            classified = True
    
    # Si no se clasificó en ninguna categoría específica, agregar a Personal/General
    if not classified:
        subcategoria = 'Notas Generales'
        if subcategoria not in dynamic_categories['Personal']['subcategories']:
            dynamic_categories['Personal']['subcategories'][subcategoria] = {
                'icon': '📝', 'memories': [], 'count': 0
            }
        dynamic_categories['Personal']['subcategories'][subcategoria]['memories'].append(memory_obj)
        dynamic_categories['Personal']['subcategories'][subcategoria]['count'] += 1
        dynamic_categories['Personal']['count'] += 1
        memory_index[memory_id] = {'category': 'Personal', 'subcategory': subcategoria, 'memory': memory_obj}
    
    return evaluation


def get_category_summary():
    """Retorna un resumen de todas las categorías y subcategorías aprendidas"""
    summary = {
        'total_categories': len(dynamic_categories),
        'total_subcategories': sum(len(cat['subcategories']) for cat in dynamic_categories.values()),
        'categories': []
    }
    
    for cat_name, cat_data in dynamic_categories.items():
        cat_summary = {
            'name': cat_name,
            'icon': cat_data['icon'],
            'color': cat_data['color'],
            'count': cat_data['count'],
            'subcategories': []
        }
        
        for subcat_name, subcat_data in cat_data['subcategories'].items():
            cat_summary['subcategories'].append({
                'name': subcat_name,
                'icon': subcat_data['icon'],
                'count': subcat_data['count'],
                'sample_memories': subcat_data['memories'][:3]  # Primeras 3 memorias
            })
        
        summary['categories'].append(cat_summary)
    
    return summary


# ===== GESTIÓN DE MEMORIAS =====

def delete_memory(memory_id: str):
    """Elimina una memoria por completo del sistema"""
    global memory_index, dynamic_categories
    
    if memory_id not in memory_index:
        return {'success': False, 'message': 'Memoria no encontrada'}
    
    mem_data = memory_index[memory_id]
    category = mem_data['category']
    subcategory = mem_data['subcategory']
    
    # Eliminar de la subcategoría
    if category in dynamic_categories and subcategory in dynamic_categories[category]['subcategories']:
        memories = dynamic_categories[category]['subcategories'][subcategory]['memories']
        dynamic_categories[category]['subcategories'][subcategory]['memories'] = [
            m for m in memories if m.get('id') != memory_id
        ]
        dynamic_categories[category]['subcategories'][subcategory]['count'] -= 1
        dynamic_categories[category]['count'] -= 1
    
    # Eliminar del índice
    del memory_index[memory_id]
    
    # Eliminar comentarios asociados
    if memory_id in memory_threads:
        del memory_threads[memory_id]
    
    return {'success': True, 'message': 'Memoria eliminada'}


def update_memory_importance(memory_id: str, is_important: bool):
    """Marca o desmarca una memoria como importante"""
    global memory_index
    
    if memory_id not in memory_index:
        return {'success': False, 'message': 'Memoria no encontrada'}
    
    memory_index[memory_id]['memory']['important'] = is_important
    
    return {
        'success': True,
        'message': f'Memoria marcada como {"importante" if is_important else "normal"}',
        'memory': memory_index[memory_id]['memory']
    }


def set_memory_reminder(memory_id: str, reminder_date: str, reminder_message: str = None):
    """Establece un recordatorio para una memoria"""
    from datetime import datetime
    global memory_index
    
    if memory_id not in memory_index:
        return {'success': False, 'message': 'Memoria no encontrada'}
    
    try:
        # Validar formato de fecha
        datetime.fromisoformat(reminder_date)
        
        memory_index[memory_id]['memory']['reminder'] = {
            'date': reminder_date,
            'message': reminder_message or memory_index[memory_id]['memory']['text']
        }
        
        return {
            'success': True,
            'message': 'Recordatorio establecido',
            'memory': memory_index[memory_id]['memory']
        }
    except ValueError:
        return {'success': False, 'message': 'Formato de fecha inválido'}


def get_reminders():
    """Obtiene todos los recordatorios pendientes"""
    from datetime import datetime
    global memory_index
    
    now = datetime.now()
    reminders = []
    
    for memory_id, mem_data in memory_index.items():
        memory = mem_data['memory']
        if memory.get('reminder'):
            reminder_date = datetime.fromisoformat(memory['reminder']['date'])
            if reminder_date <= now:
                reminders.append({
                    'id': memory_id,
                    'text': memory['text'],
                    'reminder_message': memory['reminder']['message'],
                    'reminder_date': memory['reminder']['date'],
                    'category': mem_data['category'],
                    'subcategory': mem_data['subcategory']
                })
    
    return reminders


def set_memory_expiration(memory_id: str, expires_at: str):
    """Establece fecha de caducidad para una memoria"""
    from datetime import datetime
    global memory_index
    
    if memory_id not in memory_index:
        return {'success': False, 'message': 'Memoria no encontrada'}
    
    try:
        # Validar formato de fecha
        datetime.fromisoformat(expires_at)
        
        memory_index[memory_id]['memory']['expires_at'] = expires_at
        
        return {
            'success': True,
            'message': 'Fecha de caducidad establecida',
            'memory': memory_index[memory_id]['memory']
        }
    except ValueError:
        return {'success': False, 'message': 'Formato de fecha inválido'}


def get_expired_memories():
    """Obtiene memorias que ya caducaron"""
    from datetime import datetime
    global memory_index
    
    now = datetime.now()
    expired = []
    
    for memory_id, mem_data in memory_index.items():
        memory = mem_data['memory']
        if memory.get('expires_at'):
            expiry_date = datetime.fromisoformat(memory['expires_at'])
            if expiry_date <= now and not memory.get('archived'):
                expired.append({
                    'id': memory_id,
                    'text': memory['text'],
                    'expires_at': memory['expires_at'],
                    'category': mem_data['category'],
                    'subcategory': mem_data['subcategory']
                })
    
    return expired


def cleanup_expired_memories():
    """Archiva (no elimina) memorias caducadas"""
    from datetime import datetime
    global memory_index
    
    now = datetime.now()
    archived_count = 0
    
    for memory_id, mem_data in memory_index.items():
        memory = mem_data['memory']
        if memory.get('expires_at') and not memory.get('archived'):
            expiry_date = datetime.fromisoformat(memory['expires_at'])
            if expiry_date <= now:
                memory['archived'] = True
                archived_count += 1
    
    return {
        'success': True,
        'message': f'{archived_count} memorias archivadas',
        'archived_count': archived_count
    }


def get_memory_by_id(memory_id: str):
    """Obtiene una memoria específica por ID"""
    global memory_index
    
    if memory_id not in memory_index:
        return None
    
    mem_data = memory_index[memory_id]
    return {
        'id': memory_id,
        **mem_data['memory'],
        'category': mem_data['category'],
        'subcategory': mem_data['subcategory']
    }

