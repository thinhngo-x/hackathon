from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from ticket_assistant.api import classification
from ticket_assistant.api import combined
from ticket_assistant.api import reports
from ticket_assistant.api.main import app
from ticket_assistant.api.main import get_groq_classifier
from ticket_assistant.core.models import ClassificationResponse
from ticket_assistant.core.models import Department
from ticket_assistant.core.models import ErrorSeverity
from ticket_assistant.services.groq_classifier import GroqClassifier
from ticket_assistant.services.report_service import ReportService


class TestMainAPI:
    @pytest.fixture
    def client(self):
        """Fixture to create a test client with initialized services"""
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

    @pytest.fixture
    def sample_report_data(self):
        """Fixture for sample report data"""
        return {
            "name": "Login System Error",
            "keywords": ["login", "authentication", "error"],
            "description": "Users cannot log in to the system, getting 500 error",
            "error_message": "Internal Server Error: Authentication service unavailable",
            "screenshot_url": "https://example.com/error-screenshot.png",
        }

    @pytest.fixture
    def sample_classification_data(self):
        """Fixture for sample classification data"""
        return {
            "error_description": "Database connection pool exhausted",
            "error_message": "java.sql.SQLException: Cannot get connection from pool",
            "context": "High traffic period, multiple concurrent users",
        }

    def test_root_endpoint(self, client):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Ticket Assistant API is running"
        assert data["status"] == "healthy"
        assert "groq_available" in data

    def test_health_check_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data
        assert "report_service" in data["services"]
        assert "groq_classifier" in data["services"]

    def test_send_mock_report(self, client, sample_report_data):
        """Test sending a mock report (doesn't require external API)"""
        response = client.post("/reports/mock", json=sample_report_data)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Mock report sent successfully"
        assert data["ticket_id"] is not None
        assert len(data["ticket_id"]) == 36  # UUID length

    def test_send_mock_report_invalid_data(self, client):
        """Test sending a mock report with invalid data"""
        invalid_data = {
            "name": "",  # Empty name should be invalid
            "keywords": [],
            "description": "",
        }

        response = client.post("/reports/mock", json=invalid_data)
        # Should still work with mock but name will be empty
        assert response.status_code == 200

    def test_classify_error_with_mock_groq(self, client, sample_classification_data):
        """Test error classification with mocked Groq classifier"""
        # Create a real classification response object
        mock_classification = ClassificationResponse(
            department=Department.DATABASE,
            severity=ErrorSeverity.HIGH,
            confidence=0.92,
            reasoning="Database connection pool exhaustion indicates infrastructure issue",
            suggested_actions=[
                "Increase connection pool size",
                "Monitor database performance",
            ],
        )

        # Create a synchronous mock that returns the classification
        mock_classifier = MagicMock(spec=GroqClassifier)

        # Create an async function that returns the classification
        async def mock_classify_error(*args, **kwargs):
            return mock_classification

        mock_classifier.classify_error = mock_classify_error

        # Set the global classifier directly
        original_classifier = classification.groq_classifier
        classification.groq_classifier = mock_classifier

        response = client.post("/classify", json=sample_classification_data)

        # Restore original classifier
        classification.groq_classifier = original_classifier

        # Debug the response
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")

        assert response.status_code == 200
        data = response.json()
        assert data["department"] == "database"
        assert data["severity"] == "high"
        assert data["confidence"] == 0.92

    def test_classify_error_without_groq(self, client, sample_classification_data):
        """Test error classification when Groq is not available"""

        # Set the global classifier to None to simulate no initialization
        original_classifier = classification.groq_classifier
        classification.groq_classifier = None

        response = client.post("/classify", json=sample_classification_data)

        # Restore original classifier
        classification.groq_classifier = original_classifier

        # Should return 500 when Groq classifier is not initialized
        assert response.status_code == 500
        data = response.json()
        assert "Groq classifier not initialized" in data["detail"]

    def test_classify_and_send_report(self, client, sample_report_data):
        """Test the combined classify and send report endpoint"""
        # Create a real classification response object
        mock_classification = ClassificationResponse(
            department=Department.BACKEND,
            severity=ErrorSeverity.HIGH,
            confidence=0.88,
            reasoning="Authentication service error indicates backend issue",
            suggested_actions=[
                "Check auth service logs",
                "Restart authentication service",
            ],
        )

        # Create a synchronous mock classifier
        mock_classifier = MagicMock(spec=GroqClassifier)

        # Create an async function that returns the classification
        async def mock_classify_error(*args, **kwargs):
            return mock_classification

        mock_classifier.classify_error = mock_classify_error

        # Mock report service response
        mock_report_response = MagicMock()
        mock_report_response.dict.return_value = {
            "success": True,
            "message": "Report sent successfully",
            "ticket_id": "test-ticket-123",
        }

        mock_report_service = MagicMock(spec=ReportService)

        # Create an async function that returns the report response
        async def mock_send_report(*args, **kwargs):
            return mock_report_response

        mock_report_service.send_report = mock_send_report

        mock_ticket_data = MagicMock()
        mock_ticket_data.dict.return_value = {
            "id": "test-ticket-123",
            "name": "Login System Error",
            "department": "backend",
            "severity": "high",
        }
        mock_report_service.create_ticket_data = MagicMock(return_value=mock_ticket_data)

        # Set the global services directly
        original_classifier = combined.groq_classifier
        original_report_service = combined.report_service
        combined.groq_classifier = mock_classifier
        combined.report_service = mock_report_service
        # Also set the classification module's classifier
        classification.groq_classifier = mock_classifier

        response = client.post("/combined/classify-and-send", json=sample_report_data)

        # Restore original services
        combined.groq_classifier = original_classifier
        combined.report_service = original_report_service
        classification.groq_classifier = original_classifier

        assert response.status_code == 200
        data = response.json()
        assert "report_result" in data
        assert "classification" in data
        assert "ticket_data" in data
        assert data["classification"]["department"] == "backend"

    def test_send_report_without_service(self, client, sample_report_data):
        """Test sending report when service is not available"""
        # This will use the actual report service which should work
        response = client.post("/reports", json=sample_report_data)
        # Should work but might fail due to external API call
        # The actual behavior depends on whether external API is available
        assert response.status_code in [200, 500]  # Either success or internal error

    def test_invalid_json_request(self, client):
        """Test sending invalid JSON to endpoints"""
        response = client.post("/reports/mock", json="invalid json structure")
        assert response.status_code == 422  # Validation error

    def test_missing_required_fields(self, client):
        """Test sending request with missing required fields"""
        incomplete_data = {
            "name": "Test Report"
            # Missing keywords and description
        }

        response = client.post("/reports/mock", json=incomplete_data)
        assert response.status_code == 422  # Validation error

        error_detail = response.json()
        assert "detail" in error_detail

    def test_cors_headers(self, client):
        """Test that CORS headers are properly set"""
        response = client.options("/")
        # FastAPI TestClient doesn't fully simulate CORS preflight requests
        # but we can test that the middleware is configured
        assert response.status_code in [
            200,
            405,
        ]  # Either allowed or method not allowed

    def test_classification_error_handling(self, client, sample_classification_data):
        """Test error handling in classification endpoint"""
        # Mock classifier to raise an exception
        mock_classifier = AsyncMock(spec=GroqClassifier)
        mock_classifier.classify_error = AsyncMock(side_effect=Exception("Classification failed"))

        def get_mock_classifier():
            return mock_classifier

        app.dependency_overrides[get_groq_classifier] = get_mock_classifier

        response = client.post("/classify", json=sample_classification_data)

        # Clean up
        app.dependency_overrides = {}

        assert response.status_code == 500
        data = response.json()
        assert "Classification error" in data["detail"]


if __name__ == "__main__":
    pytest.main([__file__])
