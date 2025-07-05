# 🎫 Ticket Assistant - AI-Powered Ticket Management System

A professionally organized, AI-powered ticket reporting and classification system built with FastAPI backend and modern React frontend, optimized for deployment on Vultr cloud infrastructure.

## 🏆 RAISE YOUR HACK - Hackathon Project

**Track**: Vultr Track  
**Focus**: Modern full-stack development with AI integration and cloud-native deployment

### Key Features
- 🤖 **AI-Powered Classification** using Groq API with Llama 3.1
- ⚡ **Real-time Analysis** with instant feedback
- 🎨 **Modern React Frontend** with TypeScript and Tailwind CSS
- 🚀 **FastAPI Backend** with comprehensive testing
- ☁️ **Vultr-Optimized Deployment** with Docker and Kubernetes support

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with npm
- Docker (for deployment)

### Development Setup

```bash
# 1. Install root dependencies
npm install

# 2. Set up backend environment
cd backend
cp .env.example .env
# Edit .env and add your Groq API key
uv sync --dev

# 3. Run both frontend and backend
cd ..
npm run dev

# Backend: http://localhost:8000/docs (API documentation)
# Frontend: http://localhost:3000 (Coming soon!)
```

### Backend Only

```bash
cd backend
uv run python main.py
# Visit http://localhost:8000/docs for API documentation
```

## 🏗️ Project Structure

```
ticket-assistant/
├── backend/                    # FastAPI backend
│   ├── src/ticket_assistant/   # Python source code
│   ├── tests/                  # Backend tests (38 tests, 100% pass rate)
│   └── main.py                 # Backend entry point
├── frontend/                   # React frontend (in development)
│   ├── src/                    # React source code
│   └── vite.config.ts          # Vite configuration
├── shared/                     # Shared types and constants
│   ├── types/                  # TypeScript type definitions
│   └── constants/              # Shared constants
├── docker/                     # Docker configurations
│   ├── Dockerfile.backend      # Backend container
│   ├── Dockerfile.frontend     # Frontend container
│   └── nginx.conf              # Nginx configuration
├── docs/                       # Documentation
│   ├── HACKATHON.md           # Hackathon project details
│   ├── FRONTEND_ARCHITECTURE.md # Frontend architecture
│   └── DEPLOYMENT.md           # Vultr deployment guide
└── scripts/                    # Development scripts
```

## ✨ Features

- **Report Submission**: Send structured reports with name, keywords, and descriptions to a ticket API endpoint
- **AI Classification**: Use Groq API to automatically classify errors and route them to relevant departments
### Backend Features
- **AI-Powered Classification**: Real-time analysis using Groq API with Llama 3.1
- **Department Routing**: Automatic routing to 8 technical departments
- **Severity Assessment**: 4-level severity classification (low, medium, high, critical)
- **RESTful API**: Full FastAPI implementation with automatic documentation
- **Comprehensive Testing**: 38 tests with 100% pass rate and 76% coverage
- **Fast Package Management**: Uses `uv` for lightning-fast dependency management
- **Modern Python Structure**: Follows src/ layout best practices

### Frontend Features (In Development)
- **React 18 + Vite**: Lightning-fast development and build times
- **TypeScript**: Full type safety with shared types
- **Real-time Classification**: Live AI feedback as users type
- **Modern UI**: Tailwind CSS with shadcn/ui components
- **Responsive Design**: Mobile-first responsive design
- **Interactive Dashboard**: Analytics and metrics visualization

## 🚀 Deployment

### Quick Deploy with Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost
# Backend: http://localhost:8000
```

### Vultr Cloud Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for comprehensive Vultr deployment guides including:
- Single instance deployment
- Kubernetes (VKE) deployment
- Load balancer configuration
- Performance optimization

## 📚 Documentation

- **[Hackathon Details](docs/HACKATHON.md)** - Project concept and competition information
- **[Frontend Architecture](docs/FRONTEND_ARCHITECTURE.md)** - React frontend design and implementation plan
- **[Vultr Deployment Guide](docs/DEPLOYMENT.md)** - Complete cloud deployment instructions
- **[API Documentation](docs/API.md)** - Complete API reference
- **[Development Setup](docs/DEVELOPMENT.md)** - Development environment setup

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
