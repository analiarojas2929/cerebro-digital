# Script de instalacion rapida - Cerebro Digital v2.0
# Automatiza la configuracion completa

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "      CEREBRO DIGITAL v2.0 - INSTALACION AUTOMATICA" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Docker
Write-Host "[1] Verificando Docker..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "   [OK] Docker instalado" -ForegroundColor Green
    
    # Verificar si el contenedor ya existe
    $existingContainer = docker ps -a --filter "name=cerebro-postgres" --format "{{.Names}}"
    
    if ($existingContainer) {
        Write-Host "   [INFO] Contenedor PostgreSQL ya existe" -ForegroundColor Blue
        $response = Read-Host "   Detener y recrear? (s/n)"
        if ($response -eq "s") {
            docker stop cerebro-postgres
            docker rm cerebro-postgres
            Write-Host "   [DEL] Contenedor anterior eliminado" -ForegroundColor Gray
        }
    }
    
    if (-not $existingContainer -or $response -eq "s") {
        Write-Host "   [RUN] Iniciando PostgreSQL + pgvector en Docker..." -ForegroundColor Yellow
        docker run -d `
            --name cerebro-postgres `
            -e POSTGRES_PASSWORD=postgres `
            -e POSTGRES_DB=cerebro_digital `
            -p 5432:5432 `
            pgvector/pgvector:pg16
        
        Write-Host "   [WAIT] Esperando a que PostgreSQL este listo..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        Write-Host "   [OK] PostgreSQL corriendo en puerto 5432" -ForegroundColor Green
    }
} else {
    Write-Host "   [ERROR] Docker NO instalado" -ForegroundColor Red
    Write-Host "   [INFO] Descarga Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "   Continuar sin Docker? (necesitaras PostgreSQL instalado) (s/n)"
    if ($response -ne "s") {
        exit
    }
}

# 2. Instalar dependencias Python
Write-Host ""
Write-Host "[2] Instalando dependencias Python..." -ForegroundColor Yellow
Push-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "   [CREATE] Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "   [ACTIVATE] Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "   [INSTALL] Instalando paquetes (esto puede tardar varios minutos)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

Write-Host "   [OK] Dependencias instaladas" -ForegroundColor Green

# 3. Configurar .env
Write-Host ""
Write-Host "[3] Configurando variables de entorno..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    Write-Host "   [CREATE] Creando archivo .env..." -ForegroundColor Yellow
    
    $envContent = @"
# Configuracion Cerebro Digital v2.0
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cerebro_digital
OPENAI_API_KEY=
HOST=0.0.0.0
PORT=8000
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    
    Write-Host "   [OK] Archivo .env creado" -ForegroundColor Green
    Write-Host ""
    Write-Host "   [TIP] OPCIONAL: Agrega tu OpenAI API key al archivo .env" -ForegroundColor Cyan
    Write-Host "         (Sin API key funcionara con respuestas basicas)" -ForegroundColor Gray
} else {
    Write-Host "   [INFO] .env ya existe" -ForegroundColor Blue
}

# 4. Inicial[4] Inicializando base de datos..." -ForegroundColor Yellow
python app\core\db_manager.py

# 5. Migrar datos (si existen)
Write-Host ""
Write-Host "[5] Tienes datos del sistema anterior para migrar?" -ForegroundColor Yellow
$migrate = Read-Host "   (s/n)"

if ($migrate -eq "s") {
    Write-Host "   [MIGRATE] Ejecutando migracion..." -ForegroundColor Yellow
    python migrate_to_postgres.py
}

# 6. Resumen
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "             INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Todo listo para usar Cerebro Digital v2.0" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servicios instalados:" -ForegroundColor Yellow
Write-Host "   [OK] PostgreSQL + pgvector (Docker)" -ForegroundColor Green
Write-Host "   [OK] Embeddings (sentence-transformers)" -ForegroundColor Green
Write-Host "   [OK] Busqueda semantica" -ForegroundColor Green
if ((Get-Content .env) -match "OPENAI_API_KEY=sk-") {
    Write-Host "   [OK] OpenAI LLM configurado" -ForegroundColor Green
} else {
    Write-Host "   [WARN] OpenAI no configurado (modo basico)" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Para iniciar el servidor:" -ForegroundColor Cyan
Write-Host "   python server_v2.py" -ForegroundColor White
Write-Host ""
Write-Host "Documentacion:" -ForegroundColor Cyan
Write-Host "   http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Probar busqueda:" -ForegroundColor Cyan
Write-Host "   http://localhost:8000/memory/search?query=tu-pregunta" -ForegroundColor White
Write-Host ""

$start = Read-Host "Iniciar servidor ahora? (s/n)"
if ($start -eq "s") {
    Write-Host ""
    Write-Host "[RUN] Iniciando servidor..." -ForegroundColor Green
    Write-Host ""
    python server_v2.py
}

Pop-Location
