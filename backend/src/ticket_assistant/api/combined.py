"""Combined operations endpoints."""

import logging
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ticket_assistant.api.classification import get_groq_classifier
from ticket_assistant.api.reports import get_report_service
from ticket_assistant.core.models import ReportRequest
from ticket_assistant.database.connection import get_db
from ticket_assistant.services.database_services import EnhancedReportService
from ticket_assistant.services.groq_classifier import GroqClassifier
from ticket_assistant.services.report_service import ReportService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/combined", tags=["Combined Operations"])


@router.post("/classify-and-create-ticket", response_model=dict[str, Any])
async def classify_and_create_ticket(
    report: ReportRequest,
    db: AsyncSession = Depends(get_db),
    classifier: GroqClassifier = Depends(get_groq_classifier),
) -> dict[str, Any]:
    """Enhanced endpoint that classifies an error and creates a ticket in the database.

    This endpoint:
    1. Classifies the error using Groq API
    2. Creates a ticket in the database with the classification
    3. Returns both the ticket and classification data
    """
    try:
        logger.info(f"Processing classify-and-create-ticket request for: {report.name}")

        # First, classify the error
        classification = await classifier.classify_error(
            error_description=report.description,
            error_message=report.error_message,
            context=getattr(report, "context", None),
        )

        # Create enhanced report service
        enhanced_service = EnhancedReportService()

        # Create ticket with classification in database
        report_result, ticket = await enhanced_service.send_report_with_database(
            report=report,
            db_session=db,
            classification=classification,
        )

        # Convert ticket to dict for response
        ticket_dict = {
            "id": ticket.id,
            "name": ticket.name,
            "description": ticket.description,
            "error_message": ticket.error_message,
            "department": ticket.department,
            "severity": ticket.severity,
            "status": ticket.status,
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat(),
        }

        response_data = {
            "success": True,
            "ticket": ticket_dict,
            "classification": {
                "department": classification.department.value,
                "severity": classification.severity.value,
                "confidence": classification.confidence,
                "reasoning": classification.reasoning,
                "suggested_actions": classification.suggested_actions,
            },
            "report_result": {
                "success": report_result.success,
                "message": report_result.message,
                "ticket_id": report_result.ticket_id,
            },
        }

        logger.info(f"Successfully created ticket {ticket.id} with classification")
        return response_data

    except Exception as e:
        logger.error(f"Error in classify-and-create-ticket operation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to classify and create ticket: {e!s}") from e


@router.post("/classify-and-create-ticket-mock", response_model=dict[str, Any])
async def classify_and_create_ticket_mock(
    report: ReportRequest,
    db: AsyncSession = Depends(get_db),
    classifier: GroqClassifier = Depends(get_groq_classifier),
) -> dict[str, Any]:
    """Mock version that classifies an error and creates a ticket in database without external API calls."""
    try:
        logger.info(f"Processing mock classify-and-create-ticket request for: {report.name}")

        # First, classify the error
        classification = await classifier.classify_error(
            error_description=report.description,
            error_message=report.error_message,
            context=getattr(report, "context", None),
        )

        # Create enhanced report service
        enhanced_service = EnhancedReportService()

        # Create mock ticket with classification in database
        report_result, ticket = await enhanced_service.mock_send_report_with_database(
            report=report,
            db_session=db,
            classification=classification,
        )

        # Convert ticket to dict for response
        ticket_dict = {
            "id": ticket.id,
            "name": ticket.name,
            "description": ticket.description,
            "error_message": ticket.error_message,
            "department": ticket.department,
            "severity": ticket.severity,
            "status": ticket.status,
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat(),
        }

        response_data = {
            "success": True,
            "ticket": ticket_dict,
            "classification": {
                "department": classification.department.value,
                "severity": classification.severity.value,
                "confidence": classification.confidence,
                "reasoning": classification.reasoning,
                "suggested_actions": classification.suggested_actions,
            },
            "report_result": {
                "success": report_result.success,
                "message": report_result.message,
                "ticket_id": report_result.ticket_id,
            },
        }

        logger.info(f"Successfully created mock ticket {ticket.id} with classification")
        return response_data

    except Exception as e:
        logger.error(f"Error in mock classify-and-create-ticket operation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to classify and create mock ticket: {e!s}") from e


# Legacy endpoints for backward compatibility
@router.post("/classify-and-send-legacy", response_model=dict[str, Any])
async def classify_and_send_report_legacy(
    report: ReportRequest,
    report_svc: ReportService = Depends(get_report_service),
    classifier: GroqClassifier = Depends(get_groq_classifier),
) -> dict[str, Any]:
    """Legacy endpoint that classifies an error and sends a report to external API."""
    try:
        logger.info(f"Processing legacy combined request for: {report.name}")

        # First, classify the error
        classification = await classifier.classify_error(
            error_description=report.description, error_message=report.error_message
        )

        # Create enhanced ticket data
        ticket_data = report_svc.create_ticket_data(
            report=report,
            department=classification.department,
            severity=classification.severity,
        )

        # Send the report
        report_result = await report_svc.send_report(report)

        return {
            "report_result": report_result.dict(),
            "classification": classification.dict(),
            "ticket_data": ticket_data.dict(),
        }

    except Exception as e:
        logger.error(f"Error in legacy combined operation: {e}")
        raise HTTPException(status_code=500, detail=f"Legacy combined operation error: {e!s}") from e
