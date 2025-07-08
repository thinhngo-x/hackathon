#!/bin/bash

# Vultr Deployment Script for Ticket Assistant
# This script automates deployment to Vultr Cloud Compute

set -e

echo "🚀 Starting Vultr Deployment for Ticket Assistant"

# Configuration
REGION="ewr"  # New York - change as needed
PLAN="vc2-1c-2gb"  # 1 CPU, 2GB RAM - adjust as needed
OS="ubuntu-20.04"
HOSTNAME="ticket-assistant"
LABEL="ticket-assistant-app"

# Check if vultr-cli is installed
if ! command -v vultr-cli &> /dev/null; then
    echo "❌ vultr-cli not found. Installing..."
    echo "Please install vultr-cli from https://github.com/vultr/vultr-cli"
    echo "Or run: go install github.com/vultr/vultr-cli@latest"
    exit 1
fi

# Check if VULTR_API_KEY is set
if [ -z "$VULTR_API_KEY" ]; then
    echo "❌ VULTR_API_KEY environment variable not set"
    echo "Please set your Vultr API key: export VULTR_API_KEY=your_api_key"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Build Docker images locally first
echo "🔨 Building Docker images..."
docker-compose build

# Create Vultr instance
echo "🏗️  Creating Vultr instance..."
INSTANCE_ID=$(vultr-cli instance create \
    --region $REGION \
    --plan $PLAN \
    --os $OS \
    --hostname $HOSTNAME \
    --label $LABEL \
    --enable-ipv6 \
    --tag "hackathon,ticket-assistant" \
    --format json | jq -r '.id')

echo "✅ Instance created with ID: $INSTANCE_ID"

# Wait for instance to be ready
echo "⏳ Waiting for instance to be ready..."
while true; do
    STATUS=$(vultr-cli instance get $INSTANCE_ID --format json | jq -r '.status')
    if [ "$STATUS" = "active" ]; then
        break
    fi
    echo "Instance status: $STATUS. Waiting..."
    sleep 10
done

# Get instance IP
INSTANCE_IP=$(vultr-cli instance get $INSTANCE_ID --format json | jq -r '.main_ip')
echo "✅ Instance ready at IP: $INSTANCE_IP"

# Create deployment script to run on the server
cat > deploy-server.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Setting up Ticket Assistant on Vultr instance..."

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install nginx for reverse proxy
sudo apt-get install -y nginx

# Create app directory
sudo mkdir -p /opt/ticket-assistant
sudo chown $USER:$USER /opt/ticket-assistant

echo "✅ Server setup complete"
EOF

# Copy deployment script to server
echo "📤 Copying deployment script to server..."
scp -o StrictHostKeyChecking=no deploy-server.sh root@$INSTANCE_IP:/tmp/
ssh -o StrictHostKeyChecking=no root@$INSTANCE_IP "chmod +x /tmp/deploy-server.sh && /tmp/deploy-server.sh"

# Copy application files
echo "📤 Copying application files..."
scp -o StrictHostKeyChecking=no -r . root@$INSTANCE_IP:/opt/ticket-assistant/

# Create environment file
echo "📝 Creating environment file..."
ssh -o StrictHostKeyChecking=no root@$INSTANCE_IP "cat > /opt/ticket-assistant/.env << 'EOF'
GROQ_API_KEY=${GROQ_API_KEY:-}
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
EOF"

# Deploy application
echo "🚀 Deploying application..."
ssh -o StrictHostKeyChecking=no root@$INSTANCE_IP "cd /opt/ticket-assistant && docker-compose up -d"

# Configure nginx reverse proxy
echo "🔧 Configuring nginx reverse proxy..."
ssh -o StrictHostKeyChecking=no root@$INSTANCE_IP "cat > /etc/nginx/sites-available/ticket-assistant << 'EOF'
server {
    listen 80;
    server_name $INSTANCE_IP;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"

# Enable nginx site
ssh -o StrictHostKeyChecking=no root@$INSTANCE_IP "ln -sf /etc/nginx/sites-available/ticket-assistant /etc/nginx/sites-enabled/ && systemctl restart nginx"

# Configure firewall
echo "🔒 Configuring firewall..."
ssh -o StrictHostKeyChecking=no root@$INSTANCE_IP "ufw allow 22/tcp && ufw allow 80/tcp && ufw allow 443/tcp && ufw --force enable"

echo "✅ Deployment complete!"
echo ""
echo "🎉 Your Ticket Assistant is now deployed on Vultr!"
echo "🌐 Frontend: http://$INSTANCE_IP"
echo "📚 API Docs: http://$INSTANCE_IP/docs"
echo "🖥️  Instance ID: $INSTANCE_ID"
echo ""
echo "To manage your instance:"
echo "  View: vultr-cli instance get $INSTANCE_ID"
echo "  SSH: ssh root@$INSTANCE_IP"
echo "  Logs: ssh root@$INSTANCE_IP 'cd /opt/ticket-assistant && docker-compose logs'"
echo ""
echo "To scale or update:"
echo "  1. Make changes to your code"
echo "  2. Run: scp -r . root@$INSTANCE_IP:/opt/ticket-assistant/"
echo "  3. SSH and run: cd /opt/ticket-assistant && docker-compose up -d --build"
