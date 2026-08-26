@echo off
REM Script de instalación para Windows

echo 🧠 Instalando Cerebro Digital...

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado. Por favor instala Python 3.10 o superior.
    exit /b 1
)
echo [OK] Python encontrado

REM Verificar Node.js
echo Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no está instalado. Por favor instala Node.js 18 o superior.
    exit /b 1
)
echo [OK] Node.js encontrado

REM Instalar backend
echo Instalando dependencias del backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo [OK] Backend instalado
cd ..

REM Instalar frontend
echo Instalando dependencias del frontend...
cd frontend
call npm install
echo [OK] Frontend instalado
cd ..

echo.
echo 🎉 Instalación completada!
echo.
echo Para iniciar el proyecto:
echo   1. Backend:  cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload
echo   2. Frontend: cd frontend && npm run dev
echo.
echo O usa Docker: docker-compose up
pause
