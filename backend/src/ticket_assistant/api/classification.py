"""Classification endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ticket_assistant.core.models import ClassificationRequest, ClassificationResponse
from ticket_assistant.database.connection import get_db
from ticket_assistant.services.groq_classifier import GroqClassifier

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/classification", tags=["Classification"])

# Global service instance
groq_classifier = None


def get_groq_classifier() -> GroqClassifier:
    """Dependency to get Groq classifier instance."""
    if groq_classifier is None:
        raise HTTPException(
            status_code=500,
            detail="Groq classifier not initialized. Please check GROQ_API_KEY.",
        )
    return groq_classifier


@router.post("", response_model=ClassificationResponse)
async def classify_error(
    classification_request: ClassificationRequest,
    classifier: GroqClassifier = Depends(get_groq_classifier),
) -> ClassificationResponse:
    """Classify an error and route it to the appropriate department.

    This endpoint uses Groq API to analyze the error description and
    automatically determine which department should handle the issue.
    """
    try:
        logger.info(f"Classifying error: {classification_request.error_description[:100]}...")

        result = await classifier.classify_error(
            error_description=classification_request.error_description,
            error_message=classification_request.error_message,
            context=classification_request.context,
        )

        logger.info(f"Classification result: {result.department} ({result.confidence:.2f} confidence)")

        return result

    except Exception as e:
        logger.error(f"Error in classification: {e!s}")
        raise HTTPException(status_code=500, detail=f"Classification error: {e!s}") from e
