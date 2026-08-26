# Script para iniciar PostgreSQL + pgvector en Docker

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "      Iniciando PostgreSQL + pgvector en Docker" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Docker esta corriendo
Write-Host "[CHECK] Verificando Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "   [OK] $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "   [ERROR] Docker no esta instalado o no esta corriendo" -ForegroundColor Red
    Write-Host "   [INFO] Instala Docker Desktop y vuelve a ejecutar este script" -ForegroundColor Yellow
    exit 1
}

# Verificar si el contenedor ya existe
$existingContainer = docker ps -a --filter "name=cerebro-postgres" --format "{{.Names}}" 2>&1

if ($existingContainer -eq "cerebro-postgres") {
    Write-Host "[INFO] Contenedor cerebro-postgres ya existe" -ForegroundColor Blue
    
    # Verificar si esta corriendo
    $runningContainer = docker ps --filter "name=cerebro-postgres" --format "{{.Names}}" 2>&1
    
    if ($runningContainer -eq "cerebro-postgres") {
        Write-Host "   [OK] PostgreSQL ya esta corriendo en puerto 5432" -ForegroundColor Green
    } else {
        Write-Host "   [START] Iniciando contenedor existente..." -ForegroundColor Yellow
        docker start cerebro-postgres
        Start-Sleep -Seconds 3
        Write-Host "   [OK] PostgreSQL iniciado en puerto 5432" -ForegroundColor Green
    }
} else {
    Write-Host "[CREATE] Creando nuevo contenedor PostgreSQL + pgvector..." -ForegroundColor Yellow
    
    docker run -d `
        --name cerebro-postgres `
        -e POSTGRES_PASSWORD=postgres `
        -e POSTGRES_DB=cerebro_digital `
        -p 5432:5432 `
        pgvector/pgvector:pg16
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [WAIT] Esperando a que PostgreSQL este listo..." -ForegroundColor Yellow
        Start-Sleep -Seconds 8
        Write-Host "   [OK] PostgreSQL + pgvector corriendo en puerto 5432" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] No se pudo crear el contenedor" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "              PostgreSQL LISTO" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Informacion de conexion:" -ForegroundColor Cyan
Write-Host "   Host: localhost" -ForegroundColor White
Write-Host "   Puerto: 5432" -ForegroundColor White
Write-Host "   Base de datos: cerebro_digital" -ForegroundColor White
Write-Host "   Usuario: postgres" -ForegroundColor White
Write-Host "   Password: postgres" -ForegroundColor White
Write-Host ""
Write-Host "Siguiente paso:" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   python app\core\db_manager.py" -ForegroundColor White
Write-Host ""
