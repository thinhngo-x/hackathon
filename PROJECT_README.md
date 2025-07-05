# 🎫 Ticket Assistant API

A professionally organized, AI-powered ticket reporting and classification system built with FastAPI and modern Python best practices.

## 📁 Project Structure

```
ticket-assistant/
├── src/                          # Source code
│   └── ticket_assistant/
│       ├── __init__.py
│       ├── api/                  # API layer
│       │   ├── __init__.py
│       │   ├── main.py          # Main FastAPI app
│       │   ├── health.py        # Health check endpoints
│       │   ├── reports.py       # Report endpoints
│       │   ├── classification.py # Classification endpoints
│       │   └── combined.py      # Combined operations
│       ├── core/                # Core functionality
│       │   ├── __init__.py
│       │   ├── models.py        # Pydantic models
│       │   ├── config.py        # Configuration management
│       │   └── utils.py         # Utility functions
│       └── services/            # Business logic
│           ├── __init__.py
│           ├── report_service.py # Report handling
│           └── groq_classifier.py # AI classification
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── test_main.py
│   │   ├── test_report_service.py
│   │   └── test_groq_classifier.py
│   └── integration/             # Integration tests
│       └── test_api_integration.py
├── config/                      # Configuration files
│   └── .env.example
├── docs/                        # Documentation
│   ├── README.md
│   ├── UV_GUIDE.md
│   └── UV_MIGRATION_SUMMARY.md
├── scripts/                     # Utility scripts
│   ├── run.sh
│   └── test.sh
├── examples/                    # Usage examples
│   └── example_usage.py
├── main.py                      # Application entry point
├── Makefile                     # Project commands
├── requirements.txt             # Dependencies
├── dev-requirements.txt         # Development dependencies
├── pyproject.toml              # Project configuration
└── conftest.py                 # Pytest configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup the project
git clone <repository-url>
cd ticket-assistant

# One-command setup
make setup
```

### Running the Application

```bash
# Using Makefile (recommended)
make run

# Or manually
source .venv/bin/activate
python main.py

# Development server with auto-reload
make dev
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run with coverage
source .venv/bin/activate
pytest --cov=src --cov-report=html
```

## 📖 API Documentation

Once the server is running, visit:
- **Interactive docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Development Commands

```bash
make help              # Show all available commands
make install          # Install production dependencies
make install-dev      # Install development dependencies
make clean            # Clean up generated files
make example          # Run usage example
make tree             # Show project structure
```

## 🔧 Configuration

Copy `config/.env.example` to `.env` and configure:

```env
GROQ_API_KEY=your_groq_api_key_here
TICKET_API_ENDPOINT=https://api.example.com/tickets
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
```

## 📡 API Endpoints

### Health & Status
- `GET /` - Root endpoint with API information
- `GET /health/` - Detailed health check
- `GET /health/ready` - Readiness check
- `GET /health/live` - Liveness check

### Reports
- `POST /reports` - Send report to external API
- `POST /reports/mock` - Send mock report (for testing)

### Classification
- `POST /classify` - Classify error using AI

### Combined Operations
- `POST /combined/classify-and-send` - Classify and send report

## 🏗️ Architecture

The project follows clean architecture principles:

- **API Layer** (`src/ticket_assistant/api/`): HTTP endpoints and routing
- **Services Layer** (`src/ticket_assistant/services/`): Business logic
- **Core Layer** (`src/ticket_assistant/core/`): Models, config, utilities
- **Tests** (`tests/`): Comprehensive test suite

## 🔍 Key Features

- ✅ **Modular Architecture**: Well-organized, maintainable code structure
- ✅ **Type Safety**: Full type hints with Pydantic models
- ✅ **Testing**: Comprehensive unit and integration tests
- ✅ **Configuration**: Environment-based configuration management
- ✅ **Documentation**: Auto-generated API docs with FastAPI
- ✅ **CI/CD Ready**: Structured for easy deployment
- ✅ **Development Tools**: Makefile for common tasks

## 🔄 Development Workflow

1. **Setup**: `make setup`
2. **Develop**: Edit code in `src/ticket_assistant/`
3. **Test**: `make test` (run tests frequently)
4. **Run**: `make dev` (development server with auto-reload)
5. **Check**: Ensure all tests pass before committing

## 📚 Additional Documentation

- [UV Package Manager Guide](docs/UV_GUIDE.md)
- [Migration Summary](docs/UV_MIGRATION_SUMMARY.md)
- [API Documentation](http://localhost:8000/docs) (when server is running)

## 🚀 Deployment

The project is structured for easy deployment:

```bash
# Production build
make install

# Run in production
source .venv/bin/activate
uvicorn ticket_assistant.api.main:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `make test`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
