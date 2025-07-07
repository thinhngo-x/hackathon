# 🎫 Ticket Assistant Backend

FastAPI-based backend for the AI-powered ticket reporting and classification system.

## Features

- **Report Submission**: Send structured reports with name, keywords, and descriptions
- **AI Classification**: Use Groq API to automatically classify errors and route them to relevant departments
- **Department Routing**: Automatic routing to backend, frontend, database, DevOps, security, API, integration, or general departments
- **Severity Assessment**: Automatic severity classification (low, medium, high, critical)
- **RESTful API**: Full FastAPI implementation with automatic documentation

## Quick Start

```bash
# Install dependencies
uv sync --dev

# Set up environment
cp .env.example .env
# Edit .env and add your Groq API key (optional - will use mock responses if not provided)

# Run the server
uv run python src/ticket_assistant/api/main.py

# Visit http://localhost:8000/docs for API documentation
```

## Development

```bash
# Run tests
uv run pytest tests/ -v

# Lint code
uv run ruff check --fix
uv run ruff format

# Run with auto-reload
uv run uvicorn src.ticket_assistant.api.main:app --reload

# Alternative: Run directly with Python
uv run python src/ticket_assistant/api/main.py
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/reports/submit` - Submit a ticket report
- `POST /api/classification/classify` - Classify an error
- `POST /api/combined/submit-and-classify` - Submit and classify in one request
- `GET /docs` - Interactive API documentation

## Environment Variables

- `GROQ_API_KEY` - Your Groq API key for AI classification
- `TICKET_API_ENDPOINT` - External ticket API endpoint
- `API_HOST` - Host to bind the server (default: 0.0.0.0)
- `API_PORT` - Port to run the server (default: 8000)
- `DEBUG` - Enable debug mode (default: True)
- `LOG_LEVEL` - Logging level (default: INFO)
