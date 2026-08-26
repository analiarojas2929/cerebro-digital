# ⚠️ PROBLEMA: Docker requiere virtualización

## 🔴 Situación Actual

Docker Desktop no puede iniciar porque **la virtualización no está habilitada** en tu PC.

```
Error: Virtualization support not detected
```

## ✅ Soluciones Disponibles

### Opción 1: Habilitar Virtualización (MEJOR - Usa Docker)

**Pasos:**

1. **Reinicia tu PC**
2. **Entra al BIOS** (presiona una de estas teclas al iniciar):
   - `F2` (Dell, Lenovo)
   - `DEL` (ASUS, MSI)
   - `F10` (HP)
   - `ESC` (Acer)
3. **Busca y habilita:**
   - "Intel VT-x" o "Intel Virtualization Technology" (Intel)
   - "AMD-V" o "SVM Mode" (AMD)
   - Ubicación común: `Advanced → CPU Configuration`
4. **Guarda y sale** (F10 → Yes)
5. **Inicia Windows**
6. **Abre Docker Desktop** - debería funcionar ahora

**Ventajas:**
- ✅ Instalación más fácil
- ✅ PostgreSQL + pgvector listo
- ✅ Sistema v2.0 completo

---

### Opción 2: PostgreSQL Local (SIN Docker) ⚡

**Usar PostgreSQL nativo de Windows (sin virtualización)**

#### Paso 1: Descargar PostgreSQL

```powershell
# Abrir página de descarga
Start-Process "https://www.enterprisedb.com/downloads/postgres-postgresql-downloads"
```

**Durante instalación:**
- Password: `postgres`
- Puerto: `5432`
- Incluir Stack Builder: ✅ Sí

#### Paso 2: Ejecutar script

```powershell
.\install_postgres_local.ps1
```

Este script:
- ✅ Verifica PostgreSQL instalado
- ✅ Crea base de datos `cerebro_digital`
- ✅ Configura `.env`
- ⚠️ pgvector manual (opcional)

#### Paso 3: Inicializar

```powershell
cd backend
python app\core\db_manager.py
python server_v2.py
```

**Ventajas:**
- ✅ Funciona AHORA (sin reiniciar)
- ✅ No requiere virtualización
- ✅ PostgreSQL nativo es más rápido

**Limitaciones:**
- ⚠️ pgvector requiere compilación manual (opcional)
- ⚠️ Sin búsqueda semántica hasta instalar pgvector
- ✅ Todo lo demás funciona perfectamente

---

### Opción 3: Seguir con Sistema Actual (Ya Funciona)

Tu sistema v1.0 **está funcionando ahora**:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5175`

```powershell
# Ya está corriendo, solo abre
Start-Process "http://localhost:5175"
```

**Ventajas:**
- ✅ Funciona perfectamente
- ✅ Red neuronal visual
- ✅ Comentarios y threading

**Limitaciones:**
- ❌ Datos se pierden al reiniciar

---

## 🎯 Recomendación

### Si tienes 10 minutos → **Opción 1** (Habilitar virtualización)
- Mejor solución a largo plazo
- Docker hace todo automático
- Sistema v2.0 completo

### Si necesitas usar AHORA → **Opción 2** (PostgreSQL local)
- Instala PostgreSQL Windows (10 min)
- Ejecuta `.\install_postgres_local.ps1`
- Sistema v2.0 funcionando (sin búsqueda semántica)

### Si quieres probar primero → **Opción 3** (Sistema actual)
- Ya funciona
- Úsalo para ver si te gusta
- Migra después a v2.0

---

## 📋 Comparación

| | Opción 1 (Docker) | Opción 2 (PostgreSQL Local) | Opción 3 (Actual) |
|---|---|---|---|
| **Tiempo** | 15 min (reinicio) | 15 min (sin reinicio) | 0 min ✅ |
| **Virtualización** | ⚠️ Requiere | ✅ No requiere | ✅ No requiere |
| **Persistencia** | ✅ PostgreSQL | ✅ PostgreSQL | ❌ In-memory |
| **Búsqueda Semántica** | ✅ pgvector | ⚠️ Manual | ❌ No |
| **Chat IA** | ✅ OpenAI | ✅ OpenAI | ⚠️ Básico |

---

## 🚀 Acción Inmediata

**Ejecuta UNO de estos:**

```powershell
# Opción 1: Configurar BIOS (mejor a largo plazo)
# → Reinicia → F2/DEL → Habilita VT-x/AMD-V → Guarda

# Opción 2: PostgreSQL local (funciona ahora)
Start-Process "https://www.enterprisedb.com/downloads/postgres-postgresql-downloads"
# Después de instalar:
.\install_postgres_local.ps1

# Opción 3: Usa el sistema actual
Start-Process "http://localhost:5175"
```

---

¿Qué opción prefieres?
