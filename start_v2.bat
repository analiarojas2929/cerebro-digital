@echo off
REM Script para iniciar servidor v2.0 correctamente

echo ============================================
echo    Iniciando Cerebro Digital v2.0
echo ============================================
echo.

REM Cambiar al directorio backend
cd /d "%~dp0backend"

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar si PostgreSQL esta disponible
echo [CHECK] Verificando PostgreSQL...
python -c "import psycopg2" 2>nul
if errorlevel 1 (
    echo [ERROR] Falta psycopg2-binary
    echo [FIX] Instalando ahora...
    pip install psycopg2-binary python-dotenv sentence-transformers openai pgvector --quiet
)

echo [OK] Dependencias listas
echo.

REM Verificar si existe .env
if not exist .env (
    echo [CREATE] Creando archivo .env...
    echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cerebro_digital > .env
    echo OPENAI_API_KEY= >> .env
    echo HOST=0.0.0.0 >> .env
    echo PORT=8000 >> .env
    echo [OK] .env creado
    echo.
)

echo [START] Iniciando servidor v2.0...
echo.
echo Servidor corriendo en: http://localhost:8000
echo Documentacion API: http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener
echo.

python server_v2.py
