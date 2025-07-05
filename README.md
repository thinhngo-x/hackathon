# 🎫 Ticket Assistant API

A professionally organized, AI-powered ticket reporting and classification system built with FastAPI and modern Python best practices.

## 🚀 Quick Start

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync --dev

# 3. Set up environment
cp .env.example .env
# Edit .env and add your Groq API key

# 4. Run the server
uv run python main.py

# 5. Visit http://localhost:8000/docs for API documentation
```

## ✨ Features

- **Report Submission**: Send structured reports with name, keywords, and descriptions to a ticket API endpoint
- **AI Classification**: Use Groq API to automatically classify errors and route them to relevant departments
- **Department Routing**: Automatic routing to backend, frontend, database, DevOps, security, API, integration, or general departments
- **Severity Assessment**: Automatic severity classification (low, medium, high, critical)
- **RESTful API**: Full FastAPI implementation with automatic documentation
- **Comprehensive Testing**: Unit and integration tests with pytest (38 tests, 100% pass rate)
- **Fast Package Management**: Uses `uv` for lightning-fast dependency management
- **Modern Python Structure**: Follows src/ layout best practices

## 📁 Project Structure

```
ticket-assistant/
├── src/                          # Source code
│   └── ticket_assistant/
│       ├── api/                  # API layer
│       │   ├── main.py          # Main FastAPI app
│       │   ├── health.py        # Health check endpoints
│       │   ├── reports.py       # Report endpoints
│       │   ├── classification.py # Classification endpoints
│       │   └── combined.py      # Combined operations
│       ├── core/                # Core functionality
│       │   ├── models.py        # Pydantic models
│       │   ├── config.py        # Configuration management
│       │   └── utils.py         # Utility functions
│       └── services/            # Business logic
│           ├── report_service.py # Report handling
│           └── groq_classifier.py # AI classification
├── tests/                       # Test suite (100% passing)
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── docs/                        # Documentation
├── scripts/                     # Utility scripts
├── examples/                    # Usage examples
└── pyproject.toml              # Modern Python project configuration
```

## 📚 Documentation

- **[API Documentation](docs/API.md)** - Complete API reference
- **[Development Setup](docs/DEVELOPMENT.md)** - Development environment setup
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_main.py -v
```

## 🛠️ Development

```bash
# Install development dependencies
uv sync --dev

# Run linting
uv run ruff check src/ tests/

# Run formatting
uv run ruff format src/ tests/

# Run security checks
uv run bandit -r src/

# Run pre-commit hooks
pre-commit run --all-files
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# External Ticket API Configuration
TICKET_API_ENDPOINT=https://api.example.com/tickets

# FastAPI Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## 🎯 Hackathon Project

This project was built for the **RAISE YOUR HACK** hackathon (July 4-8, 2025) as part of the **Qualcomm Track**, demonstrating:
- AI-powered ticket classification using Groq API
- Modern Python development practices
- Comprehensive testing and documentation
- Production-ready FastAPI architecture

## 📄 License

MIT License - see LICENSE file for details.
