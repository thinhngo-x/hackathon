#!/bin/bash
# Quick start script for Ticket Assistant

echo "🎫 Starting Ticket Assistant..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js first."
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use. Please stop any processes using this port."
        return 1
    fi
    return 0
}

# Check if ports are available
if ! check_port 8000; then
    echo "Backend port 8000 is in use."
    exit 1
fi

if ! check_port 3000; then
    echo "Frontend port 3000 is in use."
    exit 1
fi

echo "✅ Ports 8000 and 3000 are available"
echo ""

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Install backend dependencies if needed
if [ ! -d "backend/.venv" ]; then
    echo "🐍 Installing backend dependencies..."
    cd backend && uv sync --dev && cd ..
fi

# Copy .env if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "⚙️  Creating .env file..."
    cp backend/.env.example backend/.env
    echo "📝 Please edit backend/.env and add your Groq API key if needed"
fi

echo "🚀 Starting servers..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start both servers in parallel
trap 'kill $(jobs -p)' EXIT
cd backend && uv run python src/ticket_assistant/api/main.py &
cd frontend && npm run dev &

# Wait for both background processes
wait
