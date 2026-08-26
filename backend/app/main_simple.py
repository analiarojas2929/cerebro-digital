from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

# Crear aplicación FastAPI
app = FastAPI(
    title="Cerebro Digital - Versión Simple",
    version="1.0.0",
    description="Sistema de cerebro digital - versión sin bases de datos para testing rápido"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class MessageInput(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = "default_user"

class MessageResponse(BaseModel):
    response: str
    session_id: str
    category: Optional[str] = None
    confidence: float = 0.0
    related_memories: List = []

# Almacenamiento en memoria (temporal)
conversations = []


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "name": "Cerebro Digital - Versión Simple",
        "version": "1.0.0",
        "status": "operational",
        "message": "API funcionando correctamente (versión simplificada)"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@app.post("/chat/message", response_model=MessageResponse)
async def send_message(message_input: MessageInput):
    """Envía un mensaje al cerebro digital"""
    
    # Generar session_id si no existe
    session_id = message_input.session_id or str(uuid.uuid4())
    
    # Clasificación simple por palabras clave
    message_lower = message_input.message.lower()
    category = "general"
    confidence = 0.5
    
    if any(word in message_lower for word in ['trabajo', 'proyecto', 'reunión', 'cliente']):
        category = "trabajo"
        confidence = 0.8
    elif any(word in message_lower for word in ['código', 'programar', 'python', 'api']):
        category = "tecnología"
        confidence = 0.8
    elif any(word in message_lower for word in ['familia', 'amigo', 'casa', 'personal']):
        category = "personal"
        confidence = 0.8
    
    # Generar respuesta simple
    if any(word in message_lower for word in ['hola', 'hey', 'hello']):
        response = "¡Hola! Soy tu Cerebro Digital (versión simple). ¿En qué puedo ayudarte?"
    elif any(word in message_lower for word in ['cómo estás', 'qué tal']):
        response = f"¡Funcionando perfectamente! He clasificado tu mensaje como '{category}'. ¿Qué necesitas?"
    elif any(word in message_lower for word in ['gracias', 'thanks']):
        response = "¡De nada! Estoy aquí para ayudarte."
    else:
        response = f"He procesado tu mensaje y lo he clasificado como '{category}' con {confidence*100:.0f}% de confianza. Esta es una versión simplificada - para funcionalidad completa necesitas configurar PostgreSQL y Redis."
    
    # Guardar en memoria temporal
    conversations.append({
        "session_id": session_id,
        "user_message": message_input.message,
        "assistant_message": response,
        "category": category,
        "timestamp": datetime.now().isoformat()
    })
    
    return MessageResponse(
        response=response,
        session_id=session_id,
        category=category,
        confidence=confidence,
        related_memories=[]
    )


@app.get("/chat/history/{session_id}")
async def get_history(session_id: str, limit: int = 50):
    """Obtiene el historial de una sesión"""
    session_convs = [
        c for c in conversations 
        if c["session_id"] == session_id
    ][-limit:]
    
    return session_convs


@app.get("/memory/stats")
async def get_stats():
    """Obtiene estadísticas"""
    categories = {}
    for conv in conversations:
        cat = conv.get("category", "general")
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_conversations": len(conversations),
        "total_memories": len(conversations),
        "categories": [
            {"name": cat, "count": count}
            for cat, count in categories.items()
        ]
    }


@app.get("/memory/categories")
async def get_categories():
    """Obtiene categorías disponibles"""
    return [
        {
            "id": 1,
            "name": "trabajo",
            "description": "Trabajo y proyectos",
            "keywords": ["trabajo", "proyecto", "reunión"],
            "color": "#3B82F6",
            "icon": "💼",
            "conversation_count": sum(1 for c in conversations if c.get("category") == "trabajo")
        },
        {
            "id": 2,
            "name": "tecnología",
            "description": "Programación y tecnología",
            "keywords": ["código", "python", "api"],
            "color": "#EF4444",
            "icon": "💻",
            "conversation_count": sum(1 for c in conversations if c.get("category") == "tecnología")
        },
        {
            "id": 3,
            "name": "personal",
            "description": "Vida personal",
            "keywords": ["familia", "amigos", "casa"],
            "color": "#10B981",
            "icon": "🏠",
            "conversation_count": sum(1 for c in conversations if c.get("category") == "personal")
        },
        {
            "id": 4,
            "name": "general",
            "description": "General",
            "keywords": [],
            "color": "#6B7280",
            "icon": "📌",
            "conversation_count": sum(1 for c in conversations if c.get("category") == "general")
        }
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
