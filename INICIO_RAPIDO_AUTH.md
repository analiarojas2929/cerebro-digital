# 🚀 Inicio Rápido - Cerebro Digital con Autenticación

**5 minutos para tener tu Cerebro Digital Multi-Usuario funcionando**

---

## 📦 Requisitos

- Python 3.8+ instalado
- Node.js 18+ instalado
- PowerShell (Windows) o Terminal (Mac/Linux)

---

## ⚡ Pasos

### 1️⃣ Clonar o Navegar al Proyecto

```powershell
cd C:\Users\anali\Desktop\cerebro-digital
```

### 2️⃣ Configurar Backend (30 segundos)

```powershell
cd backend

# Crear entorno virtual (si no existe)
python -m venv venv

# Activar
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Iniciar Backend con Autenticación (10 segundos)

```powershell
# Asegúrate de estar en backend/
python server.py
```

✅ Verás:
```
🧠 Cerebro Digital Multi-Usuario v1.1
📡 Servidor con autenticación iniciando...
👥 Usuarios demo disponibles:
   - username: demo, password: demo123
   - username: admin, password: admin123

INFO:     Uvicorn running on http://0.0.0.0:8000
```

**¡No cierres esta terminal!**

### 4️⃣ Configurar Frontend (30 segundos)

**Abre NUEVA terminal**:

```powershell
cd C:\Users\anali\Desktop\cerebro-digital\frontend

# Instalar dependencias (primera vez)
npm install

# Agregar dependencia para persistencia de auth
npm install zustand
```

### 5️⃣ Iniciar Frontend (10 segundos)

```powershell
# Asegúrate de estar en frontend/
npm run dev
```

✅ Verás:
```
VITE v5.0.12  ready in 543 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 6️⃣ Abrir en Navegador

**Abre**: http://localhost:5173

Verás la **pantalla de login** 🔐

---

## 🎮 Usar la App

### Opción 1: Usuarios Demo

En la pantalla de login:

- **Usuario**: `demo`
- **Contraseña**: `demo123`

Click en **"Iniciar Sesión"**

### Opción 2: Crear Tu Cuenta

1. Click en **"Regístrate aquí"**
2. Completar:
   - Nombre completo
   - Usuario (único)
   - Email
   - Contraseña (mínimo 6 caracteres)
   - Confirmar contraseña
3. Click en **"Crear Cuenta"**

✅ **¡Automáticamente inicias sesión!**

---

## 💬 Probar el Sistema

Una vez dentro:

1. **Escribe un mensaje**:
   ```
   Hoy trabajé en un proyecto de IA muy interesante
   ```

2. **El sistema aprenderá**:
   - Clasificará como "Trabajo"
   - Creará categorías automáticamente
   - Generará respuesta con IA

3. **Ver red neuronal**:
   - Click en **"Red Neuronal"**
   - Explora nodos y conexiones
   - Zoom in/out, estadísticas

4. **Gestionar memorias**:
   - Click en nodos para opciones
   - Marcar como importante
   - Agregar recordatorios
   - Establecer caducidad

---

## 👥 Probar Multi-Usuario

### En navegador normal:
- Login como `demo`

### En ventana incógnito:
- Login como `admin`

**✨ Cada usuario tiene memorias completamente separadas**

---

## 🛑 Detener la App

### Backend:
```powershell
Ctrl + C en la terminal de backend
```

### Frontend:
```powershell
Ctrl + C en la terminal de frontend
```

---

## 🔄 Reiniciar

```powershell
# Terminal 1 (Backend)
cd backend
.\venv\Scripts\Activate.ps1
python server.py

# Terminal 2 (Frontend)
cd frontend
npm run dev
```

---

## ⚠️ Problemas Comunes

### ❌ Puerto 8000 ocupado

```powershell
# Ver qué proceso usa el puerto
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Matar el proceso
Stop-Process -Id <NUMERO_DEL_PROCESO>
```

### ❌ "Module not found: auth"

**Causa**: El servidor no se inició desde la carpeta `backend/`

**Solución**:
```powershell
python server.py  # ✅ Correcto
```

### ❌ Frontend no conecta

**Verifica**:
1. Backend corriendo en puerto 8000
2. Frontend corriendo en puerto 5173
3. No hay errores en consola del navegador

### ❌ "No autenticado" (401)

**Causa**: Token expiró o no se guardó

**Solución**:
1. Hacer logout
2. Volver a iniciar sesión

---

## 📂 Estructura Rápida

```
cerebro-digital/
├── backend/
│   ├── server.py           ← Servidor con auth
│   ├── auth.py             ← 🆕 Sistema de usuarios
│   ├── dynamic_learning.py
│   ├── ai_chat.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.tsx        ← 🆕 Pantalla login
│   │   │   ├── Register.tsx     ← 🆕 Pantalla registro
│   │   │   ├── ChatInterface.tsx
│   │   │   └── NeuralNetwork.tsx
│   │   ├── store/
│   │   │   ├── authStore.ts     ← 🆕 State de auth
│   │   │   └── chatStore.ts
│   │   └── services/
│   │       ├── apiClient.ts     ← 🆕 Con tokens JWT
│   │       └── api.ts
│   └── package.json
└── AUTENTICACION.md        ← 🆕 Documentación completa
```

---

## 🎯 Siguiente Paso

**Leer**: [AUTENTICACION.md](AUTENTICACION.md) para:
- Arquitectura técnica
- API endpoints
- Seguridad
- Deployment en producción
- Troubleshooting avanzado

---

## 💡 Tips

1. **Usuarios demo** son perfectos para testing
2. **Cada usuario** ve solo SUS memorias
3. **El token dura 7 días** - después debes volver a login
4. **Datos en memoria** - se pierden al reiniciar (v1.1)
5. **v2.0 tendrá PostgreSQL** para persistencia real

---

**¡Disfruta tu Cerebro Digital Multi-Usuario! 🧠✨**

*Creado con ❤️ para preservar memorias familiares*
