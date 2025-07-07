"""Ticket CRUD API endpoints."""

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

from ticket_assistant.core.models import Department
from ticket_assistant.core.models import ErrorSeverity
from ticket_assistant.database.connection import get_db
from ticket_assistant.database.models import Classification
from ticket_assistant.database.models import Ticket
from ticket_assistant.database.repositories.ticket_repository import TicketRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])


class TicketCreateRequest(BaseModel):
    """Request model for creating a new ticket."""

    name: str
    description: str
    error_message: str | None = None
    department: Department
    severity: ErrorSeverity
    assignee: str | None = None
    screenshot_url: str | None = None


class TicketUpdateRequest(BaseModel):
    """Request model for updating an existing ticket."""

    name: str | None = None
    description: str | None = None
    error_message: str | None = None
    department: Department | None = None
    severity: ErrorSeverity | None = None
    status: str | None = None
    assignee: str | None = None
    screenshot_url: str | None = None


class TicketResponse(BaseModel):
    """Response model for ticket data."""

    id: str
    name: str
    description: str
    error_message: str | None
    department: str
    severity: str
    status: str
    assignee: str | None
    screenshot_url: str | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True


class TicketListResponse(BaseModel):
    """Response model for ticket list."""

    tickets: list[TicketResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


@router.get("", response_model=TicketListResponse)
async def get_tickets(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    status: str | None = Query(None, description="Filter by status"),
    department: Department | None = Query(None, description="Filter by department"),
    severity: ErrorSeverity | None = Query(None, description="Filter by severity"),
    assignee: str | None = Query(None, description="Filter by assignee"),
    db: AsyncSession = Depends(get_db),
) -> TicketListResponse:
    """Get a paginated list of tickets with optional filters."""
    try:
        # Build query with filters
        query = select(Ticket)

        if status:
            query = query.where(Ticket.status == status)
        if department:
            query = query.where(Ticket.department == department.value)
        if severity:
            query = query.where(Ticket.severity == severity.value)
        if assignee:
            query = query.where(Ticket.assignee == assignee)

        # Add ordering
        query = query.order_by(Ticket.created_at.desc())

        # Count total results
        count_query = select(func.count(Ticket.id))
        if status:
            count_query = count_query.where(Ticket.status == status)
        if department:
            count_query = count_query.where(Ticket.department == department.value)
        if severity:
            count_query = count_query.where(Ticket.severity == severity.value)
        if assignee:
            count_query = count_query.where(Ticket.assignee == assignee)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        # Execute query
        result = await db.execute(query)
        tickets = result.scalars().all()

        # Calculate pagination info
        has_next = offset + per_page < total
        has_prev = page > 1

        return TicketListResponse(
            tickets=[TicketResponse.from_orm(ticket) for ticket in tickets],
            total=total,
            page=page,
            per_page=per_page,
            has_next=has_next,
            has_prev=has_prev,
        )

    except Exception as e:
        logger.error(f"Error fetching tickets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch tickets: {e!s}") from e


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str, db: AsyncSession = Depends(get_db)) -> TicketResponse:
    """Get a specific ticket by ID."""
    try:
        ticket_repo = TicketRepository(db)
        ticket = await ticket_repo.get_ticket_by_id(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return TicketResponse.from_orm(ticket)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch ticket: {e!s}") from e


@router.post("", response_model=TicketResponse)
async def create_ticket(ticket_data: TicketCreateRequest, db: AsyncSession = Depends(get_db)) -> TicketResponse:
    """Create a new ticket."""
    try:
        ticket_repo = TicketRepository(db)

        # Convert to dict for database creation
        ticket_dict = {
            "name": ticket_data.name,
            "description": ticket_data.description,
            "error_message": ticket_data.error_message,
            "department": ticket_data.department.value,
            "severity": ticket_data.severity.value,
            "assignee": ticket_data.assignee,
            "screenshot_url": ticket_data.screenshot_url,
            "status": "open",
        }

        ticket = await ticket_repo.create_ticket(ticket_dict)
        logger.info(f"Created ticket with ID: {ticket.id}")

        return TicketResponse.from_orm(ticket)

    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create ticket: {e!s}") from e


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str, ticket_data: TicketUpdateRequest, db: AsyncSession = Depends(get_db)
) -> TicketResponse:
    """Update an existing ticket."""
    try:
        ticket_repo = TicketRepository(db)
        ticket = await ticket_repo.get_ticket_by_id(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Update only provided fields
        if ticket_data.name is not None:
            ticket.name = ticket_data.name
        if ticket_data.description is not None:
            ticket.description = ticket_data.description
        if ticket_data.error_message is not None:
            ticket.error_message = ticket_data.error_message
        if ticket_data.department is not None:
            ticket.department = ticket_data.department.value
        if ticket_data.severity is not None:
            ticket.severity = ticket_data.severity.value
        if ticket_data.status is not None:
            ticket.status = ticket_data.status
            # Set resolved_at if status is resolved/closed
            if ticket_data.status in ["resolved", "closed"] and not ticket.resolved_at:
                ticket.resolved_at = datetime.utcnow()
        if ticket_data.assignee is not None:
            ticket.assignee = ticket_data.assignee
        if ticket_data.screenshot_url is not None:
            ticket.screenshot_url = ticket_data.screenshot_url

        ticket.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(ticket)

        logger.info(f"Updated ticket {ticket_id}")
        return TicketResponse.from_orm(ticket)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update ticket: {e!s}") from e


@router.patch("/{ticket_id}/status", response_model=TicketResponse)
async def update_ticket_status(ticket_id: str, status: str, db: AsyncSession = Depends(get_db)) -> TicketResponse:
    """Update only the status of a ticket."""
    try:
        ticket_repo = TicketRepository(db)
        ticket = await ticket_repo.update_ticket_status(ticket_id, status)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        logger.info(f"Updated ticket {ticket_id} status to {status}")
        return TicketResponse.from_orm(ticket)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating ticket {ticket_id} status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update ticket status: {e!s}") from e


@router.delete("/{ticket_id}", response_model=dict[str, Any])
async def delete_ticket(ticket_id: str, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    """Delete a ticket."""
    try:
        ticket_repo = TicketRepository(db)
        ticket = await ticket_repo.get_ticket_by_id(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        await db.delete(ticket)
        await db.commit()

        logger.info(f"Deleted ticket {ticket_id}")
        return {"message": "Ticket deleted successfully", "ticket_id": ticket_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete ticket: {e!s}") from e


@router.get("/{ticket_id}/classifications", response_model=list[dict[str, Any]])
async def get_ticket_classifications(ticket_id: str, db: AsyncSession = Depends(get_db)) -> list[dict[str, Any]]:
    """Get all classifications for a specific ticket."""
    try:
        # Check if ticket exists
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

        # Convert to dict format
        classifications_data = []
        for classification in classifications:
            classifications_data.append(
                {
                    "id": classification.id,
                    "confidence": classification.confidence,
                    "reasoning": classification.reasoning,
                    "suggested_actions": classification.suggested_actions,
                    "created_at": classification.created_at.isoformat(),
                }
            )

        return classifications_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching classifications for ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch classifications: {e!s}") from e
