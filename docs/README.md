# 📚 Documentation Index

Welcome to the Ticket Assistant API documentation. This directory contains comprehensive guides for using, developing, and deploying the application.

## 📖 Documentation Structure

### Core Documentation
- **[API.md](API.md)** - Complete API reference and endpoint documentation
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development environment setup and guidelines
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment instructions and best practices

### Project Information
- **[HACKATHON.md](HACKATHON.md)** - Hackathon project details and requirements
- **[TOOLS.md](TOOLS.md)** - Development tools and setup guides
- **[BRAINSTORM.md](BRAINSTORM.md)** - Original brainstorming ideas and track analysis

## 🚀 Quick Links

### For Developers
- [Getting Started](DEVELOPMENT.md#installation)
- [VS Code Setup](DEVELOPMENT.md#vs-code-setup)
- [Running Tests](DEVELOPMENT.md#testing)
- [Code Quality](DEVELOPMENT.md#code-quality)

### For Operations
- [Docker Deployment](DEPLOYMENT.md#docker-deployment)
- [Cloud Deployment](DEPLOYMENT.md#cloud-deployment)
- [Monitoring](DEPLOYMENT.md#monitoring-and-logging)
- [Troubleshooting](DEPLOYMENT.md#troubleshooting)

### For Users
- [API Reference](API.md)
- [Authentication](API.md#authentication)
- [Error Handling](API.md#error-handling)
- [Rate Limiting](API.md#rate-limiting)

## 🔧 Development Tools

The project uses modern Python development tools for optimal developer experience:

- **uv**: Ultra-fast Python package management
- **Ruff**: Modern linting and formatting
- **pytest**: Comprehensive testing framework
- **Pre-commit**: Code quality automation
- **VS Code**: Integrated development environment

## 📋 API Overview

The Ticket Assistant API provides four main categories of endpoints:

1. **Health Checks** (`/health`) - Service monitoring
2. **Reports** (`/reports`) - Ticket submission
3. **Classification** (`/classify`) - AI-powered error classification
4. **Combined** (`/combined`) - Integrated operations

## 🎯 Quick Start

```bash
# 1. Install dependencies
uv sync --dev

# 2. Configure environment
cp .env.example .env
# Edit .env with your Groq API key

# 3. Run the server
uv run python main.py

# 4. View documentation
open http://localhost:8000/docs
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Current status: 38/38 tests passing (100%)
```

## 🔗 External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq API Documentation](https://console.groq.com/docs)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

## 📝 Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md#contributing) for contribution guidelines.

## 📄 License

MIT License - see the main README for details.
