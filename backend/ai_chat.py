"""
Servicio de Conversación con IA (Kostra AI)
Para usar en el sistema v1.0 sin necesidad de PostgreSQL
"""
import os
from typing import List, Dict, Optional
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI SDK no instalado. Instala con: pip install openai")

# Cliente de IA (compatible con OpenAI API)
ai_client = None

def initialize_openai(api_key: Optional[str] = None):
    """Inicializa el cliente de IA (Kostra)"""
    global ai_client
    
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI SDK no está disponible. Instala: pip install openai")
        return False
    
    # Obtener API key de Kostra
    api_key = api_key or os.getenv('KOSTRA_KEY')
    
    if not api_key:
        print("⚠️  No se encontró KOSTRA_KEY")
        print("    Agrega tu API key a backend/.env:")
        print("    KOSTRA_KEY=tu-key-aqui")
        return False
    
    try:
        # Inicializar con Kostra AI endpoint
        ai_client = OpenAI(
            api_key=api_key,
            base_url="https://ai.kostra.cloud/v1"
        )
        print("✅ Kostra AI inicializado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar Kostra AI: {e}")
        return False


def generate_ai_response(user_message: str, conversation_history: List[Dict], memories: List[Dict] = None) -> str:
    """
    Genera una respuesta usando IA (Kostra - DeepSeek)
    
    Args:
        user_message: Mensaje del usuario
        conversation_history: Historial de la conversación
        memories: Memorias relevantes del usuario (opcional)
    
    Returns:
        Respuesta generada por la IA
    """
    global ai_client
    
    # Si IA no está disponible, respuesta básica
    if not ai_client:
        return generate_fallback_response(user_message, memories)
    
    try:
        # Construir contexto con memorias
        context = ""
        if memories and len(memories) > 0:
            context = "\n\nMemoria del usuario:\n"
            for i, memory in enumerate(memories[:5], 1):
                context += f"{i}. {memory.get('content', memory.get('text', ''))}\n"
        
        # Sistema prompt
        system_prompt = f"""Eres un Cerebro Digital, un asistente de memoria personal que ayuda a recordar y organizar la vida del usuario.

Características:
- Empático y cálido, como un confidente
- Ayudas a recordar momentos importantes
- Detectas patrones y relaciones en las memorias
- Haces preguntas para entender mejor
- Respondes de forma natural y conversacional

{context}

Responde de forma breve (máximo 3 líneas), cálida y personal."""

        # Construir mensajes
        messages = [{"role": "system", "content": system_prompt}]
        
        # Agregar historial (últimos 5 mensajes)
        for msg in conversation_history[-5:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Agregar mensaje actual
        messages.append({"role": "user", "content": user_message})
        
        # Llamar a Kostra AI (DeepSeek V4-Flash - más rápido y económico)
        response = ai_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Error con IA: {e}")
        return generate_fallback_response(user_message, memories)


def generate_fallback_response(user_message: str, memories: List[Dict] = None) -> str:
    """Respuesta básica cuando OpenAI no está disponible"""
    text_lower = user_message.lower()
    
    # Respuestas contextuales básicas
    if any(word in text_lower for word in ['hola', 'buenas', 'hey', 'hi']):
        return "¡Hola! Cuéntame algo sobre tu día, tu familia, o cualquier recuerdo que quieras guardar."
    
    elif any(word in text_lower for word in ['gracias', 'thank']):
        return "¡De nada! Estoy aquí para ayudarte a recordar lo importante."
    
    elif any(word in text_lower for word in ['qué puedes', 'qué sabes', 'ayuda', 'help']):
        return "Puedo ayudarte a recordar personas, lugares, eventos y momentos especiales. Solo cuéntame lo que quieras guardar."
    
    elif any(word in text_lower for word in ['quién', 'quien', 'recordar']):
        if memories:
            return f"He guardado {len(memories)} memorias sobre esto. ¿Quieres que te cuente más detalles?"
        return "Aún no tengo muchas memorias sobre eso. Cuéntame más para que pueda recordarlo."
    
    else:
        # Respuesta genérica
        return "Entendido, he guardado esta información. ¿Hay algo más que quieras contarme?"


# Inicializar al importar
if OPENAI_AVAILABLE:
    initialize_openai()
