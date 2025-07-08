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

> **New to the project?** Check out [QUICKSTART.md](QUICKSTART.md) for a 30-second setup guide!

### Prerequisites

- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with npm
- Git
- Docker (optional, for deployment)

### Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or with pip: pip install uv
```

### Development Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd ticket-assistant

# 2. Quick start with the startup script (recommended)
./start.sh

# OR Manual setup:

# 3. Install root dependencies for frontend
cd frontend
npm install

# 4. Set up backend environment
cd ../backend
cp .env.example .env
# Edit .env and add your Groq API key (optional - will use mock responses if not provided)
uv sync --dev

# 5. Run both frontend and backend (Option 1: Using npm scripts)
cd ..
npm run dev

# OR Option 2: Run individually
# Terminal 1 - Backend:
cd backend
uv run python src/ticket_assistant/api/main.py

# Terminal 2 - Frontend:
cd frontend
npm run dev

# Access the application:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Backend Only

```bash
cd backend
uv run python src/ticket_assistant/api/main.py
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

### Quick Deploy to Vultr Cloud ⚡

```bash
# One-command deployment to Vultr
./scripts/quick-deploy.sh

# Or setup and deploy manually
./scripts/setup-vultr.sh
export VULTR_API_KEY="your_api_key_here"
./scripts/deploy-vultr.sh
```

### Local Development

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost
# Backend: http://localhost:8000
```

### Vultr Cloud Deployment Options

- **Single Instance** ($10/month) - Perfect for demos and testing
- **Kubernetes Cluster** ($30/month) - Production-ready with auto-scaling
- **Load Balanced** - High availability setup

See [DEPLOY.md](DEPLOY.md) for quick start or [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for comprehensive guides.

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

## 🔍 Troubleshooting

### Common Issues

1. **Backend not starting**

   - Make sure you're running the correct main file: `uv run python src/ticket_assistant/api/main.py`
   - Check that all dependencies are installed: `uv sync --dev`
   - Verify the `.env` file exists (copy from `.env.example`)

2. **Frontend not loading**

   - Ensure all npm packages are installed: `npm install`
   - Check that the backend is running on port 8000
   - Verify no other process is using port 3000

3. **Missing Groq API Key**
   - The application will work without a Groq API key using mock responses
   - To use real AI classification, add your Groq API key to the `.env` file

### Port Configuration

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

### Logs

Check the terminal output for detailed error messages. The backend uses structured logging to help with debugging.

## 🎯 Hackathon Project

This project was built for the **RAISE YOUR HACK** hackathon (July 4-8, 2025) as part of the **Vultr Track**, demonstrating:

- AI-powered ticket classification using Groq API
- Modern full-stack development with FastAPI and React
- Cloud-native deployment optimized for Vultr infrastructure
- Comprehensive testing and documentation
- Production-ready architecture with Docker support

## 📄 License

MIT License - see LICENSE file for details.
