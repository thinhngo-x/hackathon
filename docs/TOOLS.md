# 🔧 Development Tools Guide

This document covers the development tools used in the Ticket Assistant project and their setup instructions.

## 📦 uv - Ultra-fast Python Package Manager

**uv** is a fast Python package manager written in Rust that replaces pip, virtualenv, and more.

### Installation

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Or with Homebrew (macOS)
brew install uv
```

### Basic Commands

```bash
# Create virtual environment
uv venv

# Install dependencies from pyproject.toml
uv sync

# Install with dev dependencies
uv sync --dev

# Add a new dependency
uv add package_name

# Add a development dependency
uv add --dev package_name

# Remove a dependency
uv remove package_name

# Run commands in the virtual environment
uv run python main.py
uv run pytest tests/

# Update dependencies
uv sync --upgrade
```

### Benefits of uv

- **Speed**: 10-100x faster than pip
- **Consistency**: Lock file ensures reproducible installs
- **Compatibility**: Drop-in replacement for pip
- **Modern**: Built for modern Python packaging standards

### Migration from pip

```bash
# Old way with pip
pip install -r requirements.txt
pip install -r dev-requirements.txt
python -m venv .venv
source .venv/bin/activate

# New way with uv
uv sync --dev
# Virtual environment is automatically managed
```

## 🔒 Pre-commit Hooks

Pre-commit hooks ensure code quality and consistency before commits are made to the repository.

### Installation

```bash
# Install pre-commit (included in dev dependencies)
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Or run the setup script
./scripts/setup.fish
```

### Manual Execution

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run

# Run specific hook
pre-commit run ruff
pre-commit run bandit
```

### Configured Tools

#### 1. **Ruff** - Modern Python Linter & Formatter
- **Replaces**: black, flake8, isort, pyupgrade, and more
- **Features**: Fast Rust-based linting, automatic fixes
- **Configuration**: `pyproject.toml`

```bash
# Run manually
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run ruff check --fix src/ tests/
```

#### 2. **Bandit** - Security Scanner
- **Purpose**: Detects common security issues in Python code
- **Output**: JSON report in `bandit-report.json`
- **Current Status**: 2 minor issues (acceptable for development)

```bash
# Run manually
uv run bandit -r src/ -f json -o bandit-report.json
```

#### 3. **Safety** - Dependency Vulnerability Scanner
- **Purpose**: Checks for known security vulnerabilities in dependencies
- **Current Status**: Clean - no vulnerabilities found

```bash
# Run manually
uv run safety check
```

#### 4. **Detect-secrets** - Secret Detection
- **Purpose**: Prevents API keys, passwords, etc. from being committed
- **Configuration**: `.secrets.baseline` file
- **Features**: Scans all file types for potential secrets

```bash
# Run manually
detect-secrets scan --all-files
```

#### 5. **Pre-commit-hooks** - Basic File Quality
- **Trailing whitespace**: Automatically removed
- **File validation**: YAML, TOML, JSON syntax checking
- **File size limits**: Prevents large files from being committed
- **Line ending normalization**: Ensures consistent line endings

### Configuration

The pre-commit configuration is in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.15
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/, -f, json, -o, bandit-report.json]

  - repo: https://github.com/gitguardian/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files
```

### Bypassing Hooks

```bash
# Skip all hooks for a commit
git commit --no-verify -m "emergency fix"

# Skip specific hook
SKIP=ruff git commit -m "skip ruff check"
```

## 🧪 pytest - Testing Framework

### Basic Usage

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/unit/test_main.py -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run tests matching pattern
uv run pytest tests/ -k "test_classify" -v

# Run tests in parallel (with pytest-xdist)
uv run pytest tests/ -n auto
```

### Configuration

Pytest configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = ["-v", "--tb=short", "--strict-markers"]
markers = [
    "asyncio: marks tests as async",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
asyncio_mode = "auto"
pythonpath = ["src"]
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures
├── unit/                       # Unit tests
│   ├── test_main.py           # API endpoint tests
│   ├── test_groq_classifier.py # AI classification tests
│   └── test_report_service.py # Report service tests
└── integration/               # Integration tests
    └── test_api_integration.py # Full API tests
```

## 🏷️ Ruff - Linting and Formatting

### Configuration

Ruff configuration is in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
    "SIM", # flake8-simplify
    "S",   # flake8-bandit (security)
    "N",   # pep8-naming
    "D",   # pydocstyle
    "RUF", # ruff-specific rules
]
```

### Commands

```bash
# Check for issues
uv run ruff check src/ tests/

# Fix issues automatically
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/

# Show available rules
uv run ruff linter
```

## 💻 VS Code Integration

### Extensions

The project includes recommended extensions in `.vscode/extensions.json`:

- **Python** - Python language support
- **Pylance** - Advanced Python language server
- **Ruff** - Linting and formatting
- **Test Explorer** - Test discovery and running
- **GitLens** - Git integration
- **Thunder Client** - API testing

### Settings

Key VS Code settings in `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": true,
            "source.organizeImports.ruff": true
        }
    }
}
```

### Tasks

Available VS Code tasks (Ctrl+Shift+P → "Tasks: Run Task"):

- **Install Dependencies** - `uv sync --dev`
- **Run Tests** - `uv run pytest tests/ -v`
- **Run Tests with Coverage** - `uv run pytest --cov=src`
- **Lint with Ruff** - `uv run ruff check src/ tests/`
- **Format with Ruff** - `uv run ruff format src/ tests/`
- **Security Check** - `uv run bandit -r src/`
- **Start API Server** - `uv run python main.py`

### Debugging

Debug configuration in `.vscode/launch.json`:

```json
{
    "name": "Python: FastAPI",
    "type": "python",
    "request": "launch",
    "program": "main.py",
    "console": "integratedTerminal",
    "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
    }
}
```

## 🚀 Workflow Integration

### Development Workflow

1. **Setup**: `uv sync --dev && pre-commit install`
2. **Development**: Make changes with VS Code
3. **Testing**: `uv run pytest tests/ -v`
4. **Quality**: Pre-commit runs automatically on commit
5. **Manual checks**: `uv run ruff check --fix src/ tests/`

### CI/CD Integration

For GitHub Actions or similar:

```yaml
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: uv sync --dev

- name: Run tests
  run: uv run pytest tests/ --cov=src

- name: Run linting
  run: uv run ruff check src/ tests/

- name: Run security checks
  run: uv run bandit -r src/
```

## 🔧 Troubleshooting

### Common Issues

1. **uv not found**: Ensure uv is in PATH after installation
2. **Pre-commit not running**: Run `pre-commit install` after cloning
3. **Python version conflicts**: Ensure Python 3.9+ is available
4. **VS Code extension issues**: Reload window after installing extensions
5. **Test failures**: Ensure all dependencies are installed with `uv sync --dev`

### Performance Tips

1. **Use uv for all Python operations** - It's much faster than pip
2. **Enable VS Code autosave** - Combined with format-on-save for immediate feedback
3. **Run tests frequently** - Use VS Code test explorer for quick feedback
4. **Use pre-commit** - Catches issues before they reach CI/CD

### Getting Help

- **uv**: [Documentation](https://docs.astral.sh/uv/)
- **Ruff**: [Documentation](https://docs.astral.sh/ruff/)
- **pytest**: [Documentation](https://docs.pytest.org/)
- **Pre-commit**: [Documentation](https://pre-commit.com/)
