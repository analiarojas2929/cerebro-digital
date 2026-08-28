# 🔐 Sistema de Autenticación Multi-Usuario

**Cerebro Digital ahora soporta múltiples usuarios** con sesiones aisladas e independientes.

---

## 📋 ¿Qué cambió?

### ✅ Antes (v1.0):
- Un solo sistema de memoria compartido
- Sin login
- Todos los datos mezclados

### ✨ Ahora (v1.1):
- **Múltiples usuarios** con cuentas individuales
- **Login y Registro**
- **Datos completamente aislados** por usuario
- **Sesiones persistentes** con tokens JWT

---

## 🚀 Cómo Usar

### 1. Iniciar el Servidor con Autenticación

```powershell
cd backend
python server.py
```

El servidor iniciará en `http://localhost:8000` con autenticación habilitada.

### 2. Iniciar el Frontend

```powershell
cd frontend
npm run dev
```

### 3. Crear Cuenta o Iniciar Sesión

Al abrir la app verás la **pantalla de login**.

#### Usuarios Demo (para testing):
- **Usuario**: `demo` / **Contraseña**: `demo123`
- **Usuario**: `admin` / **Contraseña**: `admin123`

#### O crear tu propia cuenta:
1. Click en "Regístrate aquí"
2. Completar formulario
3. ¡Listo! Acceso inmediato

---

## 🔧 Arquitectura Técnica

### Backend

#### Nuevos Archivos:

**`backend/auth.py`**
- Gestión de usuarios (crear, login, tokens)
- Hash de contraseñas (SHA256)
- Tokens JWT con expiración de 7 días
- Sesiones aisladas por usuario

**`backend/server.py`**
- Servidor FastAPI con autenticación
- Endpoints protegidos
- Middleware de autenticación

#### Nuevos Endpoints:

```
POST /auth/register
  Body: { username, email, password, full_name }
  Returns: { access_token, token_type, user_info }

POST /auth/login
  Body: { username, password }
  Returns: { access_token, token_type, user_info }

GET /auth/me
  Headers: Authorization: Bearer <token>
  Returns: { username, email, full_name, disabled }
```

#### Endpoints Protegidos (requieren token):

```
POST /chat/message
GET /memory/stats
GET /memory/categories
GET /memory/neural-graph
... (todos los endpoints excepto /health)
```

### Frontend

#### Nuevos Archivos:

**`frontend/src/store/authStore.ts`**
- Store Zustand para autenticación
- Persistencia en localStorage
- Login/logout automático

**`frontend/src/components/Login.tsx`**
- Pantalla de inicio de sesión
- Validación de credenciales
- Manejo de errores

**`frontend/src/components/Register.tsx`**
- Pantalla de registro
- Validación de formulario
- Confirmación de contraseña

**`frontend/src/services/apiClient.ts`**
- Cliente HTTP con interceptores
- Inyección automática de token
- Manejo de errores 401

---

## 🔐 Seguridad

### Características de Seguridad:

- ✅ **Contraseñas hasheadas** (SHA256)
- ✅ **Tokens JWT** con expiración
- ✅ **Headers Authorization** estándar
- ✅ **Validación en cada request**
- ✅ **Sesiones aisladas** por usuario
- ✅ **Logout automático** si el token expira

### ⚠️ Para Producción:

Antes de deployar:

1. **Cambiar SECRET_KEY** en `backend/auth.py`:
   ```python
   SECRET_KEY = "generar_clave_secreta_aleatoria_aqui"
   ```
   
   Generar con:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **Usar base de datos real** (PostgreSQL):
   - Actualmente los usuarios están en memoria (se pierden al reiniciar)
   - Implementar persistencia con SQLAlchemy

3. **HTTPS obligatorio** en producción

4. **Configurar CORS** con dominios específicos:
   ```python
   allow_origins=["https://tu-dominio.com"]
   ```

---

## 📊 Estructura de Datos

### Usuario:

```python
{
  "username": "juan123",
  "email": "juan@example.com",
  "full_name": "Juan Pérez",
  "user_id": "uuid-unico",
  "hashed_password": "hash_sha256",
  "created_at": "2026-08-27T10:30:00",
  "disabled": false
}
```

### Sesión de Usuario:

```python
{
  "user_id": "uuid",
  "dynamic_categories": {},  # Categorías del usuario
  "memory_threads": {},      # Hilos de comentarios
  "memory_index": {},        # Índice de memorias
  "conversations": []        # Historial de chat
}
```

Cada usuario tiene **su propia sesión completamente aislada**.

---

## 🔄 Migración desde v1.0

### Opción 1: Empezar de Cero
- Todos los usuarios crean cuentas nuevas
- Datos viejos se descartan

### Opción 2: Migrar Datos
- Crear cuenta para usuario principal
- Importar datos antiguos a esa cuenta
- Script de migración (próximamente)

---

## 🧪 Testing

### Probar localmente:

```powershell
# Terminal 1: Backend
cd backend
python server.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Abrir navegador en http://localhost:5173
```

### Crear usuarios de prueba:

```python
# En auth.py, descomentar:
initialize_demo_users()
```

---

## 📝 API Usage

### Ejemplo con curl:

#### Registro:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "usuario@example.com",
    "password": "contraseña123",
    "full_name": "Nombre Completo"
  }'
```

#### Login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "password": "contraseña123"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_info": {
    "username": "nuevo_usuario",
    "email": "usuario@example.com",
    "full_name": "Nombre Completo"
  }
}
```

#### Usar el token:
```bash
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token_aqui>" \
  -d '{
    "message": "Hola Cerebro Digital"
  }'
```

---

## 🔧 Troubleshooting

### Error: "No autenticado" (401)

**Causa**: Token no enviado o inválido
**Solución**: 
- Verificar que el header `Authorization: Bearer <token>` esté presente
- Verificar que el token no haya expirado
- Hacer login nuevamente

### Error: "Usuario ya existe"

**Causa**: Username o email ya registrados
**Solución**: Usar otro username/email

### Frontend no guarda la sesión

**Causa**: localStorage deshabilitado
**Solución**: Habilitar cookies/localStorage en el navegador

### Los datos no persisten al reiniciar

**Causa**: Base de datos en memoria (v1.1)
**Solución**: Esperar v2.0 con PostgreSQL o implementar manualmente

---

## 🗺️ Roadmap

### v1.1 (Actual):
- ✅ Login y registro
- ✅ Autenticación con JWT
- ✅ Sesiones aisladas
- ⚠️ Datos en memoria (no persistentes)

### v2.0 (Próximamente):
- [ ] PostgreSQL para persistencia
- [ ] Recuperación de contraseña
- [ ] Perfil de usuario editable
- [ ] Roles y permisos
- [ ] Compartir memorias entre usuarios
- [ ] OAuth (Google, GitHub)

---

## 📚 Referencias

- [JWT.io](https://jwt.io) - Aprender sobre JWT
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) - Docs oficiales
- [Zustand](https://zustand-demo.pmnd.rs/) - State management

---

**¡Cerebro Digital Multi-Usuario! 🧠👥**

Cada usuario tiene su propio espacio privado de memoria.
