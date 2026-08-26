# 📚 Preguntas Frecuentes (FAQ)

## General

### ¿Qué es Cerebro Digital?

Es un sistema inteligente de memoria y conversación que recuerda tus interacciones, clasifica automáticamente la información y te permite buscar semánticamente en tu historial de conversaciones.

### ¿Cómo funciona?

Usa:
- **Embeddings** para convertir texto en vectores numéricos
- **Base de datos vectorial** para búsqueda semántica
- **Clasificador neural** para categorizar automáticamente
- **Memoria dual** (corto y largo plazo) como el cerebro humano

### ¿Es gratis?

Sí, el proyecto es open source (MIT License). Los únicos costos potenciales son:
- Servidores si lo despliegas en la nube
- API de LLMs si usas OpenAI/Anthropic (opcional)

## Instalación

### ¿Qué necesito para ejecutarlo?

**Opción 1 (Docker)**: Solo Docker instalado

**Opción 2 (Local)**:
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### ¿Puedo usar solo el backend sin el frontend?

Sí, el backend es una API REST completa. Puedes usarla con:
- Postman/Insomnia
- CLI con curl
- Tu propia aplicación
- Scripts de Python

### Error: "No module named 'app'"

Asegúrate de:
1. Activar el entorno virtual
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar desde el directorio correcto

## Funcionalidad

### ¿Cómo mejoro las respuestas?

El sistema base usa respuestas simples. Para respuestas inteligentes:
1. Integra un LLM (OpenAI, Claude, Ollama)
2. Lee `LLM_INTEGRATION.md`
3. Configura tu API key

### ¿Puedo añadir mis propias categorías?

Sí, edita `backend/app/services/classifier/category_classifier.py`:

```python
self.categories = {
    "mi_categoria": {
        "keywords": ["palabra1", "palabra2"],
        "color": "#FF5733",
        "icon": "🎯"
    },
    # ... otras categorías
}
```

### ¿Cómo funciona la memoria?

Dos tipos:

**Memoria de Corto Plazo (Redis)**:
- Últimas 50 conversaciones
- Acceso ultra-rápido
- Expira después de 1 hora

**Memoria de Largo Plazo (PostgreSQL + ChromaDB)**:
- Información importante
- Búsqueda semántica
- Persiste indefinidamente

### ¿Puedo borrar conversaciones?

Actualmente puedes:
- Limpiar la sesión actual (botón de basura)
- Las memorias se mantienen
- Roadmap: control granular de borrado

## Privacidad y Seguridad

### ¿Dónde se guardan mis datos?

Todo local en tu máquina (por defecto):
- PostgreSQL: `./pgdata/`
- ChromaDB: `./chroma_data/`
- Redis: en memoria

### ¿Puedo usar sin conexión a internet?

Parcialmente:
- ✅ Sistema de memoria funciona offline
- ✅ Clasificador funciona offline
- ❌ LLMs externos (OpenAI/Claude) necesitan internet
- ✅ Ollama (local) funciona completamente offline

### ¿Es seguro?

El código es open source - puedes auditarlo. Recomendaciones:
- Usa HTTPS en producción
- Cambia `SECRET_KEY` en `.env`
- No expongas Redis/PostgreSQL públicamente
- Usa auth si despliegas en internet

## Performance

### ¿Cuánta RAM necesito?

Depende del modelo de embeddings:
- Mínimo: 2GB RAM
- Recomendado: 4GB RAM
- Con GPU: mejor performance

### ¿Cuántas conversaciones puede manejar?

ChromaDB puede escalar a millones de vectores. Bottlenecks potenciales:
- PostgreSQL: depende de tu hardware
- Redis: limitado por RAM disponible

### ¿Puedo usar GPU?

Sí, para acelerar embeddings:

```python
# En embeddings.py
self.model = SentenceTransformer(
    self.model_name,
    device='cuda'  # o 'mps' en Mac M1/M2
)
```

## Desarrollo

### ¿Cómo contribuyo?

Lee `CONTRIBUTING.md`. En resumen:
1. Fork el repo
2. Crea una rama
3. Haz tus cambios
4. Tests y documentación
5. Pull request

### ¿Puedo monetizar mi versión?

Sí (MIT License), pero:
- Mantén atribución original
- Comparte mejoras (opcional pero apreciado)

### ¿Hay roadmap?

Sí, revisa `ROADMAP.md` para features planeadas.

## Integración

### ¿Cómo conecto con OpenAI?

```python
# 1. Instala
pip install openai

# 2. Configura .env
OPENAI_API_KEY=sk-tu-key

# 3. Usa en conversation_service.py
from openai import OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)
```

Ver `LLM_INTEGRATION.md` para más detalles.

### ¿Puedo usar modelos locales?

Sí, opciones:
- **Ollama**: Muy fácil, buena calidad
- **llama.cpp**: Más control, requiere setup
- **Transformers**: Directo de HuggingFace

### ¿Funciona con otros idiomas?

Sí, el modelo de embeddings es multilingüe:
- Español ✅
- Inglés ✅
- Francés ✅
- Alemán ✅
- Y más...

## Troubleshooting

### "Connection refused" en backend

1. Verifica PostgreSQL: `docker ps` o `systemctl status postgresql`
2. Verifica Redis: `redis-cli ping`
3. Revisa `.env` - URLs correctas

### Frontend no conecta con backend

Verifica CORS en `backend/app/main.py`:

```python
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Añade tu frontend URL
]
```

### Embeddings muy lentos

Opciones:
1. Usa modelo más pequeño
2. Habilita GPU
3. Batch processing para múltiples textos

### ChromaDB error de permisos

```bash
# Linux/Mac
chmod -R 755 chroma_data/

# Windows: ejecuta como administrador
```

## Otros

### ¿Dónde consigo ayuda?

1. GitHub Issues para bugs
2. GitHub Discussions para preguntas
3. README.md y docs incluidas

### ¿Actualizaciones futuras?

El proyecto está activamente desarrollado. Ver:
- `CHANGELOG.md` para cambios
- `ROADMAP.md` para planes futuros
- GitHub releases

### ¿Puedo usarlo comercialmente?

Sí, licencia MIT lo permite. Solo:
- Incluye copyright notice
- No nos responsabilizamos por problemas
