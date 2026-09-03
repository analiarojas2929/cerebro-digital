"""
Sistema de Aprendizaje Dinámico de Categorías
Extrae automáticamente personas, lugares, eventos y temas de las conversaciones
"""
import uuid

# Almacenamiento de categorías dinámicas
dynamic_categories = {}

# Sistema de hilos de conversación (comentarios sobre memorias)
memory_threads = {}  # ID de memoria → lista de comentarios

# Índice de memorias por ID para acceso rápido
memory_index = {}  # ID → {category, subcategory, memory_obj}

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


def should_store_memory(message: str, entities: dict) -> bool:
    """Solo guarda contenido personal, relevante o marcado explícitamente como recuerdo."""
    text = message.strip().lower()
    if len(text) < 12:
        return False

    transient_phrases = {
        'hola', 'buenos días', 'buenas tardes', 'buenas noches',
        'gracias', 'ok', 'vale', 'sí', 'no', 'qué tal', 'cómo estás',
    }
    if text.rstrip('!?.,') in transient_phrases:
        return False

    explicit_memory = (
        'recuerda', 'memoriza', 'guarda esto', 'no olvides',
        'quiero conservar', 'esto es importante', 'mi historia',
    )
    if any(phrase in text for phrase in explicit_memory):
        return True

    if any(entities.get(key) for key in ('personas', 'lugares', 'eventos', 'temas')):
        return True

    personal_markers = (
        'mi ', 'mis ', 'me gusta', 'me encanta', 'prefiero',
        'nací', 'viví', 'vivo en', 'trabajo en', 'aprendí',
        'hoy ', 'ayer ', 'mañana ', 'siento ', 'estoy ',
    )
    return len(text) >= 28 and any(marker in text for marker in personal_markers)


def update_categories(message: str):
    """Actualiza el sistema de categorías dinámicas con la nueva información"""
    from datetime import datetime
    global dynamic_categories
    
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
    
    # Extraer entidades del mensaje
    entities = extract_entities(message)

    if not should_store_memory(message, entities):
        return entities
    
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
        'important': False,  # Nuevo: marcar como importante
        'expires_at': None,  # Nuevo: fecha de caducidad (opcional)
        'reminder': None,    # Nuevo: recordatorio (fecha + mensaje)
        'archived': False    # Nuevo: archivada pero no eliminada
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
        # Intentar detectar subcategoría más específica
        if 'reunión' in text_lower or 'junta' in text_lower:
            subcategoria = 'Reuniones'
        elif 'proyecto' in text_lower:
            subcategoria = 'Proyectos'
        elif 'cliente' in text_lower:
            subcategoria = 'Clientes'
        
        if subcategoria not in dynamic_categories['Trabajo']['subcategories']:
            dynamic_categories['Trabajo']['subcategories'][subcategoria] = {
                'icon': '📋',
                'memories': [],
                'count': 0
            }
        dynamic_categories['Trabajo']['subcategories'][subcategoria]['memories'].append(memory_obj)
        dynamic_categories['Trabajo']['subcategories'][subcategoria]['count'] += 1
        dynamic_categories['Trabajo']['count'] += 1
        memory_index[memory_id] = {
            'category': 'Trabajo',
            'subcategory': subcategoria,
            'memory': memory_obj
        }
        classified = True
    
    # Actualizar subcategorías de Familia (personas)
    if entities['personas']:
        for persona in entities['personas']:
            nombre = persona['name']
            if nombre not in dynamic_categories['Familia']['subcategories']:
                dynamic_categories['Familia']['subcategories'][nombre] = {
                    'icon': persona['icon'],
                    'memories': [],
                    'count': 0
                }
            dynamic_categories['Familia']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Familia']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Familia']['count'] += 1
            
            # Actualizar índice
            memory_index[memory_id] = {
                'category': 'Familia',
                'subcategory': nombre,
                'memory': memory_obj
            }
            classified = True
    
    # Actualizar Lugares
    if entities['lugares']:
        for lugar in entities['lugares']:
            nombre = lugar['name']
            if nombre not in dynamic_categories['Lugares']['subcategories']:
                dynamic_categories['Lugares']['subcategories'][nombre] = {
                    'icon': lugar['icon'],
                    'memories': [],
                    'count': 0
                }
            dynamic_categories['Lugares']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Lugares']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Lugares']['count'] += 1
            
            memory_index[memory_id] = {
                'category': 'Lugares',
                'subcategory': nombre,
                'memory': memory_obj
            }
            classified = True
    
    # Actualizar Eventos
    if entities['eventos']:
        for evento in entities['eventos']:
            nombre = evento['name']
            if nombre not in dynamic_categories['Eventos']['subcategories']:
                dynamic_categories['Eventos']['subcategories'][nombre] = {
                    'icon': evento['icon'],
                    'memories': [],
                    'count': 0
                }
            dynamic_categories['Eventos']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Eventos']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Eventos']['count'] += 1
            
            memory_index[memory_id] = {
                'category': 'Eventos',
                'subcategory': nombre,
                'memory': memory_obj
            }
            classified = True
    
    # Actualizar Emociones/Temas
    if entities['temas']:
        for tema in entities['temas']:
            nombre = tema['name']
            if nombre not in dynamic_categories['Emociones']['subcategories']:
                dynamic_categories['Emociones']['subcategories'][nombre] = {
                    'icon': tema['icon'],
                    'memories': [],
                    'count': 0
                }
            dynamic_categories['Emociones']['subcategories'][nombre]['memories'].append(memory_obj)
            dynamic_categories['Emociones']['subcategories'][nombre]['count'] += 1
            dynamic_categories['Emociones']['count'] += 1
            
            memory_index[memory_id] = {
                'category': 'Emociones',
                'subcategory': nombre,
                'memory': memory_obj
            }
            classified = True
    
    # Si no se clasificó en ninguna categoría específica, agregar a Personal/General
    if not classified:
        subcategoria = 'Notas Generales'
        if subcategoria not in dynamic_categories['Personal']['subcategories']:
            dynamic_categories['Personal']['subcategories'][subcategoria] = {
                'icon': '📝',
                'memories': [],
                'count': 0
            }
        dynamic_categories['Personal']['subcategories'][subcategoria]['memories'].append(memory_obj)
        dynamic_categories['Personal']['subcategories'][subcategoria]['count'] += 1
        dynamic_categories['Personal']['count'] += 1
        memory_index[memory_id] = {
            'category': 'Personal',
            'subcategory': subcategoria,
            'memory': memory_obj
        }
    
    return entities


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

