# Script de Verificación Pre-Deploy
# Ejecutar antes de desplegar en la nube

Write-Host "`n🔍 Verificando Cerebro Digital para Deploy...`n" -ForegroundColor Cyan

$allGood = $true

# 1. Verificar estructura del proyecto
Write-Host "📁 Verificando estructura..." -ForegroundColor Yellow
$requiredFiles = @(
    "backend/server.py",
    "backend/requirements.txt",
    "frontend/package.json",
    "frontend/vite.config.ts",
    "render.yaml",
    ".gitignore"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file - NO ENCONTRADO" -ForegroundColor Red
        $allGood = $false
    }
}

# 2. Verificar .env
Write-Host "`n🔑 Verificando variables de entorno..." -ForegroundColor Yellow
if (Test-Path "backend/.env") {
    $envContent = Get-Content "backend/.env" -Raw
    if ($envContent -match "KOSTRA_KEY=sk-") {
        Write-Host "  ✅ KOSTRA_KEY configurada" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  KOSTRA_KEY podría no estar configurada correctamente" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ backend/.env no existe" -ForegroundColor Red
    $allGood = $false
}

# 3. Verificar dependencias Python
Write-Host "`n🐍 Verificando dependencias Python..." -ForegroundColor Yellow
if (Test-Path "backend/venv") {
    Write-Host "  ✅ Virtual environment existe" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Virtual environment no encontrado" -ForegroundColor Yellow
}

# 4. Verificar node_modules
Write-Host "`n📦 Verificando dependencias Node..." -ForegroundColor Yellow
if (Test-Path "frontend/node_modules") {
    Write-Host "  ✅ node_modules existe" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  node_modules no encontrado (ejecutar 'npm install')" -ForegroundColor Yellow
}

# 5. Verificar Git
Write-Host "`n📝 Verificando Git..." -ForegroundColor Yellow
$gitStatus = git status --porcelain 2>$null
if ($LASTEXITCODE -eq 0) {
    if ($gitStatus) {
        Write-Host "  ⚠️  Hay cambios sin commit:" -ForegroundColor Yellow
        git status --short
    } else {
        Write-Host "  ✅ Todo está commiteado" -ForegroundColor Green
    }
    
    # Verificar remote
    $remote = git remote get-url origin 2>$null
    if ($remote -match "github.com") {
        Write-Host "  ✅ Remote configurado: $remote" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Remote no apunta a GitHub" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "  ❌ No es un repositorio Git" -ForegroundColor Red
    $allGood = $false
}

# 6. Verificar archivos sensibles no commiteados
Write-Host "`n🔒 Verificando archivos sensibles..." -ForegroundColor Yellow
$sensitiveFiles = @(
    "backend/.env",
    "frontend/.env",
    "backend/venv",
    "frontend/node_modules"
)

$gitFiles = git ls-files 2>$null
foreach ($file in $sensitiveFiles) {
    if ($gitFiles -match [regex]::Escape($file)) {
        Write-Host "  ⚠️  $file está en Git (debería estar en .gitignore)" -ForegroundColor Red
        $allGood = $false
    } else {
        Write-Host "  ✅ $file NO está en Git" -ForegroundColor Green
    }
}

# 7. Resumen
Write-Host "`n" + "="*60 -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ TODO LISTO PARA DEPLOY!" -ForegroundColor Green
    Write-Host "`nPróximos pasos:" -ForegroundColor Cyan
    Write-Host "  1. git add ." -ForegroundColor White
    Write-Host "  2. git commit -m 'Preparar para deploy'" -ForegroundColor White
    Write-Host "  3. git push" -ForegroundColor White
    Write-Host "  4. Ir a render.com y seguir DEPLOY_QUICK_START.md`n" -ForegroundColor White
} else {
    Write-Host "❌ HAY PROBLEMAS QUE RESOLVER" -ForegroundColor Red
    Write-Host "`nRevisa los errores arriba y corrígelos antes de deployar`n" -ForegroundColor Yellow
}
Write-Host "="*60 -ForegroundColor Cyan

# Información adicional
Write-Host "`n📚 Documentación:" -ForegroundColor Cyan
Write-Host "  - Guía rápida: DEPLOY_QUICK_START.md" -ForegroundColor White
Write-Host "  - Guía completa: DEPLOYMENT_CLOUD.md" -ForegroundColor White
Write-Host "  - README: README.md`n" -ForegroundColor White
