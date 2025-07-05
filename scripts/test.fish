#!/usr/bin/env fish

# Fish Shell Test Runner Script for Ticket Assistant

echo "🧪 Running Ticket Assistant Tests..."

# Check if uv is installed
if not command -v uv &> /dev/null
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
end

# Change to backend directory
cd backend

# Check if we're in the backend directory
if not test -f "pyproject.toml"
    echo "❌ Not in the backend directory or pyproject.toml not found"
    cd ..
    exit 1
end

# Install test dependencies
echo "📦 Installing test dependencies..."
uv pip install -r requirements.txt -r dev-requirements.txt

# Activate virtual environment and set PYTHONPATH
echo "🔧 Setting up environment..."
source .venv/bin/activate.fish
set -x PYTHONPATH (pwd)/src

echo ""
echo "📊 Running all tests with coverage..."
pytest --cov=src --cov-report=term-missing --cov-report=html -v

echo ""
echo "📋 Test Summary:"
echo "=================="

# Show coverage report location
if test -f "htmlcov/index.html"
    echo "📈 Coverage report generated: htmlcov/index.html"
end

echo "✅ Tests completed!"

# Return to root directory
cd ..
