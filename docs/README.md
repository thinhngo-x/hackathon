# Ticket Assistant API

A FastAPI-based ticket reporting and classification system that uses AI to automatically categorize and route support tickets to the appropriate departments.

## Quick Start

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
make install

# 3. Set up environment
cp config/.env.example .env
# Edit .env and add your Groq API key

# 4. Run the server
make run

# 5. Visit http://localhost:8000/docs for API documentation
```

## Features

- **Report Submission**: Send structured reports with name, keywords, and descriptions to a ticket API endpoint
- **AI Classification**: Use Groq API to automatically classify errors and route them to relevant departments
- **Department Routing**: Automatic routing to backend, frontend, database, DevOps, security, API, integration, or general departments
- **Severity Assessment**: Automatic severity classification (low, medium, high, critical)
- **RESTful API**: Full FastAPI implementation with automatic documentation
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Fast Package Management**: Uses `uv` for lightning-fast dependency management
- **Modern Python Structure**: Follows src/ layout best practices

## Project Structure

```
ticket-assistant/
├── main.py                           # Legacy entry point (now empty, use scripts/run.sh)
├── src/                              # Source code following src/ layout
│   └── ticket_assistant/             # Main package
│       ├── __init__.py
│       ├── api/                      # API layer
│       │   ├── __init__.py
│       │   ├── main.py               # FastAPI application entry point
│       │   ├── health.py             # Health check endpoints
│       │   ├── reports.py            # Report submission endpoints
│       │   ├── classification.py     # AI classification endpoints
│       │   └── combined.py           # Combined operations endpoints
│       ├── services/                 # Business logic layer
│       │   ├── __init__.py
│       │   ├── report_service.py     # Report submission service
│       │   └── groq_classifier.py    # AI classification service using Groq
│       └── core/                     # Core utilities and models
│           ├── __init__.py
│           ├── models.py             # Pydantic models for data validation
│           ├── config.py             # Configuration management
│           └── utils.py              # Utility functions
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest configuration and fixtures
│   ├── unit/                         # Unit tests
│   │   ├── test_main.py              # API endpoint tests
│   │   ├── test_report_service.py    # Report service tests
│   │   └── test_groq_classifier.py   # Classification service tests
│   └── integration/                  # Integration tests
│       └── test_api_integration.py   # End-to-end API tests
├── scripts/                          # Utility scripts
│   ├── run.sh                        # Application startup script
│   └── test.sh                       # Test runner script
├── config/                           # Configuration files
│   └── .env.example                  # Environment variables template
├── docs/                             # Documentation
│   ├── README.md                     # This file
│   ├── UV_GUIDE.md                   # uv package manager guide
│   └── UV_MIGRATION_SUMMARY.md       # Migration documentation
├── examples/                         # Example usage
│   └── example_usage.py              # Demo script showing API usage
├── requirements.txt                  # Production dependencies
├── dev-requirements.txt              # Development dependencies
├── pyproject.toml                    # Project configuration and pytest settings
├── uv.lock                           # uv lock file
├── Makefile                          # Project management commands
└── .gitignore                        # Git ignore rules
```

## Installation

1. **Install uv (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or visit: https://docs.astral.sh/uv/getting-started/installation/
   ```

2. **Clone and navigate to the project directory:**
   ```bash
   cd ticket-assistant
   ```

3. **Install dependencies with uv:**
   ```bash
   # Install production dependencies
   make install
   
   # OR install with development dependencies
   make install-dev
   
   # OR use uv directly
   uv sync
   ```

4. **Set up environment variables:**
   ```bash
   cp config/.env.example .env
   # Edit .env and add your Groq API key
   ```

## Configuration

Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key_here
TICKET_API_ENDPOINT=https://api.example.com/tickets
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
```

**Important**: The default `TICKET_API_ENDPOINT` is a placeholder URL. For testing purposes, use the mock endpoints below. To integrate with a real ticketing system, replace this with your actual ticket API endpoint.

## Usage

### Running the API Server

The easiest way to run the server is using the provided scripts:

```bash
# Using the startup script (automatically finds available port)
./scripts/run.sh

# OR using make
make run

# Stop the server
./scripts/stop.sh
# OR using make
make stop
```

Alternative methods:
```bash
# Using uvicorn directly
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
uvicorn ticket_assistant.api.main:app --host 0.0.0.0 --port 8000 --reload

# Using python module
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python -m ticket_assistant.api.main
```

The API will be available at `http://localhost:8000` (or the next available port if 8000 is in use)

**Note**: The run script automatically detects if port 8000 is in use and will try ports 8001-8010 to find an available one.

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

### API Endpoints

#### 1. Send Mock Report (`POST /reports/mock`) - **Recommended for Testing**

Send a mock report for testing (doesn't call external APIs):

```bash
curl -X POST "http://localhost:8000/reports/mock" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Database Connection Error",
       "keywords": ["database", "connection", "timeout"],
       "description": "Unable to connect to PostgreSQL database",
       "error_message": "psycopg2.OperationalError: could not connect to server",
       "screenshot_url": "https://example.com/screenshot.png"
     }'
```

#### 2. Send Report (`POST /reports`) - **Requires Real Ticket API**

Submit a report to the ticket system (requires a valid `TICKET_API_ENDPOINT` in `.env`):

```bash
# Note: This will fail with default configuration since TICKET_API_ENDPOINT is a placeholder
curl -X POST "http://localhost:8000/reports" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Database Connection Error",
       "keywords": ["database", "connection", "timeout"],
       "description": "Unable to connect to PostgreSQL database",
       "error_message": "psycopg2.OperationalError: could not connect to server",
       "screenshot_url": "https://example.com/screenshot.png"
     }'
```

#### 3. Classify Error (`POST /classify`)

Classify an error using AI:

```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{
       "error_description": "React component not rendering properly",
       "error_message": "TypeError: Cannot read property of undefined",
       "context": "User attempting to load dashboard"
     }'
```

#### 4. Classify and Send Mock Report (`POST /combined/classify-and-send-mock`) - **Recommended for Testing**

Combined operation that classifies and sends a mock report (no external API calls):

```bash
curl -X POST "http://localhost:8000/combined/classify-and-send-mock" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "API Integration Error", 
       "keywords": ["api", "integration", "timeout"],
       "description": "Third-party API calls are timing out",
       "error_message": "requests.exceptions.Timeout: Request timed out"
     }'
```

#### 5. Classify and Send Report (`POST /combined/classify-and-send`) - **Requires Real Ticket API**

Combined operation that classifies and sends a report (requires valid `TICKET_API_ENDPOINT`):

```bash
# Note: This will fail with default configuration since TICKET_API_ENDPOINT is a placeholder
curl -X POST "http://localhost:8000/combined/classify-and-send" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "API Integration Error", 
       "keywords": ["api", "integration", "timeout"],
       "description": "Third-party API calls are timing out",
       "error_message": "requests.exceptions.Timeout: Request timed out"
     }'
```

## Quick Testing Guide

**For immediate testing without external dependencies**, use these mock endpoints:

1. **Basic mock report**: `POST /reports/mock`
2. **AI classification**: `POST /classify`  
3. **Combined mock operation**: `POST /combined/classify-and-send-mock`

These endpoints work out of the box with the default configuration and don't require external API setup.

---

**Note**: If you encountered curl command failures before, this was due to the default `TICKET_API_ENDPOINT` being a placeholder URL. The mock endpoints listed above resolve this issue for testing purposes.

---

## Testing

Run all tests using the provided scripts:

```bash
# Using the test script
./scripts/test.sh

# OR using make
make test
```

Run specific test categories:
```bash
# Unit tests only
make test-unit

# Integration tests only
make test-integration

# Using pytest directly
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest tests/unit/ -v
pytest tests/integration/ -v
```

Run tests with coverage:
```bash
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest --cov=src --cov-report=html
```

Code quality checks:
```bash
# Linting
make lint

# Code formatting
make format

# Type checking
make check
```

## Department Classification

The AI classifier can route tickets to the following departments:

- **Backend**: Server-side logic, business logic errors, internal API issues
- **Frontend**: UI/UX issues, client-side JavaScript errors, rendering problems  
- **Database**: Data storage, query issues, connection problems
- **DevOps**: Deployment, infrastructure, CI/CD, environment issues
- **Security**: Authentication, authorization, data privacy, vulnerability issues
- **API**: External API integration, endpoint errors, data format issues
- **Integration**: Third-party service integration, workflow automation issues
- **General**: Unclear issues or those spanning multiple departments

## Severity Levels

- **Critical**: System down, data loss, security breach
- **High**: Major functionality broken, affecting many users
- **Medium**: Moderate impact, workarounds available
- **Low**: Minor issues, cosmetic problems

## Error Handling

The system includes comprehensive error handling:

- API timeouts and network errors
- Invalid Groq API responses
- Malformed classification data
- Service initialization failures
- Graceful degradation when external services are unavailable

## Development

### Project Architecture

The project follows a modern Python src/ layout with clear separation of concerns:

- **`src/ticket_assistant/api/`**: FastAPI routers and endpoints
- **`src/ticket_assistant/services/`**: Business logic and external service integrations
- **`src/ticket_assistant/core/`**: Core models, configuration, and utilities
- **`tests/unit/`**: Unit tests for individual components
- **`tests/integration/`**: End-to-end integration tests

### Available Make Commands

```bash
make help              # Show all available commands
make install           # Install production dependencies
make install-dev       # Install development dependencies
make run              # Run the application (finds available port automatically)
make stop             # Stop the application and cleanup processes
make test             # Run all tests
make test-unit        # Run unit tests only
make test-integration # Run integration tests only
make clean            # Clean up generated files
make lint             # Run linting (flake8)
make format           # Format code (black)
make check            # Run type checking (mypy)
```

### Adding New Departments

1. Add the department to the `Department` enum in `src/ticket_assistant/core/models.py`
2. Update the classification guidelines in `src/ticket_assistant/services/groq_classifier.py`
3. Add test cases for the new department in `tests/unit/test_groq_classifier.py`

### Adding New Severity Levels

1. Add the severity to the `ErrorSeverity` enum in `src/ticket_assistant/core/models.py`
2. Update the severity guidelines in `src/ticket_assistant/services/groq_classifier.py`
3. Update test cases accordingly

### Extending the Classification Logic

The classification logic can be enhanced by:
- Adding more context to the Groq prompts in `src/ticket_assistant/services/groq_classifier.py`
- Implementing additional preprocessing steps
- Adding custom business rules for specific error patterns
- Integrating with other AI models or services

### Why src/ Layout?

This project uses the modern Python src/ layout which provides several benefits:

- **Import Safety**: Prevents accidentally importing from the working directory during development
- **Testing Isolation**: Ensures tests run against the installed package, not the source directory
- **Packaging Best Practices**: Follows modern Python packaging standards
- **Clear Structure**: Separates source code from configuration, tests, and documentation
- **Tool Compatibility**: Works well with modern Python tools like uv, pytest, and mypy

For more details about the migration to this structure, see `docs/UV_MIGRATION_SUMMARY.md`.

## Troubleshooting

### Common Issues

1. **Curl commands failing with DNS errors**: 
   - **Problem**: The default `TICKET_API_ENDPOINT=https://api.example.com/tickets` is a placeholder URL
   - **Solution**: Use the mock endpoints for testing:
     ```bash
     # Use this instead of /reports
     curl -X POST "http://localhost:8000/reports/mock" -H "Content-Type: application/json" -d '{"name": "Test", "keywords": ["test"], "description": "Test report"}'
     ```
   - **For production**: Replace `TICKET_API_ENDPOINT` in `.env` with your actual ticket API URL

2. **Connection refused errors**:
   ```bash
   # Check if the server is running
   ps aux | grep -E "(uvicorn|fastapi|ticket)" | grep -v grep
   
   # If not running, start it
   make run
   ```

3. **Port already in use**:
   ```bash
   # Option 1: Kill the process using the port
   lsof -ti :8000 | xargs kill -9
   
   # Option 2: Kill all Python processes (be careful!)
   pkill -f python
   
   # Option 3: Use a different port
   export API_PORT=8001
   ./scripts/run.sh
   
   # Option 4: Run with custom port directly
   source .venv/bin/activate
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   uvicorn ticket_assistant.api.main:app --host 0.0.0.0 --port 8001 --reload
   ```

4. **Groq API Issues**: Check that your `GROQ_API_KEY` is set correctly in the `.env` file

5. **uv project error**: The updated scripts now use direct Python execution instead of `uv run` to avoid project configuration issues

### Development Tips

- Use `make help` to see all available commands
- Run tests before committing: `make test`
- Use the provided scripts in `scripts/` for consistent development workflow
- Check `docs/UV_GUIDE.md` for detailed uv usage information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.
