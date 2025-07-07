"""Classification CRUD API endpoints."""

import json
import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ticket_assistant.database.connection import get_db
from ticket_assistant.database.models import Classification
from ticket_assistant.database.repositories.ticket_repository import TicketRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/classifications", tags=["Classifications"])


class ClassificationCreateRequest(BaseModel):
    """Request model for creating a new classification."""

    ticket_id: str
    confidence: float
    reasoning: str
    suggested_actions: list[str]


class ClassificationUpdateRequest(BaseModel):
    """Request model for updating an existing classification."""

    confidence: float | None = None
    reasoning: str | None = None
    suggested_actions: list[str] | None = None


class ClassificationResponse(BaseModel):
    """Response model for classification data."""

    id: str
    ticket_id: str
    confidence: float
    reasoning: str
    suggested_actions: list[str]
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, classification: Classification) -> "ClassificationResponse":
        """Create response from ORM model."""
        # Parse suggested_actions from JSON string
        try:
            suggested_actions = json.loads(classification.suggested_actions)
        except (json.JSONDecodeError, TypeError):
            suggested_actions = []

        return cls(
            id=classification.id,
            ticket_id=classification.ticket_id,
            confidence=classification.confidence,
            reasoning=classification.reasoning,
            suggested_actions=suggested_actions,
            created_at=classification.created_at,
        )


class ClassificationListResponse(BaseModel):
    """Response model for classification list."""

    classifications: list[ClassificationResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


@router.get("", response_model=ClassificationListResponse)
async def get_classifications(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    ticket_id: str | None = Query(None, description="Filter by ticket ID"),
    db: AsyncSession = Depends(get_db),
) -> ClassificationListResponse:
    """Get a paginated list of classifications with optional filters."""
    try:
        # Build query with filters
        query = select(Classification)

        if ticket_id:
            query = query.where(Classification.ticket_id == ticket_id)

        # Add ordering
        query = query.order_by(Classification.created_at.desc())

        # Count total results
        count_query = select(func.count(Classification.id))
        if ticket_id:
            count_query = count_query.where(Classification.ticket_id == ticket_id)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        # Execute query
        result = await db.execute(query)
        classifications = result.scalars().all()

        # Calculate pagination info
        has_next = offset + per_page < total
        has_prev = page > 1

        return ClassificationListResponse(
            classifications=[ClassificationResponse.from_orm(c) for c in classifications],
            total=total,
            page=page,
            per_page=per_page,
            has_next=has_next,
            has_prev=has_prev,
        )

    except Exception as e:
        logger.error(f"Error fetching classifications: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch classifications: {e!s}") from e


@router.get("/{classification_id}", response_model=ClassificationResponse)
async def get_classification(classification_id: str, db: AsyncSession = Depends(get_db)) -> ClassificationResponse:
    """Get a specific classification by ID."""
    try:
        result = await db.execute(select(Classification).where(Classification.id == classification_id))
        classification = result.scalar_one_or_none()

        if not classification:
            raise HTTPException(status_code=404, detail="Classification not found")

        return ClassificationResponse.from_orm(classification)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching classification {classification_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch classification: {e!s}") from e


@router.post("", response_model=ClassificationResponse)
async def create_classification(
    classification_data: ClassificationCreateRequest, db: AsyncSession = Depends(get_db)
) -> ClassificationResponse:
    """Create a new classification."""
    try:
        # Verify ticket exists
        ticket_repo = TicketRepository(db)
        ticket = await ticket_repo.get_ticket_by_id(classification_data.ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Create classification
        classification = Classification(
            ticket_id=classification_data.ticket_id,
            confidence=classification_data.confidence,
            reasoning=classification_data.reasoning,
            suggested_actions=json.dumps(classification_data.suggested_actions),
        )

        db.add(classification)
        await db.commit()
        await db.refresh(classification)

        logger.info(f"Created classification with ID: {classification.id}")
        return ClassificationResponse.from_orm(classification)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating classification: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create classification: {e!s}") from e


@router.put("/{classification_id}", response_model=ClassificationResponse)
async def update_classification(
    classification_id: str,
    classification_data: ClassificationUpdateRequest,
    db: AsyncSession = Depends(get_db),
) -> ClassificationResponse:
    """Update an existing classification."""
    try:
        result = await db.execute(select(Classification).where(Classification.id == classification_id))
        classification = result.scalar_one_or_none()

        if not classification:
            raise HTTPException(status_code=404, detail="Classification not found")

        # Update only provided fields
        if classification_data.confidence is not None:
            classification.confidence = classification_data.confidence
        if classification_data.reasoning is not None:
            classification.reasoning = classification_data.reasoning
        if classification_data.suggested_actions is not None:
            classification.suggested_actions = json.dumps(classification_data.suggested_actions)

        await db.commit()
        await db.refresh(classification)

        logger.info(f"Updated classification {classification_id}")
        return ClassificationResponse.from_orm(classification)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating classification {classification_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update classification: {e!s}") from e


@router.delete("/{classification_id}", response_model=dict[str, Any])
async def delete_classification(classification_id: str, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    """Delete a classification."""
    try:
        result = await db.execute(select(Classification).where(Classification.id == classification_id))
        classification = result.scalar_one_or_none()

        if not classification:
            raise HTTPException(status_code=404, detail="Classification not found")

        await db.delete(classification)
        await db.commit()

        logger.info(f"Deleted classification {classification_id}")
        return {"message": "Classification deleted successfully", "classification_id": classification_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting classification {classification_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete classification: {e!s}") from e


@router.get("/by-ticket/{ticket_id}", response_model=list[ClassificationResponse])
async def get_classifications_by_ticket(
    ticket_id: str, db: AsyncSession = Depends(get_db)
) -> list[ClassificationResponse]:
    """Get all classifications for a specific ticket."""
    try:
        # Verify ticket exists
        ticket_repo = TicketRepository(db)
        ticket = await ticket_repo.get_ticket_by_id(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Get classifications
        result = await db.execute(
            select(Classification)
            .where(Classification.ticket_id == ticket_id)
            .order_by(Classification.created_at.desc())
        )
        classifications = result.scalars().all()

        return [ClassificationResponse.from_orm(c) for c in classifications]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching classifications for ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch classifications: {e!s}") from e
