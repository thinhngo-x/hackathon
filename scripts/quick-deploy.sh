#!/bin/bash

# Quick Vultr Deployment Script
# This script provides a simple one-click deployment to Vultr

set -e

echo "🎫 Ticket Assistant - Quick Vultr Deployment"
echo "=============================================="

# Check if we have the required tools
check_requirements() {
    echo "🔍 Checking requirements..."

    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is required but not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is required but not installed. Please install Docker Compose first."
        exit 1
    fi

    echo "✅ Requirements check passed"
}

# Get Vultr API key
get_vultr_key() {
    if [ -z "$VULTR_API_KEY" ]; then
        echo "🔑 Vultr API Key required for deployment"
        echo "Please get your API key from: https://my.vultr.com/settings/#settingsapi"
        read -p "Enter your Vultr API Key: " VULTR_API_KEY
        export VULTR_API_KEY
    fi
}

# Get Groq API key (optional)
get_groq_key() {
    if [ -z "$GROQ_API_KEY" ]; then
        echo "🤖 Groq API Key (optional - for AI features)"
        echo "Get your API key from: https://console.groq.com/keys"
        read -p "Enter your Groq API Key (or press Enter to skip): " GROQ_API_KEY
        export GROQ_API_KEY
    fi
}

# Choose deployment method
choose_deployment() {
    echo ""
    echo "🚀 Choose deployment method:"
    echo "1. Single Instance (Simple, cost-effective)"
    echo "2. Kubernetes Cluster (Scalable, production-ready)"
    echo "3. Local Docker (Test locally first)"
    echo ""
    read -p "Enter your choice (1-3): " DEPLOYMENT_CHOICE
}

# Deploy locally for testing
deploy_local() {
    echo "🏠 Deploying locally with Docker..."

    # Create .env file
    cat > .env << EOF
GROQ_API_KEY=$GROQ_API_KEY
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
EOF

    # Build and run
    docker-compose up -d --build

    echo "✅ Local deployment complete!"
    echo "🌐 Frontend: http://localhost:3000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "To stop: docker-compose down"
}

# Deploy to single Vultr instance
deploy_single_instance() {
    echo "☁️  Deploying to Vultr single instance..."

    # Install vultr-cli if not available
    if ! command -v vultr-cli &> /dev/null; then
        echo "📦 Installing vultr-cli..."
        if command -v go &> /dev/null; then
            go install github.com/vultr/vultr-cli@latest
        else
            echo "❌ Please install vultr-cli manually from: https://github.com/vultr/vultr-cli"
            exit 1
        fi
    fi

    # Run deployment script
    chmod +x scripts/deploy-vultr.sh
    ./scripts/deploy-vultr.sh
}

# Deploy to Vultr Kubernetes
deploy_kubernetes() {
    echo "🎛️  Deploying to Vultr Kubernetes..."

    # Install kubectl if not available
    if ! command -v kubectl &> /dev/null; then
        echo "📦 Installing kubectl..."
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/$(uname | tr '[:upper:]' '[:lower:]')/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
    fi

    # Run K8s deployment script
    chmod +x scripts/deploy-vultr-k8s.sh
    ./scripts/deploy-vultr-k8s.sh
}

# Main execution
main() {
    check_requirements
    get_vultr_key
    get_groq_key
    choose_deployment

    case $DEPLOYMENT_CHOICE in
        1)
            deploy_single_instance
            ;;
        2)
            deploy_kubernetes
            ;;
        3)
            deploy_local
            ;;
        *)
            echo "❌ Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
}

# Run main function
main
