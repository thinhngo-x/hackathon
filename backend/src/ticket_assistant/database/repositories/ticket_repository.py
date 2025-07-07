"""Ticket repository for database operations."""

from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ticket_assistant.database.models import Ticket, Classification
from ticket_assistant.core.models import Department, ErrorSeverity


class TicketRepository:
    """Repository for ticket database operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_total_count(self) -> int:
        """Get total number of tickets."""
        result = await self.session.execute(select(func.count(Ticket.id)))
        return result.scalar() or 0
    
    async def get_count_by_status(self, status: str) -> int:
        """Get count of tickets by status."""
        result = await self.session.execute(
            select(func.count(Ticket.id)).where(Ticket.status == status)
        )
        return result.scalar() or 0
    
    async def get_open_tickets_count(self) -> int:
        """Get count of open tickets (status != 'resolved' and != 'closed')."""
        result = await self.session.execute(
            select(func.count(Ticket.id)).where(
                and_(Ticket.status != "resolved", Ticket.status != "closed")
            )
        )
        return result.scalar() or 0
    
    async def get_resolved_tickets_count(self) -> int:
        """Get count of resolved tickets."""
        result = await self.session.execute(
            select(func.count(Ticket.id)).where(
                Ticket.status.in_(["resolved", "closed"])
            )
        )
        return result.scalar() or 0
    
    async def get_department_distribution(self) -> Dict[str, int]:
        """Get distribution of tickets by department."""
        result = await self.session.execute(
            select(Ticket.department, func.count(Ticket.id))
            .group_by(Ticket.department)
        )
        return {row[0]: row[1] for row in result.fetchall()}
    
    async def get_severity_distribution(self) -> Dict[str, int]:
        """Get distribution of tickets by severity."""
        result = await self.session.execute(
            select(Ticket.severity, func.count(Ticket.id))
            .group_by(Ticket.severity)
        )
        return {row[0]: row[1] for row in result.fetchall()}
    
    async def get_average_resolution_time(self) -> float:
        """Calculate average resolution time in hours for resolved tickets."""
        # Calculate average time between created_at and resolved_at
        result = await self.session.execute(
            select(
                func.avg(
                    func.julianday(Ticket.resolved_at) - func.julianday(Ticket.created_at)
                ) * 24  # Convert days to hours
            ).where(Ticket.resolved_at.is_not(None))
        )
        avg_hours = result.scalar()
        return round(avg_hours, 2) if avg_hours else 0.0
    
    async def get_tickets_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Ticket]:
        """Get tickets created within a date range."""
        result = await self.session.execute(
            select(Ticket).where(
                and_(
                    Ticket.created_at >= start_date,
                    Ticket.created_at <= end_date
                )
            )
        )
        return list(result.scalars().all())
    
    async def create_ticket(self, ticket_data: dict) -> Ticket:
        """Create a new ticket."""
        ticket = Ticket(**ticket_data)
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket
    
    async def get_ticket_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Get a ticket by ID."""
        result = await self.session.execute(
            select(Ticket).where(Ticket.id == ticket_id)
        )
        return result.scalar_one_or_none()
    
    async def update_ticket_status(self, ticket_id: str, status: str) -> Optional[Ticket]:
        """Update ticket status and set resolved_at if status is resolved."""
        ticket = await self.get_ticket_by_id(ticket_id)
        if ticket:
            ticket.status = status
            ticket.updated_at = datetime.utcnow()
            if status in ["resolved", "closed"] and not ticket.resolved_at:
                ticket.resolved_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(ticket)
        return ticket
