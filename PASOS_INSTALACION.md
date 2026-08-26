# ⚡ Instalación Rápida - 3 Pasos

## Estado Actual

✅ **Dependencias Python instaladas**
- FastAPI, SQLAlchemy, OpenAI
- sentence-transformers (embeddings)
- pgvector, psycopg2-binary

❌ **Falta: Docker Desktop**

---

## 📋 Pasos para Completar la Instalación

### 1️⃣ Instalar Docker Desktop

**Se abrió automáticamente la página de descarga.**

1. Descarga Docker Desktop para Windows
2. Instala y reinicia Windows si es necesario
3. Abre Docker Desktop y espera a que inicie
4. Verifica en PowerShell: `docker --version`

**Tiempo estimado:** 5-10 minutos

---

### 2️⃣ Iniciar PostgreSQL (después de instalar Docker)

```powershell
# Ejecutar este script
.\start_postgres.ps1
```

**Qué hace:**
- Descarga imagen `pgvector/pgvector:pg16`
- Crea contenedor `cerebro-postgres`
- Inicia PostgreSQL en puerto 5432
- Base de datos: `cerebro_digital`
- Usuario/Password: `postgres/postgres`

**Tiempo estimado:** 2 minutos

---

### 3️⃣ Inicializar Base de Datos

```powershell
# Ejecutar este script
.\init_database.ps1
```

**Qué hace:**
- Ejecuta `schema.sql` (crea tablas)
- Opcionalmente migra datos del sistema anterior
- Verifica que todo funcione

**Tiempo estimado:** 1 minuto

---

## 🚀 Iniciar el Servidor v2.0

Una vez completados los pasos anteriores:

```powershell
cd backend
python server_v2.py
```

Abre: http://localhost:8000/docs

---

## ⚠️ Mientras Tanto (Opcional)

Si quieres seguir usando el sistema actual (in-memory):

```powershell
# Terminal 1
cd backend
python server.py

# Terminal 2
cd frontend
npm run dev
```

Abre: http://localhost:5175

**Nota:** Este sistema pierde datos al reiniciar.

---

## 🔍 Verificar que Todo Funcione

Una vez instalado Docker y PostgreSQL:

```powershell
# 1. Verificar Docker
docker ps

# 2. Verificar PostgreSQL
docker logs cerebro-postgres

# 3. Probar conexión a DB
cd backend
python -c "from app.core.db_manager import test_connection; test_connection()"

# 4. Iniciar servidor v2
python server_v2.py
```

---

## 📁 Scripts Disponibles

| Script | Descripción |
|--------|-------------|
| `install_v2.ps1` | ❌ Instalación completa (requiere Docker ya instalado) |
| `start_postgres.ps1` | ✅ Solo inicia PostgreSQL en Docker |
| `init_database.ps1` | ✅ Solo inicializa la base de datos |

---

## 🆘 Problemas Comunes

### "docker: comando no reconocido"
- Docker Desktop no está instalado o no está corriendo
- Reinicia Windows después de instalar Docker
- Abre Docker Desktop manualmente

### "Connection refused" (PostgreSQL)
- Ejecuta `.\start_postgres.ps1` para iniciar el contenedor
- Espera 10 segundos a que PostgreSQL esté listo
- Verifica: `docker logs cerebro-postgres`

### "ModuleNotFoundError: No module named..."
- Las dependencias ya están instaladas en `.venv`
- Asegúrate de estar en el directorio correcto
- Reactiva el entorno: `.\.venv\Scripts\Activate.ps1`

---

## ✅ Siguiente Paso

**Instala Docker Desktop ahora** y luego ejecuta:

```powershell
.\start_postgres.ps1
.\init_database.ps1
cd backend
python server_v2.py
```

---

**Tiempo total estimado:** 10-15 minutos
