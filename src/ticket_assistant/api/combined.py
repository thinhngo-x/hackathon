"""Combined operations endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from ticket_assistant.core.models import ReportRequest
from ticket_assistant.services.report_service import ReportService
from ticket_assistant.services.groq_classifier import GroqClassifier
from ticket_assistant.api.reports import get_report_service
from ticket_assistant.api.classification import get_groq_classifier

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/combined", tags=["Combined Operations"])


@router.post("/classify-and-send", response_model=Dict[str, Any])
async def classify_and_send_report(
    report: ReportRequest,
    report_svc: ReportService = Depends(get_report_service),
    classifier: GroqClassifier = Depends(get_groq_classifier)
) -> Dict[str, Any]:
    """
    Combined endpoint that classifies an error and sends a report.
    
    This endpoint first classifies the error using Groq API,
    then sends the report with the classification information.
    """
    try:
        logger.info(f"Processing combined request for: {report.name}")
        
        # First, classify the error
        classification = await classifier.classify_error(
            error_description=report.description,
            error_message=report.error_message
        )
        
        # Create enhanced ticket data
        ticket_data = report_svc.create_ticket_data(
            report=report,
            department=classification.department,
            severity=classification.severity
        )
        
        # Send the report
        report_result = await report_svc.send_report(report)
        
        return {
            "report_result": report_result.dict(),
            "classification": classification.dict(),
            "ticket_data": ticket_data.dict()
        }
        
    except Exception as e:
        logger.error(f"Error in combined operation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Combined operation error: {str(e)}")


@router.post("/classify-and-send-mock", response_model=Dict[str, Any])
async def classify_and_send_report_mock(
    report: ReportRequest,
    report_svc: ReportService = Depends(get_report_service),
    classifier: GroqClassifier = Depends(get_groq_classifier)
) -> Dict[str, Any]:
    """
    Mock version of combined endpoint that classifies an error and sends a mock report.
    
    This endpoint first classifies the error using Groq API,
    then sends a mock report without calling external ticket APIs.
    """
    try:
        logger.info(f"Processing mock combined request for: {report.name}")
        
        # First, classify the error
        classification = await classifier.classify_error(
            error_description=report.description,
            error_message=report.error_message
        )
        
        # Create enhanced ticket data
        ticket_data = report_svc.create_ticket_data(
            report=report,
            department=classification.department,
            severity=classification.severity
        )
        
        # Send the mock report (no external API call)
        report_result = await report_svc.mock_send_report(report)
        
        return {
            "report_result": report_result.dict(),
            "classification": classification.dict(),
            "ticket_data": ticket_data.dict()
        }
        
    except Exception as e:
        logger.error(f"Error in mock combined operation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Mock combined operation error: {str(e)}")
