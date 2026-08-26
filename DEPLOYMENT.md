# 🚀 Guía de Despliegue en Producción

Esta guía te ayudará a desplegar Cerebro Digital en producción.

## Opciones de Despliegue

### 1. VPS/Cloud (Recomendado)

**Proveedores sugeridos:**
- DigitalOcean (~$12/mes)
- AWS EC2 (Free tier disponible)
- Google Cloud Platform
- Azure
- Linode
- Vultr

#### Requisitos mínimos del servidor:
- 2 CPU cores
- 4GB RAM
- 20GB SSD
- Ubuntu 22.04 LTS

### 2. Docker en VPS

La forma más fácil de desplegar:

```bash
# 1. En tu servidor, instala Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. Instala Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Clona el repositorio
git clone https://github.com/tu-usuario/cerebro-digital.git
cd cerebro-digital

# 4. Configura variables de entorno
cp backend/.env.example backend/.env
nano backend/.env  # Edita con tus valores de producción

# 5. Inicia con Docker
docker-compose up -d
```

### 3. Kubernetes

Para alta escala y redundancia:

```yaml
# deployment.yaml (ejemplo básico)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cerebro-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cerebro-backend
  template:
    metadata:
      labels:
        app: cerebro-backend
    spec:
      containers:
      - name: backend
        image: cerebro-digital-backend:latest
        ports:
        - containerPort: 8000
```

## Configuración de Producción

### Backend (.env)

```env
# Cambia estos valores en producción
DATABASE_URL=postgresql://cerebro:TU_PASSWORD_SEGURA@postgres:5432/cerebro_digital
REDIS_URL=redis://:TU_REDIS_PASSWORD@redis:6379/0
SECRET_KEY=genera-una-key-segura-aqui-con-openssl
DEBUG=False

# Si usas LLM
OPENAI_API_KEY=tu-api-key-real

# CORS - añade tu dominio
ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### Nginx como Reverse Proxy

```nginx
# /etc/nginx/sites-available/cerebro-digital

server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    # SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Certificado SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Auto-renovación (ya configurado por Certbot)
sudo certbot renew --dry-run
```

## Base de Datos en Producción

### PostgreSQL Gestionado

Usar servicios gestionados para facilitar backups y escalabilidad:

- **AWS RDS PostgreSQL**
- **Google Cloud SQL**
- **DigitalOcean Managed Databases**
- **Supabase** (incluye vector support)

### Redis Gestionado

- **AWS ElastiCache**
- **Redis Cloud**
- **DigitalOcean Managed Redis**

## Backups

### Script de Backup Automático

```bash
#!/bin/bash
# backup.sh

# Variables
BACKUP_DIR="/backups/cerebro-digital"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec cerebro-postgres pg_dump -U cerebro cerebro_digital > $BACKUP_DIR/db_$DATE.sql

# Backup ChromaDB
tar -czf $BACKUP_DIR/chroma_$DATE.tar.gz ./chroma_data/

# Limpiar backups antiguos (más de 7 días)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completado: $DATE"
```

### Cron para backups automáticos

```bash
# Editar crontab
crontab -e

# Añadir backup diario a las 2 AM
0 2 * * * /path/to/backup.sh >> /var/log/cerebro-backup.log 2>&1
```

## Monitoreo

### Prometheus + Grafana

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Logs Centralizados

```bash
# Usar Docker logs
docker-compose logs -f backend

# O instalar Logstash/Elasticsearch/Kibana (ELK)
```

## Seguridad

### Checklist de Seguridad

- [ ] `DEBUG=False` en producción
- [ ] Passwords fuertes en bases de datos
- [ ] `SECRET_KEY` único y seguro
- [ ] HTTPS habilitado (certificado SSL)
- [ ] CORS configurado correctamente
- [ ] Firewall configurado (solo puertos necesarios)
- [ ] Backups automatizados
- [ ] Rate limiting en API
- [ ] Actualización regular de dependencias
- [ ] Logs de acceso monitoreados

### Firewall (UFW)

```bash
# Permitir solo puertos necesarios
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### Rate Limiting

```python
# En backend/app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat/message")
@limiter.limit("10/minute")  # 10 requests por minuto
async def send_message(...):
    ...
```

## Escalabilidad

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
services:
  backend:
    deploy:
      replicas: 3
      
  nginx-load-balancer:
    image: nginx
    ports:
      - "80:80"
    depends_on:
      - backend
```

### Caché de Embeddings

```python
# Cachear embeddings frecuentes en Redis
def get_cached_embedding(text: str):
    cache_key = f"emb:{hash(text)}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return pickle.loads(cached)
    
    embedding = embedding_service.encode(text)
    redis_client.setex(cache_key, 3600, pickle.dumps(embedding))
    
    return embedding
```

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /path/to/cerebro-digital
            git pull
            docker-compose down
            docker-compose up -d --build
```

## Costos Estimados

### Setup Básico (~$20-30/mes)

- VPS ($10-12/mes) - DigitalOcean Droplet
- Dominio ($10-15/año)
- SSL gratis (Let's Encrypt)

### Setup Medio (~$50-80/mes)

- VPS más potente ($20/mes)
- PostgreSQL gestionado ($15/mes)
- Redis gestionado ($10/mes)
- OpenAI API (pay-as-you-go)
- CDN ($5/mes)

### Setup Enterprise (~$200+/mes)

- Kubernetes cluster
- Bases de datos con alta disponibilidad
- CDN global
- Monitoreo avanzado
- Backups automatizados

## Checklist Pre-Deploy

- [ ] Tests pasando
- [ ] Variables de entorno configuradas
- [ ] SSL configurado
- [ ] Backups configurados
- [ ] Monitoreo activo
- [ ] CORS configurado
- [ ] Rate limiting activo
- [ ] Logs configurados
- [ ] Documentación actualizada
- [ ] Dominio configurado

## Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Ver uso de recursos
docker stats

# Acceder a shell del contenedor
docker exec -it cerebro-backend bash

# Ejecutar migraciones de DB
docker exec cerebro-backend alembic upgrade head

# Verificar health
curl https://tu-dominio.com/health
```

## Soporte

Si encuentras problemas en producción:
1. Revisa logs: `docker-compose logs`
2. Verifica conectividad de BD
3. Revisa configuración de CORS
4. Abre un issue en GitHub

¡Feliz deployment! 🚀
