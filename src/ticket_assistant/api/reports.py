"""Report handling endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from ticket_assistant.core.models import ReportRequest, ReportResponse, TicketData
from ticket_assistant.services.report_service import ReportService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["Reports"])

# Global service instance
report_service = None


def get_report_service() -> ReportService:
    """Dependency to get report service instance"""
    if report_service is None:
        raise HTTPException(status_code=500, detail="Report service not initialized")
    return report_service


@router.post("", response_model=ReportResponse)
async def send_report(
    report: ReportRequest,
    service: ReportService = Depends(get_report_service)
) -> ReportResponse:
    """
    Send a report to the ticketing system.
    
    This endpoint accepts a report with name, keywords, and description,
    and forwards it to the configured ticket API endpoint.
    """
    try:
        logger.info(f"Received report: {report.name}")
        result = await service.send_report(report)
        
        if result.success:
            logger.info(f"Report sent successfully with ticket ID: {result.ticket_id}")
        else:
            logger.error(f"Failed to send report: {result.message}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/mock", response_model=ReportResponse)
async def send_mock_report(
    report: ReportRequest,
    service: ReportService = Depends(get_report_service)
) -> ReportResponse:
    """Mock endpoint for testing report sending without external API calls"""
    try:
        result = await service.mock_send_report(report)
        return result
    except Exception as e:
        logger.error(f"Error in mock report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Mock report error: {str(e)}")
