#!/bin/bash

# Script de instalación para Cerebro Digital

echo "🧠 Instalando Cerebro Digital..."

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${BLUE}Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 no está instalado. Por favor instala Python 3.10 o superior.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python encontrado${NC}"

# Verificar Node.js
echo -e "${BLUE}Verificando Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js no está instalado. Por favor instala Node.js 18 o superior.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js encontrado${NC}"

# Instalar backend
echo -e "${BLUE}Instalando dependencias del backend...${NC}"
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo -e "${GREEN}✓ Backend instalado${NC}"

# Copiar .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Archivo .env creado${NC}"
fi

cd ..

# Instalar frontend
echo -e "${BLUE}Instalando dependencias del frontend...${NC}"
cd frontend
npm install
echo -e "${GREEN}✓ Frontend instalado${NC}"

cd ..

echo -e "${GREEN}🎉 Instalación completada!${NC}"
echo ""
echo "Para iniciar el proyecto:"
echo "  1. Backend:  cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "  2. Frontend: cd frontend && npm run dev"
echo ""
echo "O usa Docker: docker-compose up"
