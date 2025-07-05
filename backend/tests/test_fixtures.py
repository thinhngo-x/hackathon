"""Test configuration for async services."""

import asyncio
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from ticket_assistant.api import classification
from ticket_assistant.api import combined
from ticket_assistant.api import reports
from ticket_assistant.api.main import app
from ticket_assistant.services.groq_classifier import GroqClassifier
from ticket_assistant.services.report_service import ReportService


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def setup_test_services():
    """Set up test services for each test."""
    # Initialize test services
    report_service = ReportService(api_endpoint="https://test-api.example.com/tickets")

    # Set up mock Groq classifier
    mock_groq_classifier = AsyncMock(spec=GroqClassifier)

    # Set global service instances
    reports.report_service = report_service
    combined.report_service = report_service
    classification.groq_classifier = mock_groq_classifier
    combined.groq_classifier = mock_groq_classifier

    yield {"report_service": report_service, "groq_classifier": mock_groq_classifier}

    # Cleanup
    reports.report_service = None
    combined.report_service = None
    classification.groq_classifier = None
    combined.groq_classifier = None


@pytest.fixture
def client_with_services(setup_test_services):
    """Create a test client with properly initialized services."""
    return TestClient(app)


@pytest.fixture
def sample_report_data():
    """Sample report data for testing."""
    return {
        "name": "Login System Error",
        "keywords": ["login", "authentication", "error"],
        "description": "Users cannot log in to the system, getting 500 error",
        "error_message": "Internal Server Error: Authentication service unavailable",
        "screenshot_url": "https://example.com/error-screenshot.png",
    }


@pytest.fixture
def sample_classification_data():
    """Sample classification data for testing."""
    return {
        "name": "Database Connection Error",
        "keywords": ["database", "connection", "timeout"],
        "description": "Unable to connect to the PostgreSQL database",
        "error_message": "psycopg2.OperationalError: could not connect to server",
        "screenshot_url": "https://example.com/db-error.png",
    }
