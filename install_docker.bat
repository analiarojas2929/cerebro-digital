@echo off
REM Script simple para instalar PostgreSQL v2.0 despues de instalar Docker

echo ================================================================
echo      INSTALACION FINAL - Cerebro Digital v2.0
echo ================================================================
echo.

echo [1/3] Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado
    echo.
    echo Instala Docker Desktop primero y vuelve a ejecutar este script
    pause
    exit /b 1
)
echo [OK] Docker instalado

echo.
echo [2/3] Iniciando PostgreSQL + pgvector...
docker run -d --name cerebro-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=cerebro_digital -p 5432:5432 pgvector/pgvector:pg16
timeout /t 8 /nobreak >nul
echo [OK] PostgreSQL corriendo en puerto 5432

echo.
echo [3/3] Inicializando base de datos...
cd backend
c:\Users\anali\Desktop\cerebro-digital\.venv\Scripts\python.exe app\core\db_manager.py
echo [OK] Base de datos lista

echo.
echo ================================================================
echo              INSTALACION COMPLETA
echo ================================================================
echo.
echo Iniciar servidor v2.0:
echo    cd backend
echo    python server_v2.py
echo.
pause
