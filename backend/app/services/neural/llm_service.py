"""
Servicio de LLM para conversación inteligente
Integra OpenAI con RAG (Retrieval Augmented Generation)
"""
import os
from typing import List, Dict, Optional
from openai import OpenAI


class LLMService:
    """Servicio de conversación con LLM y RAG"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de OpenAI
        
        Args:
            api_key: API key de OpenAI (o desde variable de entorno)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("⚠️  OPENAI_API_KEY no configurada - modo sin LLM")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            print("✅ Cliente OpenAI inicializado")
    
    def generate_response(
        self,
        user_message: str,
        relevant_memories: List[Dict],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Genera respuesta usando RAG: recupera memorias relevantes y genera contexto
        
        Args:
            user_message: Mensaje del usuario
            relevant_memories: Memorias recuperadas por búsqueda semántica
            system_prompt: Prompt del sistema (opcional)
            
        Returns:
            Respuesta generada
        """
        if not self.client:
            # Modo fallback sin LLM
            return self._generate_fallback_response(user_message, relevant_memories)
        
        # Construir contexto con memorias relevantes
        context = self._build_context(relevant_memories)
        
        # System prompt por defecto
        if not system_prompt:
            system_prompt = """Eres un Cerebro Digital, un asistente de memoria personal.
Tu trabajo es ayudar al usuario a recordar información sobre su vida.

Cuando el usuario te haga una pregunta:
1. Usa las memorias proporcionadas como CONTEXTO
2. Responde de forma natural y cercana
3. Si las memorias tienen información relevante, úsala
4. Si no tienes información suficiente, dilo honestamente
5. Sé empático y personal

Las memorias están ordenadas por relevancia (similitud semántica)."""

        # Construir mensajes
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "system",
                "content": f"MEMORIAS RELEVANTES:\n\n{context}"
            })
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Llamar a OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # o "gpt-4" si tienes acceso
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"❌ Error llamando a OpenAI: {e}")
            return self._generate_fallback_response(user_message, relevant_memories)
    
    def _build_context(self, memories: List[Dict]) -> str:
        """Construye texto de contexto con las memorias"""
        if not memories:
            return ""
        
        context_parts = []
        for i, mem in enumerate(memories, 1):
            similarity = mem.get('similarity', 0)
            content = mem.get('content', mem.get('short_content', ''))
            created_at = mem.get('created_at', '')
            
            context_parts.append(
                f"[Memoria {i}] (Relevancia: {similarity:.2%})\n"
                f"Fecha: {created_at}\n"
                f"Contenido: {content}\n"
            )
        
        return "\n".join(context_parts)
    
    def _generate_fallback_response(
        self,
        user_message: str,
        relevant_memories: List[Dict]
    ) -> str:
        """Respuesta básica sin LLM (cuando no hay API key)"""
        if not relevant_memories:
            return "No encontré memorias relacionadas con tu pregunta. Cuéntame más para que pueda recordar."
        
        # Respuesta simple con las memorias
        response = "Encontré estas memorias relacionadas:\n\n"
        
        for i, mem in enumerate(relevant_memories[:3], 1):
            content = mem.get('content', mem.get('short_content', ''))
            similarity = mem.get('similarity', 0)
            response += f"{i}. ({similarity:.0%} relevancia) {content}\n"
        
        return response
    
    def extract_entities_with_llm(self, text: str) -> Dict:
        """
        Usa LLM para extraer entidades de forma más inteligente que regex
        
        Args:
            text: Texto a analizar
            
        Returns:
            Dict con personas, lugares, eventos, emociones, etc.
        """
        if not self.client:
            return {"error": "LLM no disponible"}
        
        system_prompt = """Eres un extractor de información.
Analiza el texto y extrae:
- Personas (nombres, relaciones familiares)
- Lugares (ciudades, sitios específicos)
- Eventos (cumpleaños, viajes, reuniones)
- Emociones (sentimientos expresados)
- Fechas (si se mencionan)

Responde SOLO en formato JSON."""

        user_prompt = f"""Texto: "{text}"

Extrae las entidades en este formato:
{{
    "personas": [{{"nombre": "...", "relacion": "..."}}],
    "lugares": ["..."],
    "eventos": ["..."],
    "emociones": ["..."],
    "fecha": "..."
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        
        except Exception as e:
            print(f"❌ Error extrayendo entidades: {e}")
            return {"error": str(e)}


# Instancia global
_llm_service = None

def get_llm_service() -> LLMService:
    """Obtiene la instancia global del servicio LLM"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
