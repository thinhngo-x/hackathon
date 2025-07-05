"""Integration tests for the full API."""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add src to path for imports
root_dir = Path(__file__).parent.parent.parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))

from ticket_assistant.api.main import app


class TestAPIIntegration:
    """Integration tests for the complete API."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)

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
            "description": "This is an integration test report"
        }
        
        response = client.post("/reports/mock", json=report_data)
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
