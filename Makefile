.PHONY: help install install-dev run stop test test-unit test-integration clean lint format check docs

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	uv venv
	uv pip install -r requirements.txt

install-dev: ## Install development dependencies
	uv venv
	uv pip install -r requirements.txt -r dev-requirements.txt

run: ## Run the application
	@chmod +x scripts/run.sh
	@./scripts/run.sh

stop: ## Stop the application
	@chmod +x scripts/stop.sh
	@./scripts/stop.sh

test: ## Run all tests
	@chmod +x scripts/test.sh
	@./scripts/test.sh

test-unit: ## Run unit tests only
	source .venv/bin/activate && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && pytest tests/unit/ -v

test-integration: ## Run integration tests only
	source .venv/bin/activate && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && pytest tests/integration/ -v

clean: ## Clean up generated files
	rm -rf .venv/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint: ## Run linting
	source .venv/bin/activate && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && python -m flake8 src/ tests/

format: ## Format code
	source .venv/bin/activate && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && python -m black src/ tests/

check: ## Run type checking
	source .venv/bin/activate && export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && python -m mypy src/

docs: ## Generate documentation
	@echo "📖 API Documentation available at: http://localhost:8000/docs"
	@echo "📝 ReDoc available at: http://localhost:8000/redoc"

example: ## Run usage example
	source .venv/bin/activate && python examples/example_usage.py

setup: ## Initial project setup
	@echo "🚀 Setting up Ticket Assistant project..."
	make install-dev
	@if [ ! -f ".env" ]; then cp config/.env.example .env; echo "📝 Created .env file - please edit with your API keys"; fi
	@echo "✅ Setup complete! Run 'make run' to start the server"

dev: ## Start development server with auto-reload
	source .venv/bin/activate && uvicorn ticket_assistant.api.main:app --reload --host 0.0.0.0 --port 8000

# Project structure
tree: ## Show project structure
	@echo "📁 Project Structure:"
	@tree -I '.venv|__pycache__|*.pyc|.pytest_cache|htmlcov' .
