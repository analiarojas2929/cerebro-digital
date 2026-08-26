# Makefile para Cerebro Digital

.PHONY: help install dev clean test docker-up docker-down

help:
	@echo "Cerebro Digital - Comandos disponibles:"
	@echo ""
	@echo "  make install       - Instalar dependencias"
	@echo "  make dev           - Iniciar en modo desarrollo"
	@echo "  make test          - Ejecutar tests"
	@echo "  make docker-up     - Iniciar con Docker"
	@echo "  make docker-down   - Detener Docker"
	@echo "  make clean         - Limpiar archivos temporales"
	@echo ""

install:
	@echo "Instalando backend..."
	cd backend && python -m venv venv && \
		(. venv/bin/activate || venv\Scripts\activate) && \
		pip install -r requirements.txt
	@echo "Instalando frontend..."
	cd frontend && npm install
	@echo "¡Instalación completa!"

dev-backend:
	cd backend && \
		(. venv/bin/activate || venv\Scripts\activate) && \
		uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Iniciando backend y frontend..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@make -j2 dev-backend dev-frontend

test:
	@echo "Ejecutando tests del backend..."
	cd backend && \
		(. venv/bin/activate || venv\Scripts\activate) && \
		pytest
	@echo "Ejecutando tests del frontend..."
	cd frontend && npm test

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	rm -f backend/test.db
	@echo "¡Limpieza completa!"
