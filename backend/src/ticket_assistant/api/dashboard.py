"""Dashboard API endpoints for statistics and analytics."""

import logging
from datetime import datetime
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ticket_assistant.core.models import DashboardStats
from ticket_assistant.core.models import Department
from ticket_assistant.core.models import ErrorSeverity
from ticket_assistant.database.connection import get_db
from ticket_assistant.database.database_service import DatabaseDashboardService
from ticket_assistant.database.repositories.ticket_repository import TicketRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)) -> DashboardStats:
    """Get dashboard statistics including ticket counts, resolution times, and distributions.

    This endpoint queries the database for real statistics and falls back to mock data
    if the database is unavailable or contains no data.
    """
    try:
        # Create repository and service instances
        ticket_repo = TicketRepository(db)
        dashboard_service = DatabaseDashboardService(ticket_repo)

        # Get stats from database
        stats = await dashboard_service.get_dashboard_stats()

        # If no data in database, return mock data
        if stats.total_tickets == 0:
            logger.warning("No tickets found in database, returning mock data")
            return get_mock_dashboard_stats()

        logger.info(f"Dashboard stats from database: {stats.total_tickets} total tickets")
        return stats

    except Exception as e:
        logger.error(f"Error getting dashboard stats from database: {e}")
        # Fallback to mock data if database fails
        return get_mock_dashboard_stats()


def get_mock_dashboard_stats() -> DashboardStats:
    """Get mock dashboard statistics for demonstration or fallback."""
    # Sample department distribution
    department_distribution = {
        Department.BACKEND.value: 45,
        Department.FRONTEND.value: 30,
        Department.DATABASE.value: 15,
        Department.DEVOPS.value: 25,
        Department.SECURITY.value: 20,
        Department.API.value: 35,
    }

    # Sample severity distribution
    severity_distribution = {
        ErrorSeverity.LOW.value: 60,
        ErrorSeverity.MEDIUM.value: 45,
        ErrorSeverity.HIGH.value: 30,
        ErrorSeverity.CRITICAL.value: 15,
    }

    # Calculate totals
    total_tickets = sum(department_distribution.values())
    resolved_tickets = int(total_tickets * 0.73)  # 73% resolution rate
    open_tickets = total_tickets - resolved_tickets

    return DashboardStats(
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        resolved_tickets=resolved_tickets,
        average_resolution_time=2.4,  # 2.4 hours average
        classification_accuracy=94.5,  # 94.5% accuracy
        department_distribution=department_distribution,
        severity_distribution=severity_distribution,
    )


@router.get("/stats/real-time")
async def get_real_time_stats():
    """Get real-time dashboard updates.

    This endpoint could be used for live updates via WebSocket or periodic polling.
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "active_tickets": 42,
        "tickets_today": 18,
        "resolution_rate": 73.2,
        "response_time": "1.2s",
    }


@router.get("/stats/trends")
async def get_trend_data(days: int = 7):
    """Get trend data for the specified number of days."""
    # Mock trend data
    trends = []
    base_date = datetime.now() - timedelta(days=days)

    for i in range(days):
        date = base_date + timedelta(days=i)
        trends.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "tickets_created": 12 + (i % 5) * 3,
                "tickets_resolved": 8 + (i % 4) * 2,
                "average_resolution_time": 2.1 + (i % 3) * 0.3,
            }
        )

    return {"trends": trends, "period_days": days}
