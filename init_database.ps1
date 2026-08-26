# Script para inicializar base de datos y migrar datos

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "      Inicializacion de Base de Datos" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio backend
Push-Location backend

# 1. Inicializar schema
Write-Host "[1] Inicializando schema de PostgreSQL..." -ForegroundColor Yellow
c:\Users\anali\Desktop\cerebro-digital\.venv\Scripts\python.exe app\core\db_manager.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "   [OK] Base de datos inicializada" -ForegroundColor Green
} else {
    Write-Host "   [ERROR] Fallo la inicializacion" -ForegroundColor Red
    Write-Host "   [TIP] Verifica que PostgreSQL este corriendo: .\start_postgres.ps1" -ForegroundColor Yellow
    Pop-Location
    exit 1
}

# 2. Migrar datos (opcional)
Write-Host ""
Write-Host "[2] Migrar datos del sistema anterior?" -ForegroundColor Yellow
$migrate = Read-Host "   (s/n)"

if ($migrate -eq "s") {
    Write-Host "   [MIGRATE] Migrando datos..." -ForegroundColor Yellow
    c:\Users\anali\Desktop\cerebro-digital\.venv\Scripts\python.exe migrate_to_postgres.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] Migracion completada" -ForegroundColor Green
    } else {
        Write-Host "   [WARN] Fallo la migracion (puede ser normal si no hay datos)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "              BASE DE DATOS LISTA" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Siguiente paso - Iniciar servidor:" -ForegroundColor Yellow
Write-Host "   python server_v2.py" -ForegroundColor White
Write-Host ""
Write-Host "O usar el servidor actual mientras migras:" -ForegroundColor Yellow
Write-Host "   python server.py" -ForegroundColor White
Write-Host ""

Pop-Location
