# 🚀 Inicio Rápido - Deploy en Render (5 minutos)

La forma MÁS FÁCIL de desplegar Cerebro Digital en la nube **GRATIS**.

---

## ⚡ Pasos Rápidos

### 1. Push a GitHub (Ya hecho ✅)

Tu código ya está en: `https://github.com/analiarojas2929/cerebro-digital`

### 2. Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Click en **"Get Started"**
3. Registrarse con **GitHub** (más fácil)

### 3. Conectar Repositorio

1. En Render Dashboard: **"New +" → "Blueprint"**
2. **Connect GitHub** y autorizar
3. Seleccionar repositorio: **`cerebro-digital`**
4. Render detectará automáticamente el archivo `render.yaml`

### 4. Configurar Variables de Entorno

**IMPORTANTE**: Antes de hacer deploy, configurar:

1. Click en **"cerebro-digital-backend"**
2. Ir a **"Environment"**
3. Agregar variables:
   ```
   KOSTRA_KEY = sk-OACzL1DBvIicxvS779iUhw
   APP_NAME = Cerebro Digital
   ```

### 5. Deploy 🚀

1. Click en **"Apply"** o **"Create Blueprint Instance"**
2. Esperar ~5-10 minutos (la primera vez)
3. ✅ ¡Listo!

---

## 📍 URLs de tu App

Después del deploy, tendrás:

- **Backend**: `https://cerebro-digital-backend.onrender.com`
  - Probar: `https://cerebro-digital-backend.onrender.com/health`
  
- **Frontend**: `https://cerebro-digital-frontend.onrender.com`
  - Abrir en navegador y usar tu Cerebro Digital

---

## 🔧 Actualizar Código

Cada vez que hagas `git push`:

```powershell
git add .
git commit -m "Actualización"
git push
```

**Render automáticamente re-desplegará** en ~2-3 minutos.

---

## ⚠️ Importante

### El plan gratuito de Render:

- ✅ **750 horas/mes** (suficiente para 1 app 24/7)
- ⚠️ **Se duerme después de 15 min sin uso** (primer request tarda ~30s en despertar)
- ✅ **HTTPS gratuito**
- ✅ **Deploy automático desde GitHub**

### Para evitar que se duerma:

Usar servicio como [UptimeRobot](https://uptimerobot.com) (gratis) para hacer ping cada 5 minutos:
- URL a monitorear: `https://cerebro-digital-backend.onrender.com/health`

---

## 🆘 Troubleshooting

### ❌ Error: "Build failed"

**Causa**: Falta alguna dependencia
**Solución**:
1. Verificar `backend/requirements.txt`
2. Verificar `frontend/package.json`
3. Ver logs en Render Dashboard

### ❌ Error: "Application failed to respond"

**Causa**: KOSTRA_KEY no configurada
**Solución**:
1. Render → Backend → Environment
2. Agregar `KOSTRA_KEY`
3. Click "Manual Deploy" → "Deploy latest commit"

### ❌ Error: "CORS blocked"

**Causa**: Frontend intenta conectar a backend con URL incorrecta
**Solución**:
1. Frontend → Environment variables
2. Agregar: `VITE_API_URL = https://cerebro-digital-backend.onrender.com`
3. Redeploy frontend

### ❌ Frontend carga pero no conecta con backend

**Verificar**:
1. Backend está corriendo: `https://cerebro-digital-backend.onrender.com/health`
2. Ver Network tab en navegador (F12)
3. Verificar que la URL del API sea correcta

---

## 📊 Monitoreo

### Ver Logs:

1. Render Dashboard
2. Click en servicio (backend o frontend)
3. Tab **"Logs"**
4. Ver en tiempo real

### Estado del Servicio:

- 🟢 **Running**: Todo bien
- 🟡 **Building**: Desplegando
- 🔴 **Failed**: Ver logs para error

---

## 💡 Próximos Pasos

Una vez funcionando en la nube:

1. ✅ **Dominio personalizado** (opcional):
   - Render → Settings → Custom Domain
   - Ejemplo: `cerebro.tu-dominio.com`

2. ✅ **Base de datos PostgreSQL** (v2.0):
   - Render → New → PostgreSQL
   - Conectar con `DATABASE_URL`

3. ✅ **Backup automático**:
   - Configurar GitHub Actions
   - Exportar datos periódicamente

---

## 🎯 Checklist Final

Antes de usar en producción:

- [ ] Backend responde: `/health` → `{"status": "healthy"}`
- [ ] Frontend carga correctamente
- [ ] Puedes enviar mensajes y recibir respuestas
- [ ] Red neuronal se visualiza
- [ ] Categorías se actualizan
- [ ] KOSTRA_KEY configurada correctamente
- [ ] CORS configurado con tu dominio

---

## 📚 Más Opciones

Si Render no te funciona o quieres explorar otras opciones:

- Ver **[DEPLOYMENT_CLOUD.md](DEPLOYMENT_CLOUD.md)** para:
  - Railway (más rápido pero pagado)
  - Fly.io (Docker, más control)
  - Vercel + Render (mejor rendimiento)
  - VPS (control total)

---

**¡Tu Cerebro Digital en la nube en 5 minutos! 🧠☁️**

¿Problemas? Revisar [FAQ.md](FAQ.md) o abrir un Issue en GitHub.
