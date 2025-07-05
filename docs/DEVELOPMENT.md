# 🛠️ Development Setup

## Prerequisites

- Python 3.9+
- Git
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### 1. Install uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd ticket-assistant

# Install dependencies
uv sync --dev

# Copy environment file
cp .env.example .env
```

### 3. Configure Environment

Edit `.env` file with your configuration:

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# External Ticket API Configuration
TICKET_API_ENDPOINT=https://api.example.com/tickets

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Logging Configuration
LOG_LEVEL=INFO
```

### 4. Run the Application

```bash
# Start the server
uv run python main.py

# Or with uvicorn directly
uv run uvicorn ticket_assistant.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Development Tools

### VS Code Setup

The project includes comprehensive VS Code configuration:

1. **Install recommended extensions** (auto-prompted)
2. **Python environment** is auto-detected
3. **Debugging** is pre-configured
4. **Tasks** are available via Ctrl+Shift+P

**Key VS Code Features:**
- **Linting**: Ruff integration
- **Formatting**: Auto-format on save
- **Testing**: Integrated pytest runner
- **Debugging**: FastAPI debugging support
- **Type checking**: Pylance strict mode

### Pre-commit Hooks

Set up pre-commit hooks for code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**Pre-commit includes:**
- **Ruff** - Linting and formatting
- **Bandit** - Security scanning
- **Safety** - Vulnerability checks
- **Detect-secrets** - Secret detection
- **Basic checks** - Trailing whitespace, file sizes, etc.

## Testing

### Run Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run specific test file
uv run pytest tests/unit/test_main.py -v

# Run integration tests only
uv run pytest tests/integration/ -v
```

### Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── test_main.py        # API endpoint tests
│   ├── test_groq_classifier.py # AI classification tests
│   └── test_report_service.py # Report service tests
├── integration/             # Integration tests
│   └── test_api_integration.py # Full API integration tests
└── conftest.py             # Test configuration and fixtures
```

### Writing Tests

Tests use pytest with fixtures:

```python
import pytest
from fastapi.testclient import TestClient
from ticket_assistant.api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
```

## Code Quality

### Linting and Formatting

```bash
# Check code with Ruff
uv run ruff check src/ tests/

# Fix issues automatically
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/
```

### Security Scanning

```bash
# Run security check
uv run bandit -r src/ -f json -o bandit-report.json

# Check for vulnerabilities
uv run safety check
```

### Type Checking

```bash
# Run mypy (if configured)
uv run mypy src/
```

## Project Tasks

Use the provided VS Code tasks or run commands directly:

### VS Code Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- **Install Dependencies**
- **Run Tests**
- **Run Tests with Coverage**
- **Lint with Ruff**
- **Format with Ruff**
- **Security Check**
- **Start API Server**

### Make Commands (if available)

```bash
make install    # Install dependencies
make test       # Run tests
make lint       # Run linting
make format     # Format code
make run        # Start server
make clean      # Clean build artifacts
```

## Debugging

### VS Code Debugging

1. Set breakpoints in your code
2. Press F5 or use "Run and Debug" panel
3. Select "Python: FastAPI" configuration

### Manual Debugging

```bash
# Run with debugger
uv run python -m pdb main.py

# Or with uvicorn
uv run uvicorn ticket_assistant.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Management

### Virtual Environment

```bash
# Create virtual environment
uv venv

# Activate (if not using uv run)
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Deactivate
deactivate
```

### Dependencies

```bash
# Add new dependency
uv add package_name

# Add development dependency
uv add --dev package_name

# Remove dependency
uv remove package_name

# Update dependencies
uv sync --upgrade
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure PYTHONPATH includes `src/`
2. **API key errors**: Check `.env` file configuration
3. **Port conflicts**: Change API_PORT in `.env`
4. **Test failures**: Ensure all dependencies are installed

### Logs

```bash
# Check application logs
tail -f logs/app.log

# Or run with verbose logging
LOG_LEVEL=DEBUG uv run python main.py
```

### Performance

```bash
# Profile the application
uv run python -m cProfile main.py

# Memory usage
uv run python -m memory_profiler main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Code Style

- Follow PEP 8 (enforced by Ruff)
- Use type hints
- Write docstrings for public functions
- Keep functions small and focused
- Write tests for new functionality
