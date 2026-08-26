# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Cerebro Digital! Este documento te guiará en el proceso.

## 📋 Código de Conducta

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Enfócate en lo que es mejor para la comunidad
- Muestra empatía hacia otros miembros

## 🚀 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no haya sido reportado antes
2. Abre un issue con:
   - Título descriptivo
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Versión del sistema

### Sugerir Características

1. Abre un issue etiquetado como "feature request"
2. Describe claramente:
   - El problema que resuelve
   - La solución propuesta
   - Alternativas consideradas
   - Impacto esperado

### Pull Requests

1. Fork el repositorio
2. Crea una rama desde `main`:
   ```bash
   git checkout -b feature/nombre-caracteristica
   git checkout -b fix/nombre-bug
   ```

3. Haz tus cambios siguiendo las guías de estilo

4. Escribe tests si aplica

5. Commit con mensajes descriptivos:
   ```
   feat: añadir búsqueda por voz
   fix: corregir clasificación de categorías
   docs: actualizar guía de instalación
   ```

6. Push y abre un Pull Request

## 🏗️ Estructura del Código

### Backend (Python)

```
backend/
├── app/
│   ├── api/           # Endpoints
│   ├── core/          # Config y DB
│   ├── models/        # Modelos de datos
│   ├── services/      # Lógica de negocio
│   └── main.py        # App principal
└── tests/             # Tests
```

### Frontend (React/TypeScript)

```
frontend/
└── src/
    ├── components/    # Componentes React
    ├── services/      # API calls
    ├── store/         # Estado global
    ├── types/         # TypeScript types
    └── App.tsx        # App principal
```

## 🎨 Guías de Estilo

### Python

- Seguir PEP 8
- Usar type hints
- Docstrings en funciones públicas
- Máximo 100 caracteres por línea

```python
def process_message(
    message: str,
    context: Optional[str] = None
) -> MessageResponse:
    """
    Procesa un mensaje del usuario.
    
    Args:
        message: Mensaje del usuario
        context: Contexto opcional
        
    Returns:
        Respuesta procesada
    """
    ...
```

### TypeScript/React

- Usar TypeScript estricto
- Componentes funcionales con hooks
- Props tipadas
- Nombres en camelCase

```typescript
interface MessageBubbleProps {
  message: Message;
  onDelete?: () => void;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onDelete }) => {
  ...
};
```

### CSS/Tailwind

- Usar Tailwind classes
- Mantener consistencia de colores
- Responsive design first

## 🧪 Testing

### Backend

```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend

```bash
cd frontend
npm test
npm run test:coverage
```

## 📦 Commits Semánticos

Usamos conventional commits:

- `feat:` Nueva característica
- `fix:` Bug fix
- `docs:` Documentación
- `style:` Formato de código
- `refactor:` Refactorización
- `test:` Tests
- `chore:` Tareas de mantenimiento

## 🔍 Review Process

1. Al menos 1 aprobación requerida
2. Tests deben pasar
3. No conflictos con main
4. Código debe seguir guías de estilo

## 🎯 Prioridades

Áreas donde más necesitamos ayuda:

1. **Integración LLM**: OpenAI, Claude, Ollama
2. **Tests**: Cobertura actual baja
3. **UI/UX**: Mejoras de interfaz
4. **Documentación**: Tutoriales y ejemplos
5. **Performance**: Optimizaciones

## 💬 Comunicación

- Issues para bugs y features
- Discussions para ideas generales
- Pull Requests para código

## 📄 Licencia

Al contribuir, aceptas que tu código se licencie bajo MIT License.

## 🙏 Reconocimientos

Todos los contribuidores serán añadidos al README.

¡Gracias por hacer Cerebro Digital mejor! 🧠✨
