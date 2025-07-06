# Ticket Assistant Test Suite

This directory contains all testing and utility scripts for the Ticket Assistant system, organized into logical categories.

## Directory Structure

```
tests/
├── run_tests.py              # Main test runner script
├── README.md                 # This file
├── api/                      # API integration tests
│   ├── test_integration.py   # Original backend integration test
│   └── test_api_integration.py # API endpoint testing
├── database/                 # Database testing and health checks
│   ├── test_health.py        # Async database health checker
│   ├── test_inspector.py     # Database inspection tool
│   ├── check_database.py     # Database connectivity check
│   └── check_database_simple.py # Simple SQLite-based check
├── mock/                     # Mock data generation scripts
│   ├── generate_mock_data.py # Advanced mock data generator (httpx)
│   └── simple_mock_generator.py # Simple mock data generator
└── utils/                    # Utility scripts
    └── db-check.sh           # Shell-based database checker
```

## Quick Start

### Run All Tests
```bash
cd tests/
python run_tests.py --all
```

### Set Up Environment and Generate Test Data
```bash
python run_tests.py --setup --mock
```

### Check Database Health
```bash
python run_tests.py --health
```

### Test API Endpoints
```bash
python run_tests.py --api
```

### Interactive Database Inspector
```bash
python run_tests.py --interactive
```

## Individual Test Scripts

### Database Tests

#### `test_health.py`
Comprehensive async database health checker that tests:
- Database connection
- Table existence and structure
- Repository operations
- Data integrity

```bash
python database/test_health.py
```

#### `test_inspector.py`
Advanced database inspection tool with:
- Interactive SQL query mode
- Sample data display
- Statistics and analytics
- Search functionality

```bash
python database/test_inspector.py
python database/test_inspector.py --interactive
python database/test_inspector.py --search "bug"
```

#### `check_database_simple.py`
Simple SQLite-based database checker:
- File existence check
- Table structure verification
- Basic data queries

```bash
python database/check_database_simple.py
```

### API Tests

#### `test_api_integration.py`
Tests all API endpoints:
- Health check
- Dashboard statistics
- Ticket creation and classification
- Reports generation

```bash
python api/test_api_integration.py
```

### Mock Data Generation

#### `generate_mock_data.py`
Advanced mock data generator using httpx:
- Creates realistic ticket data
- Simulates actual API usage
- Supports concurrent requests

```bash
python mock/generate_mock_data.py
```

#### `simple_mock_generator.py`
Simple mock data generator using standard library:
- No external dependencies
- Sequential ticket creation
- Basic error handling

```bash
python mock/simple_mock_generator.py
```

### Utilities

#### `db-check.sh`
Shell-based database checker with multiple commands:
- File and connection checks
- Quick statistics
- Health monitoring

```bash
bash utils/db-check.sh all
bash utils/db-check.sh quick
bash utils/db-check.sh stats
```

## Testing Workflow

### 1. Initial Setup
```bash
# Set up the database and generate initial data
python run_tests.py --setup --mock
```

### 2. Development Testing
```bash
# Check database health during development
python run_tests.py --health

# Test API endpoints after changes
python run_tests.py --api
```

### 3. Full System Test
```bash
# Run comprehensive test suite
python run_tests.py --all
```

### 4. Debugging and Inspection
```bash
# Interactive database exploration
python run_tests.py --interactive

# Generate fresh test data
python run_tests.py --mock
```

## Prerequisites

### Python Dependencies
- `httpx` (for advanced mock data generation)
- `tabulate` (for database inspector)
- `sqlalchemy` (for async database operations)
- `asyncio` (for async testing)

### Backend Server
Most API tests require the backend server to be running:
```bash
cd ../backend
python -m uvicorn src.ticket_assistant.api.main:app --reload
```

## Environment Variables

The tests will use the same environment configuration as the backend:
- Database path: `../backend/ticket_assistant.db`
- API URL: `http://localhost:8000`

## Troubleshooting

### Database Not Found
```bash
python run_tests.py --setup
```

### API Connection Failed
1. Check if backend server is running
2. Verify port 8000 is available
3. Check firewall settings

### Import Errors
Ensure you're running from the tests directory and the backend src is in the Python path.

### Permission Issues
Make shell scripts executable:
```bash
chmod +x utils/db-check.sh
```

## Contributing

When adding new tests:
1. Place them in the appropriate subdirectory
2. Update this README
3. Add them to `run_tests.py` if appropriate
4. Include proper error handling and logging
