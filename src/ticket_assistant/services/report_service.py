import httpx
import uuid
from datetime import datetime
from typing import Dict, Any
import logging
from ticket_assistant.core.models import ReportRequest, ReportResponse, TicketData, Department, ErrorSeverity

logger = logging.getLogger(__name__)


class ReportService:
    def __init__(self, api_endpoint: str = None):
        self.api_endpoint = api_endpoint or "https://api.example.com/tickets"
        
    async def send_report(self, report: ReportRequest) -> ReportResponse:
        """
        Send a report to the ticketing system API endpoint
        """
        try:
            # Generate a unique ticket ID
            ticket_id = str(uuid.uuid4())
            
            # Prepare the payload
            payload = {
                "ticket_id": ticket_id,
                "name": report.name,
                "keywords": report.keywords,
                "description": report.description,
                "error_message": report.error_message,
                "screenshot_url": report.screenshot_url,
                "created_at": datetime.utcnow().isoformat(),
                "status": "open"
            }
            
            # Send the report to the API endpoint
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
                
                if response.status_code == 200 or response.status_code == 201:
                    return ReportResponse(
                        success=True,
                        message="Report sent successfully",
                        ticket_id=ticket_id
                    )
                else:
                    logger.error(f"API returned status {response.status_code}: {response.text}")
                    return ReportResponse(
                        success=False,
                        message=f"Failed to send report: API returned {response.status_code}",
                        ticket_id=None
                    )
                    
        except httpx.TimeoutException:
            logger.error("Timeout while sending report to API")
            return ReportResponse(
                success=False,
                message="Request timeout while sending report",
                ticket_id=None
            )
        except Exception as e:
            logger.error(f"Error sending report: {str(e)}")
            return ReportResponse(
                success=False,
                message=f"Error sending report: {str(e)}",
                ticket_id=None
            )
    
    def create_ticket_data(self, report: ReportRequest, department: Department, severity: ErrorSeverity) -> TicketData:
        """
        Create a TicketData object from a report and classification
        """
        ticket_id = str(uuid.uuid4())
        
        return TicketData(
            id=ticket_id,
            name=report.name,
            keywords=report.keywords,
            description=report.description,
            department=department,
            severity=severity,
            status="open",
            created_at=datetime.utcnow().isoformat()
        )
    
    async def mock_send_report(self, report: ReportRequest) -> ReportResponse:
        """
        Mock version of send_report for testing purposes
        """
        # Simulate API call delay
        import asyncio
        await asyncio.sleep(0.1)
        
        # Generate mock ticket ID
        ticket_id = str(uuid.uuid4())
        
        return ReportResponse(
            success=True,
            message="Mock report sent successfully",
            ticket_id=ticket_id
        )
