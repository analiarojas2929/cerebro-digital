from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
import uvicorn
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from auth import (
    User, UserCreate, UserInDB, UserLogin, Token,
    ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token,
    create_user, get_current_user, get_user_session, initialize_demo_users,
)
from datetime import timedelta

# Cargar variables de entorno
load_dotenv()

# Importar sistema de aprendizaje dinámico
import dynamic_learning
from dynamic_learning import (
    update_categories, get_category_summary,
    delete_memory, update_memory_importance, set_memory_reminder,
    get_reminders, set_memory_expiration, get_expired_memories,
    cleanup_expired_memories, get_memory_by_id
)

# Importar conversación con IA
try:
    from ai_chat import generate_ai_response, initialize_openai
    AI_AVAILABLE = True
    # Intentar inicializar OpenAI
    initialize_openai()
except Exception as e:
    print(f"⚠️  IA no disponible: {e}")
    print("    Sistema funcionará sin conversación inteligente")
    AI_AVAILABLE = False

# Aplicación
app = FastAPI(title="Cerebro Digital Simple", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_demo_users()

async def current_user(authorization: Optional[str] = Header(None)) -> UserInDB:
    if not authorization:
        raise HTTPException(status_code=401, detail="No autenticado")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Header de autorización inválido")
    user = get_current_user(parts[1])
    if user is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return user

@contextmanager
def user_learning_storage(user_id: str):
    """Conecta el motor existente a la sesión del usuario durante una operación."""
    session = get_user_session(user_id)
    previous = (
        dynamic_learning.dynamic_categories,
        dynamic_learning.memory_threads,
        dynamic_learning.memory_index,
    )
    dynamic_learning.dynamic_categories = session["dynamic_categories"]
    dynamic_learning.memory_threads = session["memory_threads"]
    dynamic_learning.memory_index = session["memory_index"]
    try:
        yield session
    finally:
        session["dynamic_categories"] = dynamic_learning.dynamic_categories
        session["memory_threads"] = dynamic_learning.memory_threads
        session["memory_index"] = dynamic_learning.memory_index
        (
            dynamic_learning.dynamic_categories,
            dynamic_learning.memory_threads,
            dynamic_learning.memory_index,
        ) = previous

# Modelos
class MessageInput(BaseModel):
    message: str
    session_id: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    session_id: str
    category: str = "general"
    confidence: float = 0.5
    related_memories: List = []

# Storage
conversations = []

@app.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    try:
        user = create_user(user_data)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    token = create_access_token(
        {"sub": user.username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token, token_type="bearer", user_info=user.dict())

@app.post("/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = create_access_token(
        {"sub": user.username},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token, token_type="bearer", user_info=user.dict())

@app.get("/auth/me", response_model=User)
async def me(user: UserInDB = Depends(current_user)):
    return User(**user.dict(exclude={"hashed_password", "user_id", "created_at"}))

# Rutas
@app.get("/")
async def root():
    return {
        "name": "Cerebro Digital - FUNCIONANDO ✅",
        "status": "operational",
        "message": "¡Backend corriendo correctamente!"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat/message")
async def send_message(msg: MessageInput, user: UserInDB = Depends(current_user)):
    sid = msg.session_id or str(uuid.uuid4())
    text = msg.message.lower()
    
    # APRENDIZAJE DINÁMICO - Extraer y almacenar categorías automáticamente
    with user_learning_storage(user.user_id) as user_session:
        entities_found = update_categories(msg.message)
    
    # Clasificación simple
    if 'trabajo' in text or 'proyecto' in text:
        cat, conf = "trabajo",  0.8
    elif 'python' in text or 'código' in text:
        cat, conf = "tecnología", 0.8
    elif 'familia' in text or 'personal' in text or entities_found['personas']:
        cat, conf = "familia", 0.9
    else:
        cat, conf = "general", 0.5
    
    # ==== CONVERSACIÓN CON IA ====
    if AI_AVAILABLE:
        try:
            # Obtener historial de esta sesión
            session_history = [
                {
                    "role": "user" if i % 2 == 0 else "assistant",
                    "content": c["user"] if i % 2 == 0 else c["bot"]
                }
                for i, c in enumerate([conv for conv in user_session["conversations"] if conv.get("session") == sid][-10:])
            ]
            
            # Convertir categorías dinámicas a memorias
            memories = []
            for category_name, category_data in user_session["dynamic_categories"].items():
                for subcat_name, subcat_data in category_data.get('subcategories', {}).items():
                    for memory in subcat_data.get('memories', []):
                        memories.append({
                            'content': memory.get('text', ''),
                            'category': category_name,
                            'subcategory': subcat_name
                        })
            
            # Generar respuesta con IA
            resp = generate_ai_response(msg.message, session_history, memories)
            
            # Agregar información de entidades si se encontraron
            if entities_found['personas'] or entities_found['lugares'] or entities_found['eventos']:
                extras = []
                if entities_found['personas']:
                    extras.append(f"👥 {', '.join([p['name'] for p in entities_found['personas']])}")
                if entities_found['lugares']:
                    extras.append(f"📍 {', '.join([l['name'] for l in entities_found['lugares']])}")
                if entities_found['eventos']:
                    extras.append(f"🎉 {', '.join([e['name'] for e in entities_found['eventos']])}")
                
                resp += f"\n\n{' | '.join(extras)}"
        
        except Exception as e:
            print(f"❌ Error con IA: {e}")
            # Fallback a respuesta básica
            resp = "¡Entendido! He guardado esta información."
    
    # ==== RESPUESTA BÁSICA (sin IA) ====
    else:
        resp_parts = []
        if entities_found['personas']:
            resp_parts.append(f"📝 Personas: {', '.join([p['name'] for p in entities_found['personas']])}")
        if entities_found['lugares']:
            resp_parts.append(f"📍 Lugares: {', '.join([l['name'] for l in entities_found['lugares']])}")
        if entities_found['eventos']:
            resp_parts.append(f"🎉 Eventos: {', '.join([e['name'] for e in entities_found['eventos']])}")
        
        if resp_parts:
            resp = "¡Entendido! " + " | ".join(resp_parts)
        else:
            # Respuestas simples
            if 'hola' in text:
                resp = "¡Hola! Soy tu Cerebro Digital. ¿Cómo puedo ayudarte?"
            elif 'cómo estás' in text:
                resp = f"¡Funcionando perfectamente! Tu mensaje es sobre '{cat}'"
            else:
                resp = f"Mensaje guardado como '{cat}'"
    
    # Guardar en historial
    user_session["conversations"].append({
        "session": sid,
        "user": msg.message,
        "bot": resp,
        "category": cat
    })
    
    return MessageResponse(
        response=resp,
        session_id=sid,
        category=cat,
        confidence=conf
    )

@app.get("/memory/stats")
async def stats(user: UserInDB = Depends(current_user)):
    user_session = get_user_session(user.user_id)
    cats = {}
    for c in user_session["conversations"]:
        cat = c.get("category", "general")
        cats[cat] = cats.get(cat, 0) + 1
    
    return {
        "total_conversations": len(user_session["conversations"]),
        "total_memories": len(user_session["conversations"]),
        "categories": [{"name": k, "count": v} for k, v in cats.items()]
    }

@app.get("/memory/categories")
async def categories(user: UserInDB = Depends(current_user)):
    """Retorna las categorías dinámicas aprendidas del sistema"""
    categories_list = []
    
    user_session = get_user_session(user.user_id)
    for cat_name, cat_data in user_session["dynamic_categories"].items():
        categories_list.append({
            "id": len(categories_list) + 1,
            "name": cat_name.lower(),
            "icon": cat_data.get('icon', '📁'),
            "color": cat_data.get('color', '#888888'),
            "keywords": list(cat_data.get('subcategories', {}).keys())[:4],
            "conversation_count": cat_data.get('count', 0)
        })
    
    return categories_list

@app.get("/memory/neural-graph")
async def neural_graph(user: UserInDB = Depends(current_user)):
    """Genera red neuronal HORIZONTAL con comentarios como capas adicionales"""
    import random
    with user_learning_storage(user.user_id) as user_session:
        learned_data = get_category_summary()
        memory_threads = user_session["memory_threads"]
    
    nodes = []
    links = []
    unique_memories = {}  # Diccionario para evitar duplicados: {memory_id: node_data}
    
    # CAPA 0: Categorías principales (izquierda)
    for idx, cat_data in enumerate(learned_data['categories']):
        cat_id = cat_data['name'].lower().replace(' ', '_')
        nodes.append({
            "id": cat_id,
            "name": f"{cat_data.get('icon', '📁')} {cat_data.get('name', 'Sin nombre')}",
            "color": cat_data.get('color', '#888888'),
            "layer": 0,
            "val": 15
        })
        
        # CAPA 1: Subcategorías
        for subcat in cat_data.get('subcategories', []):
            subcat_name = subcat.get('name', 'Sin nombre')
            subcat_id = f"{cat_id}_{subcat_name.lower().replace(' ', '_')}"
            nodes.append({
                "id": subcat_id,
                "name": f"{subcat.get('icon', '📌')} {subcat_name}",
                "color": cat_data.get('color', '#888888'),
                "layer": 1,
                "val": 12
            })
            
            # Conexión: Categoría → Subcategoría
            links.append({
                "source": cat_id,
                "target": subcat_id,
                "value": 5,
                "color": cat_data.get('color', '#888888') + "60"
            })
            
            # CAPA 2: Memorias originales (sin duplicados)
            sample_mems = subcat.get('sample_memories', [])
            
            for mem_idx, memory_data in enumerate(sample_mems):
                # Usar ID real de la memoria si existe
                if isinstance(memory_data, dict) and 'id' in memory_data:
                    mem_id = memory_data['id']
                else:
                    # Fallback para memorias antiguas sin ID
                    mem_id = f"mem_{subcat_id}_{mem_idx}"
                
                # Si la memoria ya existe, solo conectarla a esta subcategoría
                if mem_id in unique_memories:
                    # Solo crear link desde subcategoría a memoria existente
                    links.append({
                        "source": subcat_id,
                        "target": mem_id,
                        "value": 4,
                        "color": cat_data.get('color', '#888888') + "50"
                    })
                    continue  # Saltar creación de nodo, ya existe
                
                # Crear nodo de memoria por primera vez
                if isinstance(memory_data, dict):
                    mem_name = memory_data.get('short_text', 'Memoria')
                    full_text = memory_data.get('text', '')
                    mem_date = memory_data.get('date', '')
                    mem_time = memory_data.get('time', '')
                    is_important = memory_data.get('important', False)
                    has_reminder = memory_data.get('reminder') is not None
                    is_archived = memory_data.get('archived', False)
                else:
                    mem_name = str(memory_data)[:25] + '...' if len(str(memory_data)) > 25 else str(memory_data)
                    full_text = str(memory_data)
                    mem_date = ''
                    mem_time = ''
                    is_important = False
                    has_reminder = False
                    is_archived = False
                
                # Modificar nombre si es importante o tiene recordatorio
                display_name = mem_name
                if is_important:
                    display_name = f"⭐ {mem_name}"
                if has_reminder:
                    display_name = f"🔔 {display_name}"
                if is_archived:
                    display_name = f"📦 {display_name}"
                
                memory_node = {
                    "id": mem_id,
                    "name": display_name,
                    "color": cat_data.get('color', '#888888'),
                    "layer": 2,
                    "val": 15 if is_important else 10,
                    "full_text": full_text,
                    "date": mem_date,
                    "time": mem_time,
                    "category": cat_data.get('name', ''),
                    "subcategory": subcat_name,
                    "type": "memory",
                    "important": is_important,
                    "has_reminder": has_reminder,
                    "archived": is_archived
                }
                
                nodes.append(memory_node)
                unique_memories[mem_id] = memory_node  # Registrar como creado
                
                # Conexión: Subcategoría → Memoria
                links.append({
                    "source": subcat_id,
                    "target": mem_id,
                    "value": 4,
                    "color": cat_data.get('color', '#888888') + "50"
                })
                
                # CAPAS 3+: Comentarios sobre esta memoria (solo procesar una vez por memoria)
                thread = memory_threads.get(mem_id, [])
                prev_id = mem_id
                for comment in thread:
                    comment_id = comment['id']
                    comment_layer = comment.get('layer', 3)
                    
                    nodes.append({
                        "id": comment_id,
                        "name": comment['text'][:30] + '...' if len(comment['text']) > 30 else comment['text'],
                        "color": "#a855f7",  # Morado para comentarios
                        "layer": comment_layer,
                        "val": 8,
                        "full_text": comment['text'],
                        "date": comment.get('date', ''),
                        "time": comment.get('time', ''),
                        "user": comment.get('user', 'Usuario'),
                        "type": "comment",
                        "parent_memory": mem_id
                    })
                    
                    # Conexión: Memoria/Comentario anterior → Comentario nuevo
                    links.append({
                        "source": prev_id,
                        "target": comment_id,
                        "value": 3,
                        "color": "#a855f780"
                    })
                    
                    prev_id = comment_id
    
    stats = {
        "total_nodes": len(nodes),
        "total_connections": len(links),
        "max_layer": max([n['layer'] for n in nodes]) if nodes else 0
    }
    
    return {"nodes": nodes, "links": links, "stats": stats}

@app.get("/memory/learned-categories")
async def get_learned_categories(user: UserInDB = Depends(current_user)):
    """Retorna las categorías y subcategorías que el sistema ha aprendido automáticamente"""
    with user_learning_storage(user.user_id):
        summary = get_category_summary()
    return summary

@app.get("/memory/memories")
async def get_memories(limit: int = 50, category: Optional[str] = None, user: UserInDB = Depends(current_user)):
    """Obtiene las memorias recientes"""
    from datetime import datetime
    
    user_conversations = get_user_session(user.user_id)["conversations"]
    filtered = user_conversations
    if category:
        filtered = [c for c in conversations if c.get("category") == category]
    
    # Ordenar por más reciente primero y limitar
    result = []
    for idx, conv in enumerate(reversed(filtered[-limit:])):
        result.append({
            "id": idx,
            "content": conv.get("user", ""),
            "message": conv.get("user", ""),
            "category": conv.get("category", "general"),
            "timestamp": datetime.now().isoformat(),
            "session_id": conv.get("session", ""),
        })
    
    return result

# === SISTEMA DE COMENTARIOS/HILOS ===

class CommentInput(BaseModel):
    memory_id: str
    comment: str
    user: Optional[str] = "Usuario"

@app.post("/memory/comment")
async def add_memory_comment(input: CommentInput, user: UserInDB = Depends(current_user)):
    """Agrega un comentario a una memoria existente"""
    from dynamic_learning import add_comment_to_memory
    
    try:
        with user_learning_storage(user.user_id):
            comment_obj = add_comment_to_memory(input.memory_id, input.comment, input.user)
        return {
            "success": True,
            "comment": comment_obj,
            "message": "Comentario agregado exitosamente"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/memory/thread/{memory_id}")
async def get_memory_thread(memory_id: str, user: UserInDB = Depends(current_user)):
    """Obtiene el hilo completo de comentarios de una memoria"""
    from dynamic_learning import get_memory_thread
    
    with user_learning_storage(user.user_id):
        thread = get_memory_thread(memory_id)
    return {
        "memory_id": memory_id,
        "comments": thread,
        "count": len(thread)
    }

# ===== GESTIÓN DE MEMORIAS =====

@app.delete("/memory/{memory_id}")
async def delete_memory_endpoint(memory_id: str, user: UserInDB = Depends(current_user)):
    """Elimina una memoria"""
    with user_learning_storage(user.user_id):
        result = delete_memory(memory_id)
    return result

@app.put("/memory/{memory_id}/importance")
async def update_importance(memory_id: str, important: bool, user: UserInDB = Depends(current_user)):
    """Marca o desmarca una memoria como importante"""
    with user_learning_storage(user.user_id):
        result = update_memory_importance(memory_id, important)
    return result

@app.put("/memory/{memory_id}/reminder")
async def set_reminder(memory_id: str, reminder_date: str, reminder_message: str = None, user: UserInDB = Depends(current_user)):
    """Establece un recordatorio para una memoria"""
    with user_learning_storage(user.user_id):
        result = set_memory_reminder(memory_id, reminder_date, reminder_message)
    return result

@app.get("/memory/reminders")
async def get_pending_reminders(user: UserInDB = Depends(current_user)):
    """Obtiene todos los recordatorios pendientes"""
    with user_learning_storage(user.user_id):
        reminders = get_reminders()
    return {
        "reminders": reminders,
        "count": len(reminders)
    }

@app.put("/memory/{memory_id}/expiration")
async def set_expiration(memory_id: str, expires_at: str, user: UserInDB = Depends(current_user)):
    """Establece fecha de caducidad para una memoria"""
    with user_learning_storage(user.user_id):
        result = set_memory_expiration(memory_id, expires_at)
    return result

@app.get("/memory/expired")
async def get_expired(user: UserInDB = Depends(current_user)):
    """Obtiene memorias caducadas"""
    with user_learning_storage(user.user_id):
        expired = get_expired_memories()
    return {
        "expired": expired,
        "count": len(expired)
    }

@app.post("/memory/cleanup")
async def cleanup_expired(user: UserInDB = Depends(current_user)):
    """Archiva memorias caducadas"""
    with user_learning_storage(user.user_id):
        result = cleanup_expired_memories()
    return result

@app.get("/memory/{memory_id}")
async def get_memory(memory_id: str, user: UserInDB = Depends(current_user)):
    """Obtiene una memoria específica por ID"""
    with user_learning_storage(user.user_id):
        memory = get_memory_by_id(memory_id)
    if not memory:
        return {"error": "Memoria no encontrada"}
    return memory

if __name__ == "__main__":
    print("\n🧠 Cerebro Digital Backend")
    print("📡 Iniciando servidor en http://localhost:8000")
    print("📖 Documentación en http://localhost:8000/docs")
    print("✨ Presiona Ctrl+C para detener\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
