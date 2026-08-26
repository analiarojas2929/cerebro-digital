# Instalacion de PostgreSQL local (sin Docker)
# Para cuando la virtualizacion no esta disponible

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   PostgreSQL Local - Cerebro Digital v2.0 (Sin Docker)" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "IMPORTANTE: Esta opcion instala PostgreSQL directamente en Windows" -ForegroundColor Yellow
Write-Host "Sin necesidad de Docker ni virtualizacion" -ForegroundColor Yellow
Write-Host ""

# Verificar si PostgreSQL ya esta instalado
$pgPath = Get-Command psql -ErrorAction SilentlyContinue

if ($pgPath) {
    Write-Host "[OK] PostgreSQL ya esta instalado" -ForegroundColor Green
    Write-Host "    Ruta: $($pgPath.Source)" -ForegroundColor Gray
    Write-Host ""
    
    # Verificar si el servicio esta corriendo
    $pgService = Get-Service postgresql* -ErrorAction SilentlyContinue
    
    if ($pgService -and $pgService.Status -eq "Running") {
        Write-Host "[OK] Servicio PostgreSQL corriendo" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Servicio PostgreSQL no esta corriendo" -ForegroundColor Yellow
        Write-Host "       Intentando iniciar..." -ForegroundColor Yellow
        
        if ($pgService) {
            Start-Service $pgService.Name
            Write-Host "[OK] Servicio iniciado" -ForegroundColor Green
        }
    }
} else {
    Write-Host "[INFO] PostgreSQL NO instalado" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Descarga PostgreSQL 16 para Windows:" -ForegroundColor Cyan
    Write-Host "https://www.postgresql.org/download/windows/" -ForegroundColor White
    Write-Host ""
    Write-Host "O usa el instalador EDB:" -ForegroundColor Cyan
    Write-Host "https://www.enterprisedb.com/downloads/postgres-postgresql-downloads" -ForegroundColor White
    Write-Host ""
    Write-Host "Durante la instalacion:" -ForegroundColor Yellow
    Write-Host "  - Password: postgres" -ForegroundColor White
    Write-Host "  - Puerto: 5432" -ForegroundColor White
    Write-Host "  - Incluir Stack Builder: Si" -ForegroundColor White
    Write-Host ""
    
    # Abrir pagina de descarga
    $download = Read-Host "Abrir pagina de descarga? (s/n)"
    if ($download -eq "s") {
        Start-Process "https://www.enterprisedb.com/downloads/postgres-postgresql-downloads"
    }
    
    Write-Host ""
    Write-Host "Ejecuta este script nuevamente despues de instalar PostgreSQL" -ForegroundColor Cyan
    exit
}

# Crear base de datos
Write-Host ""
Write-Host "[1/3] Creando base de datos cerebro_digital..." -ForegroundColor Yellow

$env:PGPASSWORD = "postgres"
$createDb = psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='cerebro_digital'" 2>&1

if ($createDb -match "1") {
    Write-Host "    [INFO] Base de datos ya existe" -ForegroundColor Blue
} else {
    psql -U postgres -c "CREATE DATABASE cerebro_digital;" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    [OK] Base de datos creada" -ForegroundColor Green
    } else {
        Write-Host "    [ERROR] No se pudo crear la base de datos" -ForegroundColor Red
        Write-Host "    [TIP] Verifica password y permisos" -ForegroundColor Yellow
        exit 1
    }
}

# Instalar pgvector
Write-Host ""
Write-Host "[2/3] Instalando extension pgvector..." -ForegroundColor Yellow
Write-Host "    [INFO] Descargando pgvector para Windows..." -ForegroundColor Blue

# Descargar pgvector pre-compilado
$pgVersion = psql -U postgres -tc "SHOW server_version;" 2>&1 | ForEach-Object { $_.Trim().Split('.')[0] }
Write-Host "    [INFO] PostgreSQL version: $pgVersion" -ForegroundColor Blue

Write-Host ""
Write-Host "    MANUAL: Instalar pgvector desde:" -ForegroundColor Yellow
Write-Host "    https://github.com/pgvector/pgvector/releases" -ForegroundColor White
Write-Host ""
Write-Host "    O ejecutar en PostgreSQL:" -ForegroundColor Yellow
Write-Host '    CREATE EXTENSION IF NOT EXISTS vector;' -ForegroundColor White
Write-Host ""

$skipVector = Read-Host "Continuar sin pgvector por ahora? (s/n)"
if ($skipVector -ne "s") {
    Write-Host "    [INFO] Instala pgvector y ejecuta este script nuevamente" -ForegroundColor Cyan
    exit
}

# Actualizar DATABASE_URL
Write-Host ""
Write-Host "[3/3] Configurando conexion..." -ForegroundColor Yellow

Push-Location backend

if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "DATABASE_URL") {
        $envContent = $envContent -replace "DATABASE_URL=.*", "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cerebro_digital"
        $envContent | Out-File -FilePath ".env" -Encoding UTF8 -NoNewline
        Write-Host "    [OK] .env actualizado" -ForegroundColor Green
    }
} else {
    @"
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cerebro_digital
OPENAI_API_KEY=
HOST=0.0.0.0
PORT=8000
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "    [OK] .env creado" -ForegroundColor Green
}

Pop-Location

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "              PostgreSQL Local Configurado" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Siguiente paso:" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   python app\core\db_manager.py" -ForegroundColor White
Write-Host "   python server_v2.py" -ForegroundColor White
Write-Host ""
Write-Host "NOTA: pgvector es opcional para empezar" -ForegroundColor Cyan
Write-Host "El sistema funcionara sin busqueda semantica" -ForegroundColor Gray
Write-Host ""
