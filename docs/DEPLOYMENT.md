# 🚀 Deployment Guide

## Production Deployment

### Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ ./src/
COPY main.py ./

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uv", "run", "uvicorn", "ticket_assistant.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Build and Run

```bash
# Build image
docker build -t ticket-assistant .

# Run container
docker run -p 8000:8000 --env-file .env ticket-assistant
```

#### 3. Docker Compose

```yaml
version: '3.8'

services:
  ticket-assistant:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - TICKET_API_ENDPOINT=${TICKET_API_ENDPOINT}
      - API_HOST=0.0.0.0
      - API_PORT=8000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    restart: unless-stopped
```

### Cloud Deployment

#### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

docker build -t ticket-assistant .
docker tag ticket-assistant:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/ticket-assistant:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/ticket-assistant:latest

# Deploy to ECS (using task definition)
aws ecs update-service --cluster my-cluster --service ticket-assistant-service --force-new-deployment
```

#### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/ticket-assistant
gcloud run deploy ticket-assistant --image gcr.io/PROJECT_ID/ticket-assistant --platform managed --region us-central1 --allow-unauthenticated
```

#### Heroku

```bash
# Create Procfile
echo "web: uv run uvicorn ticket_assistant.api.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git add .
git commit -m "Add Procfile for Heroku"
git push heroku main
```

### Traditional Server Deployment

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create application user
sudo useradd -m -s /bin/bash ticket-assistant
sudo su - ticket-assistant
```

#### 2. Application Setup

```bash
# Clone repository
git clone <repository-url> /home/ticket-assistant/app
cd /home/ticket-assistant/app

# Install dependencies
uv sync --frozen

# Configure environment
cp .env.example .env
# Edit .env with production values
```

#### 3. Process Management with Systemd

Create `/etc/systemd/system/ticket-assistant.service`:

```ini
[Unit]
Description=Ticket Assistant API
After=network.target

[Service]
Type=simple
User=ticket-assistant
Group=ticket-assistant
WorkingDirectory=/home/ticket-assistant/app
Environment=PATH=/home/ticket-assistant/app/.venv/bin
ExecStart=/home/ticket-assistant/app/.venv/bin/uvicorn ticket_assistant.api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ticket-assistant
sudo systemctl start ticket-assistant
sudo systemctl status ticket-assistant
```

#### 4. Reverse Proxy with Nginx

Create `/etc/nginx/sites-available/ticket-assistant`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/ticket-assistant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Environment Configuration

### Production Environment Variables

```bash
# Application
GROQ_API_KEY=your_production_groq_api_key
TICKET_API_ENDPOINT=https://api.production.com/tickets

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Logging
LOG_LEVEL=INFO

# Security (if implementing)
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=["your-domain.com", "www.your-domain.com"]

# Database (if adding)
DATABASE_URL=postgresql://user:password@localhost/ticket_assistant  # pragma: allowlist secret
```

### Security Considerations

1. **Environment Variables**: Use secure secret management
2. **HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: Ensure all inputs are validated
5. **CORS**: Configure CORS properly for your domain
6. **Authentication**: Add authentication if needed

## Monitoring and Logging

### Health Checks

The application provides health check endpoints:
- `/health` - Basic health check
- `/health/live` - Liveness probe
- `/health/ready` - Readiness probe

### Logging

Configure structured logging:

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### Metrics

Consider adding metrics collection:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Example metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_duration_seconds', 'Request latency')
```

## Backup and Recovery

### Database Backup (if applicable)

```bash
# PostgreSQL backup
pg_dump -h localhost -U user -d ticket_assistant > backup.sql

# Restore
psql -h localhost -U user -d ticket_assistant < backup.sql
```

### Application Backup

```bash
# Backup application files
tar -czf ticket-assistant-backup-$(date +%Y%m%d).tar.gz /home/ticket-assistant/app

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz /var/log/ticket-assistant/
```

## Scaling

### Horizontal Scaling

```bash
# Run multiple instances
uvicorn ticket_assistant.api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or use gunicorn
gunicorn ticket_assistant.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Load Balancing

Configure load balancer (nginx/HAProxy) to distribute traffic across multiple instances.

## Maintenance

### Updates

```bash
# Update dependencies
uv sync --upgrade

# Restart service
sudo systemctl restart ticket-assistant

# Check logs
journalctl -u ticket-assistant -f
```

### Performance Tuning

1. **Database indexing** (if applicable)
2. **Caching** (Redis/Memcached)
3. **Connection pooling**
4. **Rate limiting**
5. **CDN for static assets**

## Troubleshooting

### Common Issues

1. **Port conflicts**: Check if port 8000 is available
2. **Environment variables**: Verify all required variables are set
3. **API key issues**: Check Groq API key validity
4. **Memory issues**: Monitor memory usage and adjust worker count
5. **Network issues**: Check firewall and security group settings

### Debug Mode

```bash
# Enable debug mode
export DEBUG=True
uv run python main.py

# Check logs
tail -f logs/app.log
```

### Performance Monitoring

```bash
# Monitor CPU/Memory
top -p $(pgrep -f "uvicorn")

# Network connections
ss -tulpn | grep :8000

# Application metrics
curl http://localhost:8000/metrics
```
