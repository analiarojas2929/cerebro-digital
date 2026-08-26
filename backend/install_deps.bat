@echo off
echo Instalando dependencias del Cerebro Digital Backend...
echo.

echo [1/5] Instalando framework web...
pip install fastapi uvicorn[standard] python-multipart

echo.
echo [2/5] Instalando bases de datos...
pip install sqlalchemy redis python-dotenv pydantic pydantic-settings

echo.
echo [3/5] Instalando dependencias de ML (esto puede tardar)...
pip install sentence-transformers chromadb numpy

echo.
echo [4/5] Instalando utilidades...
pip install loguru httpx

echo.
echo [5/5] Instalando dependencias opcionales...
pip install pytest pytest-asyncio black

echo.
echo ✓ Instalacion completada!
echo.
echo Para iniciar el servidor ejecuta:
echo   python -m uvicorn app.main:app --reload
pause
