# 🧠 Cerebro Digital - Instalación Fase 1-3

## 📋 Prerequisitos

1. **PostgreSQL 14+** instalado y corriendo
2. **Python 3.10+**
3. **Node.js 18+** (para frontend)
4. **Cuenta OpenAI** (opcional pero recomendado)

## 🚀 Instalación Rápida

### 1. Instalar PostgreSQL + pgvector

#### Windows (con Chocolatey):
```powershell
choco install postgresql
```

#### O descarga desde: https://www.postgresql.org/download/windows/

Después de instalar PostgreSQL:

```powershell
# Iniciar servicio
net start postgresql-x64-14

# Crear base de datos
psql -U postgres
CREATE DATABASE cerebro_digital;
\q
```

### 2. Instalar extensión pgvector

```powershell
# Opción 1: Desde binarios pre-compilados
# https://github.com/pgvector/pgvector/releases

# Opción 2: Compilar desde fuente (requiere Visual Studio)
git clone https://github.com/pgvector/pgvector.git
cd pgvector
# Seguir instrucciones en README
```

**NOTA**: En Windows es más fácil usar Docker:

```powershell
# Usar PostgreSQL con pgvector en Docker
docker run -d \
  --name cerebro-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=cerebro_digital \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

### 3. Configurar Backend

```powershell
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales

# Inicializar base de datos
python app/core/db_manager.py

# Iniciar servidor
python server.py
```

### 4. Configurar API de OpenAI (opcional)

1. Ve a https://platform.openai.com/api-keys
2. Crea una API key
3. Agrega a tu `.env`:
```
OPENAI_API_KEY=sk-...tu-key-aqui
```

Si NO configuras OpenAI, el sistema funcionará pero sin conversación inteligente.

## ✅ Verificación

### Test de base de datos:
```powershell
python app/core/db_manager.py
```

Deberías ver:
```
✅ Conexión exitosa a PostgreSQL
✅ Extensión pgvector disponible
✅ Base de datos inicializada correctamente
```

### Test de embeddings:
```powershell
python app/services/neural/embedding_service.py
```

Deberías ver:
```
📦 Cargando modelo de embeddings: all-MiniLM-L6-v2...
✅ Modelo cargado (384D)
```

## 🧪 Probar el Sistema

### 1. Crear una memoria:
```powershell
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Mi pareja se llama Sebastián Montero"}'
```

### 2. Buscar semánticamente:
```powershell
curl "http://localhost:8000/memory/search?query=información sobre mi pareja"
```

### 3. Ver red neuronal:
```
http://localhost:5175/
```

## 📊 Nuevas Funcionalidades

### Búsqueda Semántica
```javascript
// Frontend
const results = await memoryApi.searchMemories("¿qué sabes de mi familia?");
```

### Conversación con IA
```javascript
const response = await chatApi.sendMessage({
  message: "Cuéntame sobre mis recuerdos en Viña"
});
```

### Memoria Persistente
- ✅ Las memorias se guardan en PostgreSQL
- ✅ Los embeddings se almacenan en pgvector
- ✅ Búsqueda vectorial ultra rápida
- ✅ NO se pierde nada al reiniciar

## 🔧 Troubleshooting

### Error: "extensión pgvector no encontrada"
```sql
-- Conectar a PostgreSQL
psql -U postgres -d cerebro_digital

-- Instalar extensión
CREATE EXTENSION vector;
```

### Error: "OpenAI API key inválida"
- Verifica que tu key sea correcta en `.env`
- O comenta/elimina la key para usar modo fallback

### Error: "No module named 'sentence_transformers'"
```powershell
pip install sentence-transformers
```

### Error de conexión a PostgreSQL
- Verifica que el servicio esté corriendo: `net start postgresql-x64-14`
- Revisa el `DATABASE_URL` en `.env`
- Prueba la conexión: `psql -U postgres`

## 📦 Dependencias Nuevas

Instaladas automáticamente con `requirements.txt`:
- `pgvector` - Extensión PostgreSQL para vectores
- `sentence-transformers` - Generación de embeddings
- `openai` - Cliente de OpenAI
- `sqlalchemy` - ORM para PostgreSQL
- `psycopg2-binary` - Driver PostgreSQL

## 🎯 Próximos Pasos

Ahora que tienes:
- ✅ Persistencia real (PostgreSQL)
- ✅ Búsqueda semántica (embeddings)
- ✅ Conversación inteligente (LLM)

Puedes avanzar a:
- [ ] Fase 4: Red neuronal propia con PyTorch
- [ ] Fase 5: Voz (Speech-to-Text + Text-to-Speech)
- [ ] Timeline visual de memorias
- [ ] Exportar legado familiar en PDF

## 💡 Comandos Útiles

```powershell
# Ver memorias en DB
psql -U postgres -d cerebro_digital -c "SELECT id, short_content FROM memories ORDER BY created_at DESC LIMIT 10;"

# Contar memorias
psql -U postgres -d cerebro_digital -c "SELECT COUNT(*) FROM memories;"

# Buscar por similitud (SQL directo)
psql -U postgres -d cerebro_digital -c "SELECT short_content, 1 - (embedding <=> '[...]') as similarity FROM memories ORDER BY similarity DESC LIMIT 5;"
```
