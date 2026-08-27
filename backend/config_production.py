# Configuración de CORS para Producción
# Agregar estos dominios después del deployment

ALLOWED_ORIGINS = [
    "http://localhost:5175",
    "http://localhost:3000",
    "https://cerebro-digital-frontend.onrender.com",
    "https://cerebro-digital.vercel.app",
    # Agregar tu dominio personalizado aquí
]

# Para desarrollo, usar allow_origins=["*"]
# Para producción, usar allow_origins=ALLOWED_ORIGINS
