"""Seed data for populating the database with sample tickets."""

import asyncio
import json
from datetime import datetime
from datetime import timedelta
from random import choice
from random import randint
from random import uniform

from ticket_assistant.core.models import Department
from ticket_assistant.core.models import ErrorSeverity
from ticket_assistant.database.connection import AsyncSessionLocal
from ticket_assistant.database.connection import init_db
from ticket_assistant.database.models import Classification
from ticket_assistant.database.models import Ticket

# Sample data templates
SAMPLE_TICKETS = [
    {
        "name": "Authentication service returning 500 errors",
        "description": "Users are unable to log in due to authentication service failures",
        "error_message": "Internal Server Error: Authentication service unavailable",
        "department": Department.BACKEND.value,
        "severity": ErrorSeverity.HIGH.value,
    },
    {
        "name": "Frontend form validation not working",
        "description": "Form validation is not triggering on the registration page",
        "error_message": "TypeError: Cannot read property 'validate' of undefined",
        "department": Department.FRONTEND.value,
        "severity": ErrorSeverity.MEDIUM.value,
    },
    {
        "name": "Database connection timeout",
        "description": "Frequent database connection timeouts during peak hours",
        "error_message": "Connection timeout after 30 seconds",
        "department": Department.DATABASE.value,
        "severity": ErrorSeverity.CRITICAL.value,
    },
    {
        "name": "SSL certificate expiring soon",
        "description": "SSL certificate for main domain expires in 7 days",
        "error_message": None,
        "department": Department.DEVOPS.value,
        "severity": ErrorSeverity.HIGH.value,
    },
    {
        "name": "API rate limiting not enforced",
        "description": "Rate limiting middleware is not working properly",
        "error_message": "Rate limit bypass detected",
        "department": Department.SECURITY.value,
        "severity": ErrorSeverity.HIGH.value,
    },
    {
        "name": "API response time degradation",
        "description": "API endpoints showing increased response times",
        "error_message": "Request timeout after 10 seconds",
        "department": Department.API.value,
        "severity": ErrorSeverity.MEDIUM.value,
    },
    {
        "name": "Mobile app crashing on startup",
        "description": "iOS app crashes immediately after opening",
        "error_message": "Fatal Exception: NSInvalidArgumentException",
        "department": Department.FRONTEND.value,
        "severity": ErrorSeverity.CRITICAL.value,
    },
    {
        "name": "Payment processing failures",
        "description": "Credit card payments failing intermittently",
        "error_message": "Payment gateway error: Invalid merchant ID",
        "department": Department.BACKEND.value,
        "severity": ErrorSeverity.CRITICAL.value,
    },
    {
        "name": "Search functionality broken",
        "description": "Search returns no results even for valid queries",
        "error_message": "Elasticsearch connection refused",
        "department": Department.DATABASE.value,
        "severity": ErrorSeverity.HIGH.value,
    },
    {
        "name": "Docker container memory leak",
        "description": "Application containers consuming excessive memory",
        "error_message": "Out of memory: Kill process",
        "department": Department.DEVOPS.value,
        "severity": ErrorSeverity.HIGH.value,
    },
]

# Possible statuses with weights (for realistic distribution)
STATUS_WEIGHTS = [
    ("open", 0.3),
    ("in_progress", 0.2),
    ("pending", 0.15),
    ("resolved", 0.25),
    ("closed", 0.1),
]

ASSIGNEES = [
    "john.doe@company.com",
    "jane.smith@company.com",
    "mike.johnson@company.com",
    "sarah.wilson@company.com",
    "alex.brown@company.com",
    None,  # Unassigned tickets
]


def weighted_choice(choices):
    """Select a choice based on weights."""
    total = sum(weight for choice, weight in choices)
    r = uniform(0, total)  # noqa: S311
    upto = 0
    for option, weight in choices:
        if upto + weight >= r:
            return option
        upto += weight
    return choices[-1][0]


async def create_sample_tickets(session, count: int = 50):
    """Create sample tickets with realistic data."""
    tickets_created = []

    for i in range(count):
        # Choose a base ticket template
        base_ticket = choice(SAMPLE_TICKETS)  # noqa: S311

        # Generate realistic timestamps
        days_ago = randint(1, 90)  # Tickets from last 90 days  # noqa: S311
        created_at = datetime.utcnow() - timedelta(days=days_ago)

        # Choose status and set resolved_at if applicable
        status = weighted_choice(STATUS_WEIGHTS)
        resolved_at = None
        if status in ["resolved", "closed"]:
            # Resolved within 0.5 to 7 days after creation
            resolution_hours = uniform(0.5, 168)  # 0.5 hours to 7 days  # noqa: S311
            resolved_at = created_at + timedelta(hours=resolution_hours)

        # Create ticket
        ticket_data = {
            "name": f"{base_ticket['name']} #{i + 1}",
            "description": base_ticket["description"],
            "error_message": base_ticket["error_message"],
            "department": base_ticket["department"],
            "severity": base_ticket["severity"],
            "status": status,
            "assignee": choice(ASSIGNEES),  # noqa: S311
            "created_at": created_at,
            "updated_at": created_at + timedelta(hours=randint(0, 24)),  # noqa: S311
            "resolved_at": resolved_at,
        }

        ticket = Ticket(**ticket_data)
        session.add(ticket)
        tickets_created.append(ticket)

        # Commit every 10 tickets to avoid memory issues
        if (i + 1) % 10 == 0:
            await session.commit()

    # Final commit
    await session.commit()

    return tickets_created


async def create_sample_classifications(session, tickets):
    """Create sample classifications for tickets."""
    sample_reasonings = [
        "Based on error message and description, this appears to be a backend service issue",
        "Frontend validation error suggests client-side JavaScript problem",
        "Database timeout indicates performance or connectivity issues",
        "Security vulnerability requires immediate attention",
        "Infrastructure issue affecting system reliability",
        "API performance degradation needs investigation",
    ]

    sample_actions = [
        ["Check server logs", "Restart service", "Monitor performance"],
        ["Review JavaScript code", "Update validation library", "Test on multiple browsers"],
        ["Analyze database performance", "Check connection pool", "Review slow queries"],
        ["Apply security patch", "Update dependencies", "Run security audit"],
        ["Scale infrastructure", "Check monitoring alerts", "Review system metrics"],
        ["Optimize API endpoints", "Check rate limiting", "Review caching strategy"],
    ]

    for ticket in tickets:
        # Create classification for 70% of tickets
        if uniform(0, 1) < 0.7:  # noqa: S311
            classification = Classification(
                ticket_id=ticket.id,
                confidence=uniform(0.7, 0.99),  # noqa: S311
                reasoning=choice(sample_reasonings),  # noqa: S311
                suggested_actions=json.dumps(choice(sample_actions)),  # noqa: S311
                created_at=ticket.created_at + timedelta(minutes=randint(1, 30)),  # noqa: S311
            )
            session.add(classification)

    await session.commit()


async def seed_database():
    """Main function to seed the database with sample data."""
    print("Initializing database...")
    await init_db()

    async with AsyncSessionLocal() as session:
        print("Creating sample tickets...")
        tickets = await create_sample_tickets(session, count=100)

        print("Creating sample classifications...")
        await create_sample_classifications(session, tickets)

        print(f"Successfully created {len(tickets)} tickets with classifications!")


if __name__ == "__main__":
    asyncio.run(seed_database())
