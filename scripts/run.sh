#!/bin/bash

echo "🎫 Ticket Assistant API Runner Script"

echo "🎫 Starting Ticket Assistant API..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   or visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Change to backend directory
cd backend

# Check if we're in the backend directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Not in the backend directory or pyproject.toml not found"
    cd ..
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Install dependencies if not already done
echo "📚 Installing dependencies..."
uv pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp config/.env.example .env
    echo "📝 Please edit .env file and add your Groq API key"
    echo "🔑 You can get a Groq API key from: https://console.groq.com/"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default port if not specified
DEFAULT_PORT=${API_PORT:-8000}

# Check if port is in use and find alternative
check_port() {
    local port=$1
    if lsof -i :$port >/dev/null 2>&1; then
        return 1  # Port is in use
    else
        return 0  # Port is free
    fi
}

# Find available port starting from default
find_available_port() {
    local port=$DEFAULT_PORT
    while ! check_port $port; do
        echo "⚠️  Port $port is in use, trying port $((port + 1))..."
        port=$((port + 1))
        if [ $port -gt 8010 ]; then
            echo "❌ Could not find available port between 8000-8010"
            echo "💡 You can:"
            echo "   - Kill existing processes: lsof -ti :8000 | xargs kill -9"
            echo "   - Set custom port: export API_PORT=8001 && ./scripts/run.sh"
            exit 1
        fi
    done
    echo $port
}

AVAILABLE_PORT=$(find_available_port)
echo "🚀 Starting FastAPI server on port $AVAILABLE_PORT..."

# Run the application
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export API_PORT=$AVAILABLE_PORT
python -m ticket_assistant.api.main
