# Mock Data Generation Scripts

This directory contains scripts for generating test data for the Ticket Assistant system.

## Scripts

### `generate_mock_data.py`
Advanced mock data generator using httpx for concurrent API requests.

**Features:**
- Realistic ticket data templates
- Concurrent request processing
- Comprehensive error handling
- Progress tracking

**Usage:**
```bash
python generate_mock_data.py
```

**Dependencies:**
- httpx
- asyncio

### `simple_mock_generator.py`
Simple mock data generator using only Python standard library.

**Features:**
- No external dependencies
- Sequential ticket creation
- Basic error handling
- Lightweight implementation

**Usage:**
```bash
python simple_mock_generator.py
```

**Dependencies:**
- Python standard library only

## Mock Data Templates

Both scripts use realistic ticket data including:
- Bug reports
- Feature requests
- Support tickets
- Technical issues
- User feedback

Categories include:
- Bug
- Feature Request
- Support
- Enhancement
- Question

Priorities include:
- High
- Medium
- Low

## Configuration

Both scripts are configured to:
- Target API: `http://localhost:8000`
- Generate 50 tickets by default
- Include realistic descriptions and titles
- Simulate various user types and departments
