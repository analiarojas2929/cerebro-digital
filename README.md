# 🧠 Cerebro Digital

**Sistema Neural de Memoria Personal con IA**

Un asistente inteligente que recuerda tus conversaciones, las clasifica automáticamente y construye una red neuronal visual de tus memorias para crear un legado digital familiar.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.14+-green)
![React](https://img.shields.io/badge/react-18.2.0-61dafb)
![FastAPI](https://img.shields.io/badge/fastapi-0.141.1-009688)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Documentation](#-api-documentation)
- [Configuración](#-configuración)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🎯 Descripción

**Cerebro Digital** es un sistema de memoria personal inteligente que combina:

- 🤖 **IA Conversacional** con Kostra AI (DeepSeek v4)
- 🧠 **Red Neuronal Visual** interactiva y cronológica
- 📚 **Clasificación Automática** en 6 categorías principales
- 🔍 **Extracción de Entidades** (personas, lugares, eventos)
- 💬 **Sistema de Hilos** para comentar memorias
- ⏰ **Recordatorios y Expiración** de memorias
- 🎨 **Interfaz Moderna** con React + TailwindCSS

### 💡 Propósito

Crear un **legado digital familiar** donde puedas hablar sobre tu vida y el sistema:
- Recuerde automáticamente información importante
- Clasifique en categorías y subcategorías dinámicas
- Construya una red neuronal visual de conexiones
- Permita a tus familiares explorar tus memorias organizadas

---

## ✨ Características

### 🤖 IA Conversacional
- Integración con **Kostra AI** (modelo DeepSeek v4 Flash)
- Respuestas contextuales basadas en tu historial
- Comprensión de entidades y relaciones

### 🧠 Red Neuronal Visual
- **Visualización horizontal** con flujo cronológico (izquierda → derecha)
- **4 tipos de nodos**:
  - 🟦 Categorías principales
  - 🟨 Subcategorías
  - 🟩 Memorias originales
  - 🟣 Comentarios/Historia
- **Controles de Zoom** y centrado automático
- **Panel de estadísticas** en tiempo real
- **Deduplicación inteligente** de nodos

### 📊 Sistema de Categorización

**6 Categorías Principales:**
1. 👤 **Personal** - Notas generales y reflexiones
2. 💼 **Trabajo** - Proyectos, reuniones, tareas laborales
3. 👨‍👩‍👧‍👦 **Familia** - Personas, relaciones familiares
4. 🏠 **Lugares** - Ubicaciones, direcciones, sitios
5. 🎂 **Eventos** - Cumpleaños, celebraciones, hitos
6. 💭 **Emociones** - Sentimientos, estados de ánimo

**Subcategorías Dinámicas:**
- Detección automática de personas (María, Juan, etc.)
- Detección de lugares (Santiago, oficina, etc.)
- Detección de eventos (reunión, cumpleaños, etc.)
- Análisis de sentimientos y emociones

### 🔧 Gestión de Memorias
- ⭐ **Marcar como importante**
- 🗑️ **Eliminar** memorias obsoletas
- ⏰ **Recordatorios** programables
- 📅 **Fecha de expiración** automática
- 💬 **Comentar** sobre memorias existentes

---

## 📸 Capturas de Pantalla

### Chat Inteligente
Interfaz conversacional con respuestas contextuales de IA.

### Red Neuronal
Visualización interactiva de memorias organizadas cronológicamente.

### Sidebar Dinámico
Estadísticas y categorías que se actualizan en tiempo real.

---

## 🛠️ Tecnologías

### Backend
- **Python 3.14.2**
- **FastAPI 0.141.1** - Framework web moderno
- **Uvicorn 0.52.4** - Servidor ASGI
- **OpenAI SDK 3.3.1** - Cliente para Kostra AI
- **python-dotenv** - Gestión de variables de entorno

### Frontend
- **React 18.2.0** - Biblioteca UI
- **TypeScript 5.3.3** - Tipado estático
- **Vite 5.0.12** - Build tool y dev server
- **TailwindCSS 3.4.1** - Framework CSS
- **Zustand 4.5.0** - Gestión de estado
- **React Query** - Gestión de datos asíncronos
- **react-force-graph-2d** - Visualización de grafos
- **Lucide React** - Iconos modernos

### IA
- **Kostra AI** - Proveedor de IA
- **DeepSeek v4 Flash** - Modelo de lenguaje
- Base URL: `https://ai.kostra.cloud/v1`

---

## 📦 Instalación

### Requisitos Previos
- **Python 3.14+** instalado
- **Node.js 18+** y npm
- **Git** (opcional)

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd cerebro-digital
```

### 2. Configurar Backend

#### Crear entorno virtual
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Instalar dependencias
```powershell
pip install -r requirements.txt
```

#### Configurar variables de entorno
Crea un archivo `.env` en la carpeta `backend/`:
```env
KOSTRA_KEY=tu_api_key_aqui
APP_NAME=Cerebro Digital
```

### 3. Configurar Frontend
```powershell
cd ..\frontend
npm install
```

---

## 🚀 Uso

### Iniciar Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python server.py
```
El servidor estará disponible en: **http://localhost:8000**

### Iniciar Frontend
```powershell
cd frontend
npm run dev
```
La aplicación estará disponible en: **http://localhost:5175**

### Acceder a la Documentación de la API
Abre tu navegador en: **http://localhost:8000/docs**

---

## 📁 Estructura del Proyecto

```
cerebro-digital/
├── backend/
│   ├── venv/                    # Entorno virtual Python
│   ├── .env                     # Variables de entorno
│   ├── server.py               # Servidor FastAPI principal
│   ├── dynamic_learning.py     # Sistema de aprendizaje dinámico
│   ├── ai_chat.py              # Integración con Kostra AI
│   ├── requirements.txt        # Dependencias Python
│   └── schema.sql              # Schema DB (v2.0 futuro)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx      # Interfaz de chat
│   │   │   ├── NeuralNetwork.tsx      # Red neuronal visual
│   │   │   ├── Sidebar.tsx            # Panel lateral
│   │   │   └── MessageBubble.tsx      # Burbujas de mensaje
│   │   ├── services/
│   │   │   └── api.ts                 # Cliente API
│   │   ├── store/
│   │   │   └── chatStore.ts           # Store Zustand
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript types
│   │   ├── App.tsx                    # Componente principal
│   │   └── main.tsx                   # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── docs/                       # Documentación adicional
│   ├── INSTALACION_FINAL.md
│   ├── LLM_INTEGRATION.md
│   ├── COMO_ACTIVAR_IA.md
│   └── FAQ.md
│
├── README.md                   # Este archivo
├── LICENSE
└── ROADMAP.md
```

---

## 📡 API Documentation

### Endpoints Principales

#### **Chat**
- `POST /chat/message` - Enviar mensaje
  ```json
  {
    "message": "Texto del mensaje",
    "session_id": "uuid-opcional"
  }
  ```

#### **Memoria**
- `GET /memory/stats` - Estadísticas generales
- `GET /memory/categories` - Listar categorías dinámicas
- `GET /memory/neural-graph` - Datos para red neuronal
- `GET /memory/summary` - Resumen de categoría específica
- `GET /memory/{memory_id}` - Obtener memoria por ID

#### **Gestión de Memorias**
- `DELETE /memory/{memory_id}` - Eliminar memoria
- `PUT /memory/{memory_id}/importance` - Marcar como importante
- `PUT /memory/{memory_id}/reminder` - Establecer recordatorio
- `PUT /memory/{memory_id}/expiration` - Establecer expiración
- `GET /memory/reminders` - Listar recordatorios
- `GET /memory/expired` - Listar memorias caducadas

#### **Sistema de Hilos**
- `POST /memory/{memory_id}/comment` - Agregar comentario
- `GET /memory/{memory_id}/thread` - Obtener hilo completo

#### **Salud**
- `GET /health` - Estado del servidor

### Documentación Interactiva
Swagger UI: **http://localhost:8000/docs**

---

## ⚙️ Configuración

### Variables de Entorno (`backend/.env`)

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `KOSTRA_KEY` | API Key de Kostra AI | ✅ Sí |
| `APP_NAME` | Nombre de la aplicación | ❌ No |
| `DATABASE_URL` | URL PostgreSQL (v2.0) | ❌ No |

### Obtener API Key de Kostra
1. Visita [kostra.cloud](https://kostra.cloud)
2. Crea una cuenta gratuita
3. Genera una API key
4. Copia la key al archivo `.env`

---

## 🗺️ Roadmap

### ✅ v1.0 - Sistema Base (Actual)
- [x] Chat con IA (Kostra)
- [x] Clasificación automática
- [x] Red neuronal visual
- [x] Gestión de memorias
- [x] Sistema de hilos
- [x] Almacenamiento en memoria

### 🔄 v2.0 - Persistencia (Planeado)
- [ ] PostgreSQL + pgvector
- [ ] Embeddings con sentence-transformers
- [ ] Búsqueda semántica
- [ ] Autenticación de usuarios
- [ ] Multi-usuario

### 🚀 v3.0 - Avanzado (Futuro)
- [ ] Exportar/importar memorias
- [ ] Timeline visual interactivo
- [ ] Estadísticas avanzadas
- [ ] Temas personalizables
- [ ] PWA (Progressive Web App)
- [ ] API pública documentada

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más información.

---

## 👥 Autores

- **Desarrollador Principal** - Cerebro Digital Team

---

## 🙏 Agradecimientos

- **Kostra AI** por proporcionar acceso a modelos de IA asequibles
- **DeepSeek** por el modelo v4 Flash
- **FastAPI** por el excelente framework
- **React** y **Vite** por las herramientas modernas de desarrollo
- Comunidad de código abierto

---

## 📞 Soporte

- 📧 **Email**: soporte@cerebrodigital.com
- 💬 **Discord**: [Link al servidor]
- 📖 **Docs**: Ver carpeta `docs/`
- 🐛 **Issues**: [GitHub Issues](https://github.com/usuario/cerebro-digital/issues)

---

## 🌟 Características Destacadas

### 🎨 Interfaz Moderna
- Diseño con gradientes y sombras
- Animaciones fluidas
- Responsive design
- Modo oscuro por defecto

### 🧪 Extracción de Entidades
El sistema detecta automáticamente:
- **Personas**: Mamá, papá, nombres propios
- **Lugares**: Ciudades, direcciones, locaciones
- **Eventos**: Reuniones, cumpleaños, celebraciones
- **Emociones**: Feliz, triste, motivado, etc.

### 🔗 Red Neuronal Inteligente
- Layout horizontal cronológico
- Conexiones automáticas entre memorias
- Colores por tipo de nodo
- Zoom y navegación interactiva
- Sin duplicados garantizado

---

## 💻 Desarrollo

### Comandos Útiles

#### Backend
```powershell
# Activar entorno virtual
.\backend\venv\Scripts\Activate.ps1

# Instalar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Ejecutar servidor
python server.py
```

#### Frontend
```powershell
# Instalar nueva dependencia
npm install nombre-paquete

# Ejecutar en desarrollo
npm run dev

# Build para producción
npm run build

# Preview build
npm run preview
```

### Tests
```powershell
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~3,000+
- **Componentes React**: 4 principales
- **Endpoints API**: 15+
- **Categorías**: 6 principales
- **Tipos de nodos**: 4 en red neuronal

---

**¡Gracias por usar Cerebro Digital! 🧠✨**

*Construyendo memorias, creando legados.*
