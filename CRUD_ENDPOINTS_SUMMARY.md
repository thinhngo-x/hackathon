# Backend CRUD Endpoints Summary

## Overview

The backend now has **full CRUD (Create, Read, Update, Delete) operations** for both tickets and classifications. Here's a comprehensive summary of all available endpoints:

## Tickets API (`/api/tickets`)

### Core CRUD Operations

- **GET** `/api/tickets` - List all tickets with pagination and filtering

  - Query params: `page`, `per_page`, `status`, `department`, `severity`, `assignee`
  - Returns: Paginated list of tickets with metadata

- **POST** `/api/tickets` - Create a new ticket

  - Body: `TicketCreateRequest` (name, description, department, severity, etc.)
  - Returns: Created ticket data

- **GET** `/api/tickets/{ticket_id}` - Get a specific ticket by ID

  - Returns: Single ticket data

- **PUT** `/api/tickets/{ticket_id}` - Update an existing ticket

  - Body: `TicketUpdateRequest` (partial updates allowed)
  - Returns: Updated ticket data

- **DELETE** `/api/tickets/{ticket_id}` - Delete a ticket
  - Returns: Success message

### Additional Ticket Operations

- **PATCH** `/api/tickets/{ticket_id}/status` - Update only ticket status

  - Body: `{"status": "new_status"}`
  - Automatically sets `resolved_at` for resolved/closed tickets

- **GET** `/api/tickets/{ticket_id}/classifications` - Get all classifications for a ticket
  - Returns: List of classifications for the specific ticket

## Classifications API (`/api/classifications`)

### Core CRUD Operations

- **GET** `/api/classifications` - List all classifications with pagination

  - Query params: `page`, `per_page`, `ticket_id` (filter by ticket)
  - Returns: Paginated list of classifications

- **POST** `/api/classifications` - Create a new classification

  - Body: `ClassificationCreateRequest` (ticket_id, confidence, reasoning, suggested_actions)
  - Returns: Created classification data

- **GET** `/api/classifications/{classification_id}` - Get a specific classification by ID

  - Returns: Single classification data

- **PUT** `/api/classifications/{classification_id}` - Update an existing classification

  - Body: `ClassificationUpdateRequest` (partial updates allowed)
  - Returns: Updated classification data

- **DELETE** `/api/classifications/{classification_id}` - Delete a classification
  - Returns: Success message

### Additional Classification Operations

- **GET** `/api/classifications/by-ticket/{ticket_id}` - Get all classifications for a specific ticket
  - Returns: List of classifications for the ticket

## Existing Non-CRUD Endpoints

### Reports API (`/api/reports`)

- **POST** `/api/reports` - Create ticket from report (primary endpoint)
- **POST** `/api/reports/legacy` - Send report to external API
- **POST** `/api/reports/mock` - Create mock ticket for testing

### Classification Service (`/api/classification`)

- **POST** `/api/classification` - Classify error description using AI

### Combined Operations (`/api/combined`)

- **POST** `/api/combined/classify-and-create-ticket` - Classify and create ticket in one step
- **POST** `/api/combined/classify-and-create-ticket-mock` - Mock version
- **POST** `/api/combined/classify-and-send-legacy` - Legacy version

### Dashboard API (`/api/dashboard`)

- **GET** `/api/dashboard/stats` - Get dashboard statistics
- **GET** `/api/dashboard/stats/real-time` - Get real-time stats
- **GET** `/api/dashboard/stats/trends` - Get trend data

### Health Checks (`/health`)

- **GET** `/health/` - Basic health check
- **GET** `/health/live` - Liveness probe
- **GET** `/health/ready` - Readiness probe

## Database Schema

### Tickets Table

- `id` (UUID, primary key)
- `name` (string, required)
- `description` (text, required)
- `error_message` (text, optional)
- `department` (string, required)
- `severity` (string, required)
- `status` (string, default: "open")
- `assignee` (string, optional)
- `screenshot_url` (string, optional)
- `created_at` (datetime)
- `updated_at` (datetime)
- `resolved_at` (datetime, nullable)

### Classifications Table

- `id` (UUID, primary key)
- `ticket_id` (UUID, foreign key to tickets)
- `confidence` (float, required)
- `reasoning` (text, required)
- `suggested_actions` (text, JSON array)
- `created_at` (datetime)

## Current Database State

- **Total tickets**: 48
- **Total classifications**: 27
- **Relationships**: Classifications are linked to tickets via foreign key

## Key Features

### Pagination

- All list endpoints support pagination with `page` and `per_page` parameters
- Returns metadata: `total`, `has_next`, `has_prev`

### Filtering

- Tickets can be filtered by: `status`, `department`, `severity`, `assignee`
- Classifications can be filtered by: `ticket_id`

### Validation

- All endpoints include proper request/response validation using Pydantic models
- Foreign key constraints ensure data integrity

### Error Handling

- Comprehensive error handling with appropriate HTTP status codes
- Detailed error messages for debugging

## Testing

All CRUD endpoints have been tested and are working correctly. The test script `test_crud_endpoints.py` demonstrates:

- Creating tickets and classifications
- Reading individual and paginated data
- Updating ticket status
- Proper error handling for not found resources

## API Documentation

The complete OpenAPI documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
