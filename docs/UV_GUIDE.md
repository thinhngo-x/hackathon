# UV Quick Start Guide

## Installation Commands

### Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create virtual environment
```bash
uv venv
```

### Install dependencies
```bash
uv pip install -r requirements.txt
```

### Install dev dependencies
```bash
uv pip install -r dev-requirements.txt
```

### Activate virtual environment
```bash
source .venv/bin/activate  # On Unix/macOS
# .venv\Scripts\activate   # On Windows
```

### Run the application
```bash
source .venv/bin/activate
python main.py
```

### Run tests
```bash
source .venv/bin/activate
pytest
```

### Add new dependencies
```bash
uv pip install package-name
# Then add to requirements.txt manually
```

### Update dependencies
```bash
uv pip install --upgrade -r requirements.txt
```

## Benefits of using uv

- **Fast**: 10-100x faster than pip
- **Reliable**: Consistent dependency resolution
- **Simple**: Single tool for all Python package management
- **Compatible**: Works with existing PyPI packages and requirements.txt
- **Virtual environments**: Easy venv creation and management
