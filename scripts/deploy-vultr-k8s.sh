#!/bin/bash

# Vultr Kubernetes Deployment Script
# This script deploys the Ticket Assistant to Vultr Kubernetes Engine (VKE)

set -e

echo "🚀 Starting Vultr Kubernetes Deployment for Ticket Assistant"

# Configuration
CLUSTER_NAME="ticket-assistant-cluster"
REGION="ewr"  # New York
NODE_POOL_SIZE="2"
NODE_PLAN="vc2-1c-2gb"
K8S_VERSION="1.28.3"

# Check prerequisites
if ! command -v vultr-cli &> /dev/null; then
    echo "❌ vultr-cli not found. Please install it first."
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install it first."
    exit 1
fi

if [ -z "$VULTR_API_KEY" ]; then
    echo "❌ VULTR_API_KEY environment variable not set"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create VKE cluster
echo "🏗️  Creating Vultr Kubernetes cluster..."
CLUSTER_ID=$(vultr-cli kubernetes create \
    --label $CLUSTER_NAME \
    --region $REGION \
    --version $K8S_VERSION \
    --node-pools="quantity:$NODE_POOL_SIZE,plan:$NODE_PLAN,label:worker-nodes" \
    --format json | jq -r '.id')

echo "✅ Cluster created with ID: $CLUSTER_ID"

# Wait for cluster to be ready
echo "⏳ Waiting for cluster to be ready..."
while true; do
    STATUS=$(vultr-cli kubernetes get $CLUSTER_ID --format json | jq -r '.status')
    if [ "$STATUS" = "active" ]; then
        break
    fi
    echo "Cluster status: $STATUS. Waiting..."
    sleep 30
done

# Get kubeconfig
echo "🔧 Downloading kubeconfig..."
vultr-cli kubernetes config $CLUSTER_ID > kubeconfig.yaml
export KUBECONFIG=kubeconfig.yaml

# Test kubectl connection
echo "🧪 Testing kubectl connection..."
kubectl get nodes

echo "✅ Kubernetes cluster ready!"
echo "📋 Cluster Info:"
echo "  ID: $CLUSTER_ID"
echo "  Name: $CLUSTER_NAME"
echo "  Region: $REGION"
echo "  Nodes: $(kubectl get nodes --no-headers | wc -l)"

# Deploy application
echo "🚀 Deploying Ticket Assistant to Kubernetes..."
kubectl apply -f k8s/

# Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/ticket-assistant-backend
kubectl rollout status deployment/ticket-assistant-frontend

# Get service URLs
echo "🌐 Getting service URLs..."
FRONTEND_URL=$(kubectl get service ticket-assistant-frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
BACKEND_URL=$(kubectl get service ticket-assistant-backend -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "✅ Deployment complete!"
echo ""
echo "🎉 Your Ticket Assistant is now deployed on Vultr Kubernetes!"
echo "🌐 Frontend: http://$FRONTEND_URL"
echo "📚 API Docs: http://$BACKEND_URL:8000/docs"
echo "🖥️  Cluster ID: $CLUSTER_ID"
echo ""
echo "To manage your deployment:"
echo "  View pods: kubectl get pods"
echo "  View services: kubectl get services"
echo "  View logs: kubectl logs -f deployment/ticket-assistant-backend"
echo "  Scale: kubectl scale deployment/ticket-assistant-backend --replicas=3"
