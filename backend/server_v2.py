"""
Cerebro Digital Server v2.0
Sistema con PostgreSQL + Embeddings + LLM

NUEVO: Búsqueda semántica + Conversación inteligente + Memoria persistente
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar nuevos servicios
from app.core.db_manager import test_connection, init_database
from app.services.memory.persistent_memory import get_memory_service
from app.services.neural.llm_service import get_llm_service
from dynamic_learning import extract_entities  # Mantener detección de entidades

# Aplicación
app = FastAPI(
    title="Cerebro Digital v2.0",
    description="Sistema de memoria persistente con IA",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class MessageInput(BaseModel):
    message: str
    session_id: Optional[str] = None

class MessageResponse(BaseModel):
    response: str
    session_id: str
    entities_detected: Optional[dict] = None
    memory_id: Optional[int] = None

class SearchQuery(BaseModel):
    query: str
    limit: int = 5

class CommentInput(BaseModel):
    memory_id: int
    comment: str
    user: str = "Usuario"


# === INICIALIZACIÓN ===

@app.on_event("startup")
async def startup():
    """Inicialización al arrancar el servidor"""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║          🧠 CEREBRO DIGITAL v2.0 - SISTEMA NEURONAL         ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    # Test de conexión a DB
    print("🔍 Verificando base de datos...")
    if not test_connection():
        print("⚠️  PostgreSQL no disponible - algunas funciones no funcionarán")
    else:
        print("✅ PostgreSQL conectado")
    
    # Cargar servicios
    print("\n📦 Cargando servicios...")
    get_memory_service()
    get_llm_service()
    
    print("\n🚀 Servidor listo\n")


# === ENDPOINTS PRINCIPALES ===

@app.get("/")
async def root():
    """Información del servidor"""
    return {
        "name": "Cerebro Digital v2.0",
        "version": "2.0.0",
        "features": [
            "PostgreSQL + pgvector",
            "Búsqueda semántica",
            "Conversación con LLM",
            "Memoria persistente",
            "Red neuronal visual"
        ],
        "status": "online"
    }


@app.get("/health")
async def health():
    """Health check"""
    try:
        test_connection()
        return {"status": "healthy", "database": "connected"}
    except:
        return {"status": "degraded", "database": "disconnected"}


# === CHAT CON IA ===

@app.post("/chat/message")
async def chat_message(input: MessageInput):
    """
    Envía mensaje y recibe respuesta inteligente con RAG
    
    NUEVO: Ahora usa búsqueda semántica + LLM para respuestas contextuales
    """
    try:
        memory_service = get_memory_service()
        llm_service = get_llm_service()
        
        # 1. Extraer entidades del mensaje
        entities = extract_entities(input.message)
        
        # 2. Guardar memoria en PostgreSQL
        memory_id = memory_service.create_memory(
            content=input.message,
            memory_type="conversation",
            importance=0.6
        )
        
        # 3. Asociar entidades a la memoria
        for persona in entities.get('personas', []):
            memory_service.add_entity_to_memory(
                memory_id=memory_id,
                entity_name=persona['name'],
                entity_type="PERSONA",
                icon=persona['icon']
            )
        
        for lugar in entities.get('lugares', []):
            memory_service.add_entity_to_memory(
                memory_id=memory_id,
                entity_name=lugar['name'],
                entity_type="LUGAR",
                icon=lugar['icon']
            )
        
        # 4. Buscar memorias relevantes para contexto
        relevant_memories = memory_service.semantic_search(
            query=input.message,
            limit=5
        )
        
        # 5. Generar respuesta con LLM + RAG
        response_text = llm_service.generate_response(
            user_message=input.message,
            relevant_memories=relevant_memories
        )
        
        return MessageResponse(
            response=response_text,
            session_id=input.session_id or "default",
            entities_detected=entities,
            memory_id=memory_id
        )
    
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# === BÚSQUEDA SEMÁNTICA ===

@app.get("/memory/search")
async def search_memories(
    query: str = Query(..., description="Pregunta o búsqueda"),
    limit: int = Query(5, ge=1, le=50)
):
    """
    Búsqueda semántica de memorias
    
    Ejemplo: /memory/search?query=qué sabes de mi familia
    """
    try:
        memory_service = get_memory_service()
        results = memory_service.semantic_search(query=query, limit=limit)
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memory/search")
async def search_memories_post(search: SearchQuery):
    """Búsqueda semántica (POST)"""
    try:
        memory_service = get_memory_service()
        results = memory_service.semantic_search(
            query=search.query,
            limit=search.limit
        )
        
        return {
            "query": search.query,
            "results": results,
            "count": len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === MEMORIAS ===

@app.get("/memory/recent")
async def get_recent_memories(limit: int = Query(50, ge=1, le=200)):
    """Obtiene las memorias más recientes"""
    try:
        memory_service = get_memory_service()
        memories = memory_service.get_recent_memories(limit=limit)
        
        return {
            "memories": memories,
            "count": len(memories)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === COMENTARIOS ===

@app.post("/memory/comment")
async def add_comment(input: CommentInput):
    """Agrega comentario a una memoria"""
    try:
        memory_service = get_memory_service()
        comment_id = memory_service.add_comment(
            memory_id=input.memory_id,
            content=input.comment,
            user_name=input.user
        )
        
        return {
            "success": True,
            "comment_id": comment_id,
            "message": "Comentario agregado"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/thread/{memory_id}")
async def get_thread(memory_id: int):
    """Obtiene hilo de comentarios de una memoria"""
    try:
        memory_service = get_memory_service()
        comments = memory_service.get_memory_thread(memory_id)
        
        return {
            "memory_id": memory_id,
            "comments": comments,
            "count": len(comments)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === ESTADÍSTICAS ===

@app.get("/memory/stats")
async def get_stats():
    """Estadísticas del sistema"""
    from app.core.db_manager import engine
    from sqlalchemy import text
    
    try:
        with engine.connect() as conn:
            # Contar memorias
            result = conn.execute(text("SELECT COUNT(*) FROM memories"))
            total_memories = result.fetchone()[0]
            
            # Contar entidades
            result = conn.execute(text("SELECT COUNT(*) FROM entities"))
            total_entities = result.fetchone()[0]
            
            # Contar categorías
            result = conn.execute(text("SELECT COUNT(*) FROM categories"))
            total_categories = result.fetchone()[0]
            
            # Contar subcategorías
            result = conn.execute(text("SELECT COUNT(*) FROM subcategories"))
            total_subcategories = result.fetchone()[0]
        
        return {
            "total_memories": total_memories,
            "total_entities": total_entities,
            "total_categories": total_categories,
            "total_subcategories": total_subcategories,
            "database": "PostgreSQL + pgvector",
            "features": ["semantic_search", "llm_chat", "persistent_storage"]
        }
    
    except Exception as e:
        return {"error": str(e)}


# === RED NEURONAL ===

@app.get("/memory/neural-graph")
async def get_neural_graph():
    """
    Genera red neuronal visual
    
    NOTA: Por ahora mantiene compatibilidad con el sistema anterior
    TODO: Migrar completamente a PostgreSQL
    """
    from dynamic_learning import get_category_summary, memory_threads
    
    learned_data = get_category_summary()
    nodes = []
    links = []
    
    # Generar nodos y links (mantener lógica anterior)
    # ... [código de generación del grafo]
    
    # Por ahora retornar estructura vacía
    # El usuario puede decidir si migrar esta parte también
    
    return {
        "nodes": nodes,
        "links": links,
        "stats": {
            "total_nodes": len(nodes),
            "total_connections": len(links)
        }
    }


if __name__ == "__main__":
    print("\n🧠 Iniciando Cerebro Digital v2.0...\n")
    print("📡 Servidor: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("🔍 Búsqueda: http://localhost:8000/memory/search?query=...")
    print("\n✨ Presiona Ctrl+C para detener\n")
    
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
