from typing import Optional
import uuid
from sqlalchemy.orm import Session
from loguru import logger

from app.models.schemas import MessageInput, MessageResponse
from app.models.database_models import Conversation
from app.services.memory.memory_manager import memory_manager
from app.services.classifier.category_classifier import classifier


class ConversationService:
    """Servicio principal de conversación"""
    
    def __init__(self):
        pass
    
    def generate_response(self, message: str, context: str) -> str:
        """
        Genera una respuesta basada en el mensaje y contexto
        
        NOTA: Esta es una implementación básica.
        En producción, integrar con OpenAI, Anthropic, o un modelo local (Ollama)
        
        Args:
            message: Mensaje del usuario
            context: Contexto de la conversación
            
        Returns:
            Respuesta generada
        """
        # Implementación simple basada en reglas
        # TODO: Integrar con LLM real (OpenAI, Claude, Ollama)
        
        message_lower = message.lower()
        
        # Respuestas básicas de ejemplo
        if any(word in message_lower for word in ['hola', 'hey', 'hello']):
            return "¡Hola! Soy tu cerebro digital. Puedo recordar nuestras conversaciones y ayudarte a organizar información. ¿En qué puedo ayudarte?"
        
        elif any(word in message_lower for word in ['cómo estás', 'qué tal']):
            return "Estoy funcionando perfectamente. Listo para ayudarte y recordar todo lo que hablemos. ¿Qué tienes en mente?"
        
        elif any(word in message_lower for word in ['gracias', 'thanks']):
            return "¡De nada! Estoy aquí para ayudarte. Todo lo que hablamos queda guardado en mi memoria."
        
        elif any(word in message_lower for word in ['recordar', 'memoria', 'recuerdas']):
            return "Tengo acceso a toda nuestra conversación anterior. Puedo buscar información específica si me dices qué necesitas recordar."
        
        else:
            # Respuesta genérica con contexto
            response = f"He procesado tu mensaje sobre: '{message[:100]}...'. "
            response += "Esta información se ha guardado en mi memoria y la he clasificado automáticamente. "
            
            if context:
                response += "También he considerado nuestras conversaciones previas para darte una mejor respuesta."
            
            return response
    
    def process_message(
        self,
        message_input: MessageInput,
        db: Session
    ) -> MessageResponse:
        """
        Procesa un mensaje del usuario y genera respuesta
        
        Args:
            message_input: Datos del mensaje
            db: Sesión de base de datos
            
        Returns:
            Respuesta completa con metadata
        """
        try:
            # Generar session_id si no existe
            session_id = message_input.session_id or str(uuid.uuid4())
            
            # 1. Obtener contexto de memoria
            context = memory_manager.get_conversation_context(
                session_id=session_id,
                current_message=message_input.message,
                db=db
            )
            
            # 2. Clasificar mensaje
            category, confidence = classifier.classify(message_input.message)
            
            # 3. Buscar memorias relacionadas
            related_memories = memory_manager.search_memories(
                query=message_input.message,
                limit=3
            )
            
            # 4. Generar respuesta
            assistant_response = self.generate_response(
                message=message_input.message,
                context=context
            )
            
            # 5. Guardar en memoria de corto plazo
            memory_manager.add_to_short_term(
                session_id=session_id,
                user_message=message_input.message,
                assistant_message=assistant_response
            )
            
            # 6. Guardar en base de datos
            conversation = Conversation(
                session_id=session_id,
                user_message=message_input.message,
                assistant_message=assistant_response,
                category=category,
                importance_score=confidence,
                metadata={
                    "user_id": message_input.user_id,
                    "context_used": bool(context)
                }
            )
            db.add(conversation)
            db.commit()
            
            # 7. Si es importante, guardar en largo plazo
            if confidence > 0.7:
                memory_manager.save_to_long_term(
                    db=db,
                    content=f"Usuario: {message_input.message}\nAsistente: {assistant_response}",
                    category=category,
                    importance_score=confidence,
                    metadata={"session_id": session_id}
                )
            
            logger.info(f"Mensaje procesado. Categoría: {category}, Confianza: {confidence:.2f}")
            
            # 8. Crear respuesta
            return MessageResponse(
                response=assistant_response,
                session_id=session_id,
                category=category,
                confidence=confidence,
                related_memories=[
                    {
                        "content": mem["content"][:200],
                        "similarity": mem["similarity"],
                        "category": mem["metadata"].get("category")
                    }
                    for mem in related_memories
                ]
            )
            
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {e}")
            raise


# Singleton instance
conversation_service = ConversationService()
