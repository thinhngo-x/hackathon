import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from ticket_assistant.services.report_service import ReportService
from ticket_assistant.core.models import ReportRequest, ReportResponse
import httpx


class TestReportService:
    
    @pytest.fixture
    def report_service(self):
        """Fixture to create a ReportService instance"""
        return ReportService(api_endpoint="https://test-api.example.com/tickets")
    
    @pytest.fixture
    def sample_report(self):
        """Fixture to create a sample report request"""
        return ReportRequest(
            name="Database Connection Error",
            keywords=["database", "connection", "timeout"],
            description="Unable to connect to the PostgreSQL database. Connection times out after 30 seconds.",
            error_message="psycopg2.OperationalError: could not connect to server",
            screenshot_url="https://example.com/screenshot.png"
        )
    
    @pytest.mark.asyncio
    async def test_send_report_success(self, report_service, sample_report):
        """Test successful report sending"""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.text = "Success"
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await report_service.send_report(sample_report)
            
            assert result.success is True
            assert result.message == "Report sent successfully"
            assert result.ticket_id is not None
            assert len(result.ticket_id) == 36  # UUID length
    
    @pytest.mark.asyncio
    async def test_send_report_api_error(self, report_service, sample_report):
        """Test report sending with API error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
            
            result = await report_service.send_report(sample_report)
            
            assert result.success is False
            assert "Failed to send report: API returned 500" in result.message
            assert result.ticket_id is None
    
    @pytest.mark.asyncio
    async def test_send_report_timeout(self, report_service, sample_report):
        """Test report sending with timeout"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.TimeoutException("Request timeout")
            )
            
            result = await report_service.send_report(sample_report)
            
            assert result.success is False
            assert "Request timeout while sending report" in result.message
            assert result.ticket_id is None
    
    @pytest.mark.asyncio
    async def test_send_report_network_error(self, report_service, sample_report):
        """Test report sending with network error"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=Exception("Network error")
            )
            
            result = await report_service.send_report(sample_report)
            
            assert result.success is False
            assert "Error sending report: Network error" in result.message
            assert result.ticket_id is None
    
    @pytest.mark.asyncio
    async def test_mock_send_report(self, report_service, sample_report):
        """Test mock report sending"""
        result = await report_service.mock_send_report(sample_report)
        
        assert result.success is True
        assert result.message == "Mock report sent successfully"
        assert result.ticket_id is not None
        assert len(result.ticket_id) == 36  # UUID length
    
    def test_create_ticket_data(self, report_service, sample_report):
        """Test ticket data creation"""
        from ticket_assistant.core.models import Department, ErrorSeverity
        
        ticket_data = report_service.create_ticket_data(
            report=sample_report,
            department=Department.DATABASE,
            severity=ErrorSeverity.HIGH
        )
        
        assert ticket_data.name == sample_report.name
        assert ticket_data.keywords == sample_report.keywords
        assert ticket_data.description == sample_report.description
        assert ticket_data.department == Department.DATABASE
        assert ticket_data.severity == ErrorSeverity.HIGH
        assert ticket_data.status == "open"
        assert ticket_data.created_at is not None
        assert len(ticket_data.id) == 36  # UUID length
    
    @pytest.mark.asyncio
    async def test_send_report_payload_structure(self, sample_report):
        """Test that the payload sent to API has correct structure"""
        report_service = ReportService(api_endpoint="https://test-api.example.com/tickets")
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_post = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value.post = mock_post
            
            await report_service.send_report(sample_report)
            
            # Verify the API call was made with correct parameters
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            
            # Check the payload structure
            payload = call_args.kwargs["json"]
            assert "ticket_id" in payload
            assert payload["name"] == sample_report.name
            assert payload["keywords"] == sample_report.keywords
            assert payload["description"] == sample_report.description
            assert payload["error_message"] == sample_report.error_message
            assert payload["screenshot_url"] == sample_report.screenshot_url
            assert "created_at" in payload
            assert payload["status"] == "open"
    
    def test_report_service_initialization(self):
        """Test ReportService initialization with different parameters"""
        # Test with custom endpoint
        service1 = ReportService(api_endpoint="https://custom.api.com/tickets")
        assert service1.api_endpoint == "https://custom.api.com/tickets"
        
        # Test with default endpoint
        service2 = ReportService()
        assert service2.api_endpoint == "https://api.example.com/tickets"


if __name__ == "__main__":
    pytest.main([__file__])
