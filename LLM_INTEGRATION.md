# 📋 INSTRUCCIONES DE INTEGRACIÓN CON LLM

El proyecto viene con un sistema de respuestas básico. Para hacerlo realmente inteligente, integra con un LLM:

## Opción 1: OpenAI (Recomendado para producción)

1. Instala la dependencia:
```bash
pip install openai
```

2. Edita `backend/app/services/conversation/conversation_service.py`:

```python
from openai import OpenAI

class ConversationService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_response(self, message: str, context: str) -> str:
        system_prompt = f"""Eres un asistente de cerebro digital que recuerda conversaciones.
        
Contexto de memoria:
{context}

Tu trabajo es:
- Responder de forma útil y conversacional
- Usar el contexto de memoria cuando sea relevante
- Ayudar al usuario a organizar y recordar información
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
```

## Opción 2: Anthropic Claude

1. Instala:
```bash
pip install anthropic
```

2. Implementa:
```python
from anthropic import Anthropic

class ConversationService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate_response(self, message: str, context: str) -> str:
        system_prompt = f"Contexto de memoria:\n{context}"
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": message}
            ]
        )
        
        return response.content[0].text
```

## Opción 3: Ollama (Local, gratis, privado)

1. Instala Ollama: https://ollama.ai

2. Descarga un modelo:
```bash
ollama pull llama2
# o
ollama pull mistral
```

3. Implementa:
```python
import requests

class ConversationService:
    def generate_response(self, message: str, context: str) -> str:
        prompt = f"""Contexto de memoria:
{context}

Usuario: {message}

Asistente:"""
        
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        })
        
        return response.json()['response']
```

## Opción 4: LangChain (Flexible)

Para mayor control y memoria avanzada:

```python
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

class ConversationService:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-4")
        self.memory = ConversationBufferMemory()
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory
        )
    
    def generate_response(self, message: str, context: str) -> str:
        # Inyectar contexto en la memoria
        if context:
            self.memory.chat_memory.add_ai_message(f"Contexto: {context}")
        
        response = self.chain.predict(input=message)
        return response
```

## Recomendaciones

### Para Desarrollo/Pruebas
- **Ollama** (Llama 2 o Mistral): Gratis, local, buena calidad

### Para Producción
- **OpenAI GPT-4**: Mejor calidad, más costoso
- **Claude 3**: Excelente para conversaciones largas
- **GPT-3.5-turbo**: Balance precio/calidad

### Para Privacidad
- **Ollama local**: 100% privado, sin costos

## Próximos Pasos

Después de integrar el LLM:

1. **Mejora el sistema de memoria**: 
   - Implementa resúmenes automáticos de conversaciones
   - Añade búsqueda híbrida (keyword + semántica)

2. **Añade funciones de herramientas**:
   - Búsqueda en internet
   - Calculadora
   - Extracción de información

3. **Mejora la clasificación**:
   - Entrena un clasificador personalizado
   - Añade detección de entidades (personas, lugares, fechas)

4. **Dashboard de analytics**:
   - Visualización de patrones de conversación
   - Gráficos de categorías más usadas
   - Timeline de memoria
