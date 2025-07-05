#!/bin/bash

# Test Runner Script for Ticket Assistant

echo "🧪 Running Ticket Assistant Tests..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Change to backend directory
cd backend

# Install test dependencies
echo "📦 Installing test dependencies..."
uv pip install -r requirements.txt -r dev-requirements.txt

echo ""
echo "📊 Running all tests with coverage..."
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest --cov=src --cov-report=term-missing --cov-report=html -v

echo ""
echo "📋 Test Summary:"
echo "=================="

# Show coverage report location
if [ -f "htmlcov/index.html" ]; then
    echo "📈 Coverage report generated: htmlcov/index.html"
fi

echo "✅ Tests completed!"
