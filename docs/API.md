# 🔗 API Documentation

## Overview

The Ticket Assistant API provides endpoints for submitting, classifying, and routing support tickets using AI-powered classification.

## Base URL

```
http://localhost:8000
```

## Authentication

Some endpoints require a Groq API key to be configured in the environment variables.

## Endpoints

### Health Check

#### GET `/health`
Returns the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-05T12:00:00Z",
  "services": {
    "report_service": "available",
    "groq_classifier": "available"
  }
}
```

### Reports

#### POST `/reports/mock`
Submit a mock report (for testing purposes).

**Request Body:**
```json
{
  "name": "Login System Error",
  "keywords": ["login", "authentication", "error"],
  "description": "Users cannot log in to the system, getting 500 error",
  "error_message": "Internal Server Error: Authentication service unavailable",
  "screenshot_url": "https://example.com/error-screenshot.png"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Mock report sent successfully",
  "ticket_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### POST `/reports`
Submit a real report to the configured ticket API.

**Request Body:** Same as mock endpoint
**Response:** Depends on external API response

### Classification

#### POST `/classify`
Classify an error using AI.

**Request Body:**
```json
{
  "error_description": "Database connection pool exhausted",
  "error_message": "java.sql.SQLException: Cannot get connection from pool",
  "context": "High traffic period, multiple concurrent users"
}
```

**Response:**
```json
{
  "department": "database",
  "severity": "high",
  "confidence": 0.95,
  "reasoning": "Database connection pool exhaustion indicates infrastructure issue requiring immediate attention",
  "suggested_actions": [
    "Check database server status",
    "Verify network connectivity",
    "Review connection pool settings"
  ]
}
```

### Combined Operations

#### POST `/combined/classify-and-send`
Classify an error and submit a report in one operation.

**Request Body:** Same as reports endpoint
**Response:**
```json
{
  "report_result": {
    "success": true,
    "message": "Report sent successfully",
    "ticket_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "classification": {
    "department": "backend",
    "severity": "high",
    "confidence": 0.88,
    "reasoning": "Authentication service error indicates backend issue",
    "suggested_actions": ["Check auth service logs", "Restart authentication service"]
  },
  "ticket_data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Login System Error",
    "department": "backend",
    "severity": "high"
  }
}
```

#### POST `/combined/classify-and-send-mock`
Mock version of the combined operation (for testing).

**Request Body:** Same as above
**Response:** Same structure but with mock data

## Data Models

### ReportRequest
```python
{
  "name": str,                    # Report name
  "keywords": List[str],          # Keywords for categorization
  "description": str,             # Detailed description
  "error_message": str,           # Error message (optional)
  "screenshot_url": str           # Screenshot URL (optional)
}
```

### ClassificationRequest
```python
{
  "error_description": str,       # Error description
  "error_message": str,           # Error message (optional)
  "context": str                  # Additional context (optional)
}
```

### Departments
- `backend` - Backend/server issues
- `frontend` - UI/client issues
- `database` - Database-related issues
- `devops` - Infrastructure/deployment issues
- `security` - Security-related issues
- `api` - API-specific issues
- `integration` - Integration issues
- `general` - General or uncategorized issues

### Severity Levels
- `low` - Minor issues
- `medium` - Moderate issues
- `high` - Important issues requiring attention
- `critical` - Critical issues requiring immediate action

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `422` - Validation error
- `500` - Internal server error

Error responses include detailed messages:
```json
{
  "detail": "Error description"
}
```

## Rate Limiting

Currently no rate limiting is implemented, but consider implementing it for production use.

## Interactive Documentation

Visit `/docs` for Swagger UI documentation or `/redoc` for ReDoc documentation.
