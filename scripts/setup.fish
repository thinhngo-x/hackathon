#!/usr/bin/env fish

# Fish Shell Setup Script for Ticket Assistant

echo "🚀 Setting up Ticket Assistant Development Environment..."

# Check if uv is installed
if not command -v uv &> /dev/null
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
end

# Change to backend directory
cd backend

# Create virtual environment if it doesn't exist
if not test -d ".venv"
    echo "🔧 Creating virtual environment..."
    uv venv
end

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -r requirements.txt -r dev-requirements.txt

# Set up environment
echo "🔧 Setting up environment..."
source .venv/bin/activate.fish
set -x PYTHONPATH (pwd)/src

# Install pre-commit hooks
echo "🔒 Installing pre-commit hooks..."
pre-commit install

# Run pre-commit on all files to ensure everything is set up correctly
echo "🧪 Running pre-commit checks on all files..."
pre-commit run --all-files

# Initialize secrets detection baseline
echo "🔍 Initializing secrets detection baseline..."
detect-secrets scan --baseline .secrets.baseline

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Available commands:"
echo "   ./scripts/test.fish          # Run tests"
echo "   ./scripts/lint.fish          # Run linting and formatting"
echo "   ./scripts/security.fish      # Run security checks"
echo ""
echo "🎯 To run the application:"
echo "   cd backend"
echo "   source .venv/bin/activate.fish"
echo "   set -x PYTHONPATH (pwd)/src"
echo "   python src/ticket_assistant/api/main.py"
echo ""
echo "🎯 Pre-commit hooks are now installed and will run on every commit!"
echo "   git add ."
echo "   git commit -m 'Your commit message'"
echo ""
echo "🎯 To run pre-commit manually:"
echo "   pre-commit run --all-files"
