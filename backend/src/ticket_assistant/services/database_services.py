"""Enhanced database-aware services for tickets and classifications."""

import json
import logging
from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from ticket_assistant.core.models import ClassificationResponse
from ticket_assistant.core.models import Department
from ticket_assistant.core.models import ErrorSeverity
from ticket_assistant.core.models import ReportRequest
from ticket_assistant.core.models import ReportResponse
from ticket_assistant.database.models import Classification
from ticket_assistant.database.models import Ticket
from ticket_assistant.database.repositories.ticket_repository import TicketRepository

logger = logging.getLogger(__name__)


class DatabaseTicketService:
    """Service for handling tickets with database persistence."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.ticket_repo = TicketRepository(session)

    async def create_ticket_from_report(
        self,
        report: ReportRequest,
        department: Department | None = None,
        severity: ErrorSeverity | None = None,
    ) -> Ticket:
        """Create a new ticket in the database from a report."""
        ticket_data = {
            "id": str(uuid4()),
            "name": report.name,
            "description": report.description,
            "error_message": report.error_message,
            "department": department.value if department else Department.GENERAL.value,
            "severity": severity.value if severity else ErrorSeverity.MEDIUM.value,
            "status": "open",
            "screenshot_url": report.screenshot_url,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        ticket = await self.ticket_repo.create_ticket(ticket_data)
        logger.info(f"Created ticket {ticket.id} in database")
        return ticket

    async def create_classification_for_ticket(
        self,
        ticket_id: str,
        classification: ClassificationResponse,
    ) -> Classification:
        """Create a classification record for a ticket."""
        classification_data = Classification(
            id=str(uuid4()),
            ticket_id=ticket_id,
            confidence=classification.confidence,
            reasoning=classification.reasoning,
            suggested_actions=json.dumps(classification.suggested_actions),
            created_at=datetime.utcnow(),
        )

        self.session.add(classification_data)
        await self.session.commit()
        await self.session.refresh(classification_data)

        logger.info(f"Created classification {classification_data.id} for ticket {ticket_id}")
        return classification_data

    async def create_ticket_with_classification(
        self,
        report: ReportRequest,
        classification: ClassificationResponse,
    ) -> tuple[Ticket, Classification]:
        """Create both ticket and classification in a single transaction."""
        # Create ticket
        ticket = await self.create_ticket_from_report(
            report=report,
            department=classification.department,
            severity=classification.severity,
        )

        # Create classification
        classification_record = await self.create_classification_for_ticket(
            ticket_id=ticket.id,
            classification=classification,
        )

        return ticket, classification_record


class EnhancedReportService:
    """Enhanced report service with database integration."""

    def __init__(self, api_endpoint: str | None = None):
        self.api_endpoint = api_endpoint or "https://api.example.com/tickets"

    async def send_report_with_database(
        self,
        report: ReportRequest,
        db_session: AsyncSession,
        classification: ClassificationResponse | None = None,
    ) -> tuple[ReportResponse, Ticket]:
        """Send report and save to database."""
        try:
            # Create database service
            db_service = DatabaseTicketService(db_session)

            # Create ticket in database
            if classification:
                ticket, _ = await db_service.create_ticket_with_classification(report, classification)
            else:
                ticket = await db_service.create_ticket_from_report(report)

            # Create successful response
            response = ReportResponse(
                success=True,
                message="Ticket created successfully",
                ticket_id=ticket.id,
            )

            logger.info(f"Successfully created ticket {ticket.id} in database")
            return response, ticket

        except Exception as e:
            logger.error(f"Error creating ticket in database: {e}")
            # Create error response
            response = ReportResponse(
                success=False,
                message=f"Failed to create ticket: {e!s}",
                ticket_id=None,
            )
            raise Exception(f"Database ticket creation failed: {e}") from e

    async def mock_send_report_with_database(
        self,
        report: ReportRequest,
        db_session: AsyncSession,
        classification: ClassificationResponse | None = None,
    ) -> tuple[ReportResponse, Ticket]:
        """Mock version that only saves to database without external API calls."""
        # Simulate API delay
        import asyncio

        await asyncio.sleep(0.1)

        # Use the same database logic as the real version
        return await self.send_report_with_database(report, db_session, classification)
