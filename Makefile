.PHONY: help install install-dev run stop test test-unit test-integration clean lint format check docs security pre-commit

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
	pre-commit install

setup: ## Full development setup
	@chmod +x scripts/setup.fish
	@./scripts/setup.fish

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

lint: ## Run linting and formatting
	@chmod +x scripts/lint.fish
	@./scripts/lint.fish

security: ## Run security checks
	@chmod +x scripts/security.fish
	@./scripts/security.fish

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks to latest versions
	pre-commit autoupdate

format: ## Format code with Ruff
	source .venv/bin/activate && ruff format src/ tests/

check: ## Run all quality checks
	source .venv/bin/activate && ruff check src/ tests/
	source .venv/bin/activate && mypy src/ --ignore-missing-imports
	source .venv/bin/activate && bandit -r src/
	source .venv/bin/activate && safety check -r requirements.txt

clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf bandit-report.json
	rm -rf safety-report.json
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

# Development workflow targets
dev-setup: install-dev ## Alias for install-dev
dev-test: test ## Alias for test
dev-lint: lint ## Alias for lint
dev-security: security ## Alias for security

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
