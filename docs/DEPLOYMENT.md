# 🚀 Vultr Deployment Guide

## Vultr Cloud Deployment

This guide covers deploying the Ticket Assistant application on Vultr's high-performance cloud infrastructure, optimized for the full-stack React + FastAPI architecture.

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Vultr Load     │    │  Frontend       │    │  Backend        │
│  Balancer       │───▶│  (React + Vite) │───▶│  (FastAPI)      │
│  (HAProxy)      │    │  Vultr Instance │    │  Vultr Instance │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Vultr DNS      │    │  Vultr Block    │    │  Vultr Private  │
│  Management     │    │  Storage        │    │  Network        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Prerequisites

- Vultr account with API access
- Docker installed locally
- Domain name (optional, for custom DNS)

## Docker Deployment

### 1. Backend Dockerfile

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

### 2. Frontend Dockerfile

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY frontend/package*.json ./frontend/

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ ./frontend/
COPY shared/ ./shared/

# Build application
WORKDIR /app/frontend
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - API_HOST=0.0.0.0
      - API_PORT=8000
    networks:
      - app-network
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://backend:8000
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
```

## Cloud Deployment

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

## Vultr Deployment Options

### Option 1: Vultr Compute Instances

#### 1. Create Vultr Instance

```bash
# Create a high-performance compute instance
vultr instance create \
  --region "ewr" \
  --plan "vc2-2c-4gb" \
  --os "ubuntu-20.04" \
  --label "ticket-assistant-app"
```

#### 2. Setup Script

```bash
#!/bin/bash
# setup-vultr.sh

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/your-username/ticket-assistant.git
cd ticket-assistant

# Set environment variables
echo "GROQ_API_KEY=your_api_key_here" > .env

# Start services
docker-compose up -d

# Setup SSL (optional)
# certbot --nginx -d yourdomain.com
```

### Option 2: Vultr Kubernetes Engine (VKE)

#### 1. Create Kubernetes Cluster

```bash
# Create VKE cluster
vultr kubernetes create \
  --cluster-name "ticket-assistant-cluster" \
  --region "ewr" \
  --version "v1.27.0" \
  --node-pools='[{"node_quantity":2,"plan":"vc2-2c-4gb","label":"worker-nodes"}]'
```

#### 2. Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ticket-assistant

---
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: ticket-assistant
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/ticket-assistant-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: groq-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

---
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: ticket-assistant
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/ticket-assistant-frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Option 3: Vultr Load Balancer with Multiple Instances

#### 1. Create Multiple Instances

```bash
# Create backend instances
for i in {1..2}; do
  vultr instance create \
    --region "ewr" \
    --plan "vc2-2c-4gb" \
    --os "ubuntu-20.04" \
    --label "ticket-assistant-backend-$i"
done

# Create frontend instances
for i in {1..2}; do
  vultr instance create \
    --region "ewr" \
    --plan "vc2-1c-2gb" \
    --os "ubuntu-20.04" \
    --label "ticket-assistant-frontend-$i"
done
```

#### 2. Setup Load Balancer

```bash
# Create load balancer
vultr load-balancer create \
  --region "ewr" \
  --label "ticket-assistant-lb" \
  --forwarding-rules '[
    {
      "frontend_protocol": "HTTP",
      "frontend_port": 80,
      "backend_protocol": "HTTP",
      "backend_port": 80
    },
    {
      "frontend_protocol": "HTTP",
      "frontend_port": 8000,
      "backend_protocol": "HTTP",
      "backend_port": 8000
    }
  ]'
```

## Performance Optimization for Vultr

### 1. Instance Selection

```bash
# High-performance instances for production
# Backend: vc2-4c-8gb or vc2-8c-16gb
# Frontend: vc2-2c-4gb
# Database: vc2-4c-8gb with SSD storage

# Development/testing
# Backend: vc2-2c-4gb
# Frontend: vc2-1c-2gb
```

### 2. Network Optimization

```bash
# Create private network
vultr network create \
  --region "ewr" \
  --description "ticket-assistant-network" \
  --v4_subnet "10.0.0.0/24"

# Attach instances to private network
vultr instance attach-private-network \
  --instance-id "your-instance-id" \
  --network-id "your-network-id"
```

### 3. Storage Optimization

```bash
# Create block storage for persistent data
vultr block-storage create \
  --region "ewr" \
  --size 100 \
  --label "ticket-assistant-storage"

# Attach to instance
vultr instance attach-block-storage \
  --instance-id "your-instance-id" \
  --block-storage-id "your-storage-id"
```

### 4. Monitoring and Logging

```bash
# Install monitoring agent
curl -s https://repo.vultr.com/setup.sh | bash
apt install vultr-agent

# Configure logging
cat > /etc/rsyslog.d/50-vultr.conf << EOF
*.*  @@logs.vultr.com:514
EOF

systemctl restart rsyslog
```
