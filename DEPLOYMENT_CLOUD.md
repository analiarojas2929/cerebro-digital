# ☁️ Guía de Deployment en la Nube

Guía completa para desplegar **Cerebro Digital** en diferentes plataformas cloud.

---

## 📋 Tabla de Contenidos

- [Opción 1: Render (Recomendado - Gratis)](#opción-1-render-recomendado---gratis)
- [Opción 2: Railway (Fácil - Gratis con límites)](#opción-2-railway-fácil---gratis-con-límites)
- [Opción 3: Fly.io (Docker - Gratis)](#opción-3-flyio-docker---gratis)
- [Opción 4: Vercel + Render (Separado)](#opción-4-vercel--render-separado)
- [Opción 5: VPS (DigitalOcean/Linode)](#opción-5-vps-digitaloceanlinode)
- [Preparación Común](#preparación-común)

---

## 🎯 Comparación Rápida

| Plataforma | Dificultad | Costo | Backend | Frontend | Base de Datos |
|------------|------------|-------|---------|----------|---------------|
| **Render** | ⭐ Fácil | Gratis | ✅ | ✅ | ✅ PostgreSQL |
| **Railway** | ⭐ Fácil | $5/mes | ✅ | ✅ | ✅ PostgreSQL |
| **Fly.io** | ⭐⭐ Media | Gratis | ✅ | ✅ | ❌ |
| **Vercel+Render** | ⭐⭐ Media | Gratis | ✅ | ✅ | ✅ |
| **VPS** | ⭐⭐⭐ Difícil | $5-10/mes | ✅ | ✅ | ✅ |

---

## 🚀 Preparación Común

### 1. Actualizar `.gitignore`

Asegúrate de tener esto en tu `.gitignore`:

```gitignore
# Entorno virtual
venv/
.venv/
backend/venv/

# Variables de entorno
.env
*.env

# Node modules
node_modules/
frontend/node_modules/

# Build
frontend/dist/
frontend/build/

# Cache
__pycache__/
*.pyc
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
```

### 2. Crear archivo de configuración para producción

**`backend/requirements.txt`** - Ya lo tienes, verificar que incluya:
```txt
fastapi==0.141.1
uvicorn[standard]==0.52.4
openai==3.3.1
python-dotenv==1.0.0
pydantic==2.10.4
```

### 3. Configurar CORS para producción

Edita `backend/server.py` para permitir tu dominio:

```python
# CORS - Actualizar con tu dominio en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "https://tu-app.onrender.com",  # Agregar tu dominio
        "https://cerebro-digital.vercel.app"  # Si usas Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🟢 Opción 1: Render (Recomendado - Gratis)

**Ventajas:**
- ✅ 100% Gratis para proyectos pequeños
- ✅ PostgreSQL incluido gratis
- ✅ Deploy automático desde GitHub
- ✅ HTTPS gratuito
- ✅ Muy fácil de configurar

### Paso 1: Preparar el proyecto

#### Crear `render.yaml` en la raíz:

```yaml
services:
  # Backend FastAPI
  - type: web
    name: cerebro-digital-backend
    runtime: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: KOSTRA_KEY
        sync: false
      - key: APP_NAME
        value: Cerebro Digital
      - key: PYTHON_VERSION
        value: 3.14.2

  # Frontend React
  - type: web
    name: cerebro-digital-frontend
    runtime: node
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    envVars:
      - key: VITE_API_URL
        value: https://cerebro-digital-backend.onrender.com

databases:
  - name: cerebro-db
    databaseName: cerebro_digital
    user: cerebro
```

#### Actualizar `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/chat': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
      '/memory': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### Paso 2: Deploy en Render

1. **Crear cuenta**: Ve a [render.com](https://render.com)
2. **Conectar GitHub**: Autoriza acceso a tu repositorio
3. **Crear servicios**:
   - Click en "New" → "Blueprint"
   - Selecciona tu repositorio `cerebro-digital`
   - Render detectará el `render.yaml`
   - Configurar variables de entorno:
     - `KOSTRA_KEY`: Tu API key de Kostra
4. **Deploy**: Click en "Apply" y esperar ~5-10 minutos

### Paso 3: Configurar variables de entorno

En Render Dashboard:
- Backend → Environment → Add:
  - `KOSTRA_KEY` = tu_api_key
  - `DATABASE_URL` = (auto-generada si creaste PostgreSQL)

### URLs finales:
- **Backend**: `https://cerebro-digital-backend.onrender.com`
- **Frontend**: `https://cerebro-digital-frontend.onrender.com`

---

## 🚂 Opción 2: Railway (Fácil - Gratis con límites)

**Ventajas:**
- ✅ Interfaz muy intuitiva
- ✅ Deploy desde GitHub en segundos
- ✅ PostgreSQL incluido
- ✅ $5 crédito gratis/mes

### Paso 1: Preparar archivos

#### Crear `Procfile` en la raíz:

```
web: cd backend && uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
```

#### Crear `nixpacks.toml` en la raíz:

```toml
[phases.setup]
nixPkgs = ['python314', 'nodejs-18_x']

[phases.install]
cmds = [
  'cd backend && pip install -r requirements.txt',
  'cd frontend && npm install && npm run build'
]

[start]
cmd = 'cd backend && uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}'
```

### Paso 2: Deploy en Railway

1. **Crear cuenta**: [railway.app](https://railway.app)
2. **New Project** → "Deploy from GitHub repo"
3. **Seleccionar** `cerebro-digital`
4. **Add PostgreSQL**: Click en "+ New" → "Database" → "PostgreSQL"
5. **Variables de entorno**:
   - `KOSTRA_KEY` = tu_api_key
   - `DATABASE_URL` = (auto-generada)

### Paso 3: Frontend en Railway

1. **Add service** → "Frontend"
2. **Build Command**: `cd frontend && npm install && npm run build`
3. **Start Command**: `npx vite preview --host 0.0.0.0 --port $PORT`
4. **Variable**: `VITE_API_URL` = URL del backend

---

## 🛫 Opción 3: Fly.io (Docker - Gratis)

**Ventajas:**
- ✅ Usa Docker (más control)
- ✅ Gratis para proyectos pequeños
- ✅ Deploy global (edge computing)

### Paso 1: Instalar Fly CLI

```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Paso 2: Login y crear app

```powershell
fly auth login
fly launch --name cerebro-digital
```

### Paso 3: Configurar `fly.toml`

```toml
app = "cerebro-digital"
primary_region = "mia"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"
  APP_NAME = "Cerebro Digital"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

[http_service]
  internal_port = 8000
  force_https = true
```

### Paso 4: Crear Dockerfile multi-stage en raíz

```dockerfile
# Build frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Build backend
FROM python:3.14-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
COPY --from=frontend-build /app/frontend/dist ./static

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Paso 5: Deploy

```powershell
fly secrets set KOSTRA_KEY=tu_api_key
fly deploy
```

---

## ⚡ Opción 4: Vercel + Render (Separado)

**Ventajas:**
- ✅ Frontend ultra-rápido en Vercel
- ✅ Backend en Render gratis
- ✅ Mejor rendimiento

### Backend en Render (ver Opción 1)

### Frontend en Vercel

1. **Instalar Vercel CLI**:
   ```powershell
   npm install -g vercel
   ```

2. **Desde `frontend/`**:
   ```powershell
   cd frontend
   vercel login
   vercel
   ```

3. **Configurar variables**:
   ```powershell
   vercel env add VITE_API_URL production
   # Pegar: https://cerebro-digital-backend.onrender.com
   ```

4. **Deploy**:
   ```powershell
   vercel --prod
   ```

---

## 💻 Opción 5: VPS (DigitalOcean/Linode)

**Para control total y mejor rendimiento**

### Paso 1: Crear Droplet/VPS

1. **DigitalOcean**: Crear Droplet Ubuntu 22.04 ($5/mes)
2. **SSH**: Conectar a tu servidor

### Paso 2: Instalar dependencias

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.14
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.14 python3.14-venv python3-pip -y

# Instalar Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Instalar Nginx
sudo apt install nginx -y

# Instalar PostgreSQL (opcional)
sudo apt install postgresql postgresql-contrib -y
```

### Paso 3: Clonar y configurar

```bash
# Clonar proyecto
git clone git@github.com:analiarojas2929/cerebro-digital.git
cd cerebro-digital

# Backend
cd backend
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Crear .env
cat > .env << EOF
KOSTRA_KEY=tu_api_key_aqui
APP_NAME=Cerebro Digital
EOF

# Frontend
cd ../frontend
npm install
npm run build
```

### Paso 4: Configurar servicio systemd

**`/etc/systemd/system/cerebro-backend.service`**:

```ini
[Unit]
Description=Cerebro Digital Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/home/tu-usuario/cerebro-digital/backend
Environment="PATH=/home/tu-usuario/cerebro-digital/backend/venv/bin"
ExecStart=/home/tu-usuario/cerebro-digital/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Paso 5: Configurar Nginx

**`/etc/nginx/sites-available/cerebro-digital`**:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        root /home/tu-usuario/cerebro-digital/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /chat {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /memory {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Paso 6: Iniciar servicios

```bash
# Habilitar servicio
sudo systemctl enable cerebro-backend
sudo systemctl start cerebro-backend

# Configurar Nginx
sudo ln -s /etc/nginx/sites-available/cerebro-digital /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 7: HTTPS con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

---

## 🔧 Configuración Post-Deploy

### Actualizar API URL en Frontend

**`frontend/src/services/api.ts`**:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 
                import.meta.env.PROD 
                  ? 'https://cerebro-digital-backend.onrender.com'
                  : 'http://localhost:8000';
```

### Monitoreo y Logs

**Render**: Dashboard → Logs
**Railway**: Dashboard → Deployments → Logs
**Fly.io**: `fly logs`
**VPS**: `journalctl -u cerebro-backend -f`

---

## 📊 Resumen de Costos

| Plataforma | Gratis | Pagado |
|------------|--------|--------|
| Render | ✅ 750h/mes | $7/mes (hobby) |
| Railway | ✅ $5 crédito/mes | $5-20/mes |
| Fly.io | ✅ 3 VMs pequeñas | $5-10/mes |
| Vercel | ✅ Ilimitado frontend | $20/mes (Pro) |
| VPS | ❌ | $5-10/mes |

---

## 🎯 Recomendación Final

### Para Empezar:
**Render** (Opción 1) - Gratis y completo

### Para Producción Seria:
**Railway** o **VPS** - Mejor control y rendimiento

### Para Máximo Rendimiento:
**Vercel (Frontend) + Render (Backend)** - Lo mejor de ambos mundos

---

## ❓ Troubleshooting

### Error: "Port already in use"
```bash
# Verificar proceso
lsof -i :8000
# Matar proceso
kill -9 <PID>
```

### Error: "Module not found"
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "CORS blocked"
- Verificar `allow_origins` en `server.py`
- Agregar dominio de producción

### Base de datos no conecta
- Verificar `DATABASE_URL` en variables de entorno
- Usar PostgreSQL connection string completo

---

## 📚 Recursos Adicionales

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Fly.io Docs](https://fly.io/docs)
- [Vercel Docs](https://vercel.com/docs)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)

---

**¡Tu Cerebro Digital en la nube! ☁️🧠**
