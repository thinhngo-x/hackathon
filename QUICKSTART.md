# 🚀 Quick Start Guide

## TL;DR - Get Started in 30 seconds

```bash
# 1. Clone and navigate
git clone <repository-url>
cd ticket-assistant

# 2. One-command startup
./start.sh
```

That's it! The script will:

- ✅ Check prerequisites (uv, npm)
- ✅ Install all dependencies
- ✅ Set up environment files
- ✅ Start both servers

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Prerequisites

- **Python 3.9+** with [uv](https://docs.astral.sh/uv/)
- **Node.js 18+** with npm
- **Git**

## Install Prerequisites

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Node.js (use your preferred method)
# - Visit https://nodejs.org/
# - Or use package manager: brew install node (macOS)
```

## Manual Setup (Alternative)

If you prefer manual control:

```bash
# Backend
cd backend
cp .env.example .env
uv sync --dev
uv run python src/ticket_assistant/api/main.py

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

## Troubleshooting

### Common Issues

1. **"uv: command not found"**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **"npm: command not found"**

   - Install Node.js from https://nodejs.org/

3. **Port already in use**

   - Check what's using ports 3000 or 8000
   - Kill the process or change ports in configuration

4. **Permission denied on start.sh**
   ```bash
   chmod +x start.sh
   ```

### Getting Help

- Check the full [README.md](README.md) for detailed information
- Visit [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for development setup
- Look at [docs/](docs/) for comprehensive documentation

## Next Steps

1. **Optional**: Add your Groq API key to `backend/.env` for real AI classification
2. **Development**: Check out the codebase structure
3. **Testing**: Run `npm test` to execute the test suite
4. **Deployment**: See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production setup
