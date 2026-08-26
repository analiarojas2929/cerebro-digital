# ⚡ INSTALACIÓN FINAL - 2 Pasos

## Estado Actual ✅

✅ Todas las dependencias Python instaladas
✅ Código v2.0 completo
✅ Sistema v1.0 funcionando

## Falta Docker ⏳

### Paso 1: Instalar Docker Desktop (10-15 min)

**La página ya se abrió en tu navegador**

1. Descarga Docker Desktop para Windows
2. Instala (puede pedir reiniciar Windows)
3. Abre Docker Desktop y espera a que inicie
4. Verifica: `docker --version` en PowerShell

### Paso 2: Ejecutar Script (30 segundos)

Una vez Docker instalado:

```cmd
.\install_docker.bat
```

**Este script hace TODO automáticamente:**
- Descarga imagen PostgreSQL + pgvector
- Crea contenedor `cerebro-postgres`
- Inicializa base de datos
- ¡Listo!

## Iniciar Servidor v2.0

```powershell
cd backend
python server_v2.py
```

Abre: http://localhost:8000/docs

## Mientras Tanto...

Tu sistema actual sigue funcionando:
- Backend: http://localhost:8000 ✅
- Frontend: http://localhost:5175 ✅

## Comparación

| | v1 (Actual) | v2 (Después Docker) |
|---|---|---|
| **Funciona** | ✅ Ahora | ✅ Después |
| **Persistencia** | ❌ In-memory | ✅ PostgreSQL |
| **Búsqueda** | Regex | 🧠 Semántica |
| **Chat** | Básico | 🤖 OpenAI GPT |

---

**Próximo paso:** Instalar Docker Desktop y ejecutar `.\install_docker.bat`
