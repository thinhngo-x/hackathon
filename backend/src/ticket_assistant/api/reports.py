"""Report handling endpoints."""

import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ticket_assistant.core.models import ReportRequest
from ticket_assistant.core.models import ReportResponse
from ticket_assistant.database.connection import get_db
from ticket_assistant.services.database_services import EnhancedReportService
from ticket_assistant.services.report_service import ReportService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reports", tags=["Reports"])

# Global service instance (legacy)
report_service = None


def get_report_service() -> ReportService:
    """Legacy dependency to get report service instance."""
    if report_service is None:
        raise HTTPException(status_code=500, detail="Report service not initialized")
    return report_service


@router.post("", response_model=ReportResponse)
async def create_ticket_report(report: ReportRequest, db: AsyncSession = Depends(get_db)) -> ReportResponse:
    """Create a new ticket from a report and save to database.

    This endpoint accepts a report with name, keywords, and description,
    and creates a ticket record in the database.
    """
    try:
        logger.info(f"Creating ticket from report: {report.name}")

        # Create enhanced service
        enhanced_service = EnhancedReportService()

        # Create ticket in database
        response, ticket = await enhanced_service.send_report_with_database(
            report=report,
            db_session=db,
        )

        logger.info(f"Ticket created successfully with ID: {ticket.id}")
        return response

    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create ticket: {e!s}") from e


@router.post("/legacy", response_model=ReportResponse)
async def send_report_legacy(
    report: ReportRequest, service: ReportService = Depends(get_report_service)
) -> ReportResponse:
    """Legacy endpoint that sends report to external API (for backward compatibility)."""
    try:
        logger.info(f"Received legacy report: {report.name}")
        result = await service.send_report(report)

        if result.success:
            logger.info(f"Legacy report sent successfully with ticket ID: {result.ticket_id}")
        else:
            logger.error(f"Failed to send legacy report: {result.message}")

        return result

    except Exception as e:
        logger.error(f"Error processing legacy report: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e!s}") from e


@router.post("/mock", response_model=ReportResponse)
async def create_mock_ticket_report(report: ReportRequest, db: AsyncSession = Depends(get_db)) -> ReportResponse:
    """Create a mock ticket in database for testing purposes."""
    try:
        logger.info(f"Creating mock ticket from report: {report.name}")

        # Create enhanced service
        enhanced_service = EnhancedReportService()

        # Create mock ticket in database
        response, ticket = await enhanced_service.mock_send_report_with_database(
            report=report,
            db_session=db,
        )

        logger.info(f"Mock ticket created successfully with ID: {ticket.id}")
        return response

    except Exception as e:
        logger.error(f"Error creating mock ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create mock ticket: {e!s}") from e
