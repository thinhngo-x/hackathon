"""Database service for dashboard statistics."""

import logging
from typing import Dict

from ticket_assistant.core.models import DashboardStats
from ticket_assistant.database.repositories.ticket_repository import TicketRepository

logger = logging.getLogger(__name__)


class DatabaseDashboardService:
    """Service for calculating dashboard statistics from database."""
    
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repo = ticket_repository
    
    async def get_dashboard_stats(self) -> DashboardStats:
        """Calculate dashboard statistics from database."""
        try:
            # Get basic counts
            total_tickets = await self.ticket_repo.get_total_count()
            open_tickets = await self.ticket_repo.get_open_tickets_count()
            resolved_tickets = await self.ticket_repo.get_resolved_tickets_count()
            
            # Get distributions
            department_distribution = await self.ticket_repo.get_department_distribution()
            severity_distribution = await self.ticket_repo.get_severity_distribution()
            
            # Get average resolution time
            avg_resolution_time = await self.ticket_repo.get_average_resolution_time()
            
            # Calculate classification accuracy (mock for now - would need classification data)
            classification_accuracy = 94.5  # TODO: Calculate from actual classification data
            
            stats = DashboardStats(
                total_tickets=total_tickets,
                open_tickets=open_tickets,
                resolved_tickets=resolved_tickets,
                average_resolution_time=avg_resolution_time,
                classification_accuracy=classification_accuracy,
                department_distribution=department_distribution,
                severity_distribution=severity_distribution,
            )
            
            logger.info(f"Dashboard stats calculated: {total_tickets} total tickets")
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating dashboard stats: {e}")
            # Return fallback mock data if database fails
            return self._get_fallback_stats()
    
    def _get_fallback_stats(self) -> DashboardStats:
        """Fallback statistics if database is unavailable."""
        return DashboardStats(
            total_tickets=0,
            open_tickets=0,
            resolved_tickets=0,
            average_resolution_time=0.0,
            classification_accuracy=0.0,
            department_distribution={},
            severity_distribution={},
        )
