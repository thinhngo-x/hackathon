"""Integration tests for the full API."""

import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

# Add src to path for imports
root_dir = Path(__file__).parent.parent.parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

# Import after path modification
from ticket_assistant.api import classification
from ticket_assistant.api import combined
from ticket_assistant.api import reports
from ticket_assistant.api.main import app
from ticket_assistant.services.groq_classifier import GroqClassifier
from ticket_assistant.services.report_service import ReportService


class TestAPIIntegration:
    """Integration tests for the complete API."""

    @pytest.fixture
    def client(self):
        """Create a test client with initialized services."""
        # Initialize test services
        report_service = ReportService(api_endpoint="https://test-api.example.com/tickets")

        # Set up mock Groq classifier
        mock_groq_classifier = AsyncMock(spec=GroqClassifier)

        # Set global service instances for the duration of the test
        reports.report_service = report_service
        combined.report_service = report_service
        classification.groq_classifier = mock_groq_classifier
        combined.groq_classifier = mock_groq_classifier

        client = TestClient(app)
        yield client

        # Cleanup after test
        reports.report_service = None
        combined.report_service = None
        classification.groq_classifier = None
        combined.groq_classifier = None

    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Ticket Assistant API is running"
        assert data["status"] == "healthy"
        assert "version" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_readiness_check(self, client):
        """Test readiness check."""
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_liveness_check(self, client):
        """Test liveness check."""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"

    def test_mock_report_endpoint(self, client):
        """Test mock report endpoint."""
        report_data = {
            "name": "Integration Test Report",
            "keywords": ["test", "integration"],
            "description": "This is an integration test report",
        }

        response = client.post("/api/reports/mock", json=report_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["ticket_id"] is not None

    def test_api_documentation(self, client):
        """Test that API documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema(self, client):
        """Test OpenAPI schema generation."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Ticket Assistant API"
