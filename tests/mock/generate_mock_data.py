"""
Mock data generator that hits API endpoints to populate the database.
This script simulates real API usage by sending requests to the ticket creation endpoints.
"""

import asyncio
import json
import random
from datetime import datetime
from typing import List

import httpx

# Configuration
API_BASE_URL = "http://localhost:8000"
TOTAL_TICKETS = 50

# Mock ticket data templates
TICKET_TEMPLATES = [
    {
        "name": "Authentication service returning 500 errors",
        "description": "Users are unable to log in due to authentication service failures. The login endpoint is throwing internal server errors consistently.",
        "error_message": "Internal Server Error: Authentication service unavailable at /auth/login",
        "keywords": ["authentication", "login", "500", "internal server error"]
    },
    {
        "name": "Frontend form validation not working",
        "description": "Form validation is not triggering on the registration page. Users can submit forms with invalid data.",
        "error_message": "TypeError: Cannot read property 'validate' of undefined at FormValidator.js:45",
        "keywords": ["frontend", "validation", "form", "registration", "javascript"]
    },
    {
        "name": "Database connection timeout",
        "description": "Frequent database connection timeouts during peak hours. Queries are taking too long to execute.",
        "error_message": "Connection timeout after 30 seconds to database server db.example.com:5432",
        "keywords": ["database", "timeout", "connection", "performance"]
    },
    {
        "name": "SSL certificate expiring soon",
        "description": "SSL certificate for main domain expires in 7 days. Need to renew before expiration.",
        "error_message": None,
        "keywords": ["ssl", "certificate", "expiring", "security", "domain"]
    },
    {
        "name": "API rate limiting not enforced",
        "description": "Rate limiting middleware is not working properly. Some clients are bypassing the rate limits.",
        "error_message": "Rate limit bypass detected for client IP 192.168.1.100",
        "keywords": ["api", "rate limiting", "middleware", "security"]
    },
    {
        "name": "Mobile app crashing on startup",
        "description": "iOS app crashes immediately after opening. Crash occurs during initial data loading.",
        "error_message": "Fatal Exception: NSInvalidArgumentException: Invalid argument passed to NSArray",
        "keywords": ["mobile", "ios", "crash", "startup", "exception"]
    },
    {
        "name": "Payment processing failures",
        "description": "Credit card payments failing intermittently. Customers cannot complete purchases.",
        "error_message": "Payment gateway error: Invalid merchant ID or insufficient permissions",
        "keywords": ["payment", "credit card", "gateway", "merchant", "transaction"]
    },
    {
        "name": "Search functionality broken",
        "description": "Search returns no results even for valid queries. Search index might be corrupted.",
        "error_message": "Elasticsearch connection refused at search.example.com:9200",
        "keywords": ["search", "elasticsearch", "index", "query", "results"]
    },
    {
        "name": "Docker container memory leak",
        "description": "Application containers consuming excessive memory over time. Memory usage keeps increasing.",
        "error_message": "Out of memory: Kill process 1234 (node) score 500 or sacrifice child",
        "keywords": ["docker", "memory", "leak", "container", "performance"]
    },
    {
        "name": "API response time degradation",
        "description": "API endpoints showing increased response times. Average response time has doubled.",
        "error_message": "Request timeout after 10 seconds for GET /api/users",
        "keywords": ["api", "performance", "timeout", "response time", "slow"]
    },
    {
        "name": "WebSocket connection drops",
        "description": "Real-time WebSocket connections are dropping frequently. Users lose live updates.",
        "error_message": "WebSocket connection closed unexpectedly: code 1006",
        "keywords": ["websocket", "connection", "real-time", "drops", "live updates"]
    },
    {
        "name": "Email notifications not sending",
        "description": "System emails are not being sent to users. SMTP server might be down.",
        "error_message": "SMTP Error: Connection refused to mail.example.com:587",
        "keywords": ["email", "notifications", "smtp", "mail server", "delivery"]
    },
    {
        "name": "Cache invalidation issues",
        "description": "Cached data is not being invalidated properly. Users see stale information.",
        "error_message": "Redis connection timeout: TIMEOUT after 5 seconds",
        "keywords": ["cache", "redis", "invalidation", "stale data", "performance"]
    },
    {
        "name": "File upload failures",
        "description": "Users cannot upload files larger than 1MB. Upload process fails silently.",
        "error_message": "413 Payload Too Large: Request entity too large",
        "keywords": ["file upload", "payload", "size limit", "413 error"]
    },
    {
        "name": "Background job queue stuck",
        "description": "Background processing queue is not processing jobs. Tasks are accumulating.",
        "error_message": "Queue worker timeout: Job execution exceeded 300 seconds",
        "keywords": ["background jobs", "queue", "worker", "timeout", "processing"]
    }
]

# Additional error variations
ERROR_VARIATIONS = [
    "Application crashed unexpectedly",
    "Service temporarily unavailable", 
    "Network connection lost",
    "Invalid configuration detected",
    "Permission denied",
    "Resource not found",
    "Bad request format",
    "Unauthorized access attempt",
    "Service quota exceeded",
    "Invalid JSON format in request"
]

async def generate_mock_ticket():
    """Generate a single mock ticket with random variations."""
    template = random.choice(TICKET_TEMPLATES)
    
    # Add some randomization
    ticket_number = random.randint(1, 999)
    
    # Sometimes add error variations
    error_message = template["error_message"]
    if error_message is None and random.random() < 0.3:
        error_message = random.choice(ERROR_VARIATIONS)
    
    return {
        "name": f"{template['name']} #{ticket_number}",
        "description": template["description"],
        "error_message": error_message,
        "keywords": template["keywords"] + [f"issue-{ticket_number}"],
        "screenshot_url": f"https://example.com/screenshots/issue-{ticket_number}.png" if random.random() < 0.2 else None
    }

async def send_ticket_to_api(client: httpx.AsyncClient, ticket_data: dict) -> dict:
    """Send a ticket to the API endpoint."""
    try:
        # Use the combined endpoint that classifies and creates tickets
        response = await client.post(
            f"{API_BASE_URL}/api/combined/classify-and-create-ticket-mock",
            json=ticket_data,
            timeout=30.0
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error creating ticket: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Exception sending ticket: {e}")
        return None

async def check_api_health() -> bool:
    """Check if the API is running."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/health", timeout=5.0)
            return response.status_code == 200
    except:
        return False

async def get_dashboard_stats(client: httpx.AsyncClient) -> dict:
    """Get current dashboard statistics."""
    try:
        response = await client.get(f"{API_BASE_URL}/api/dashboard/stats", timeout=10.0)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return None

async def main():
    """Main function to generate mock data."""
    print("🚀 Mock Data Generator for Ticket Assistant")
    print("=" * 50)
    
    # Check if API is running
    print("Checking API health...")
    if not await check_api_health():
        print("❌ API is not running! Please start the backend server first:")
        print("   cd backend && python -m uvicorn src.ticket_assistant.api.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("✅ API is running!")
    
    # Get initial stats
    async with httpx.AsyncClient() as client:
        initial_stats = await get_dashboard_stats(client)
        if initial_stats:
            print(f"📊 Initial database state: {initial_stats['total_tickets']} tickets")
        
        print(f"\n🎲 Generating {TOTAL_TICKETS} mock tickets...")
        
        successful_tickets = []
        failed_tickets = []
        
        for i in range(TOTAL_TICKETS):
            # Generate mock ticket
            ticket_data = await generate_mock_ticket()
            
            print(f"  Creating ticket {i+1}/{TOTAL_TICKETS}: {ticket_data['name'][:50]}...")
            
            # Send to API
            result = await send_ticket_to_api(client, ticket_data)
            
            if result and result.get('success'):
                successful_tickets.append(result)
                print(f"    ✅ Created ticket {result['ticket']['id']} - {result['classification']['department'].upper()}/{result['classification']['severity'].upper()}")
            else:
                failed_tickets.append(ticket_data)
                print(f"    ❌ Failed to create ticket")
            
            # Small delay to avoid overwhelming the API
            await asyncio.sleep(0.1)
        
        # Get final stats
        print("\n📈 Fetching updated dashboard statistics...")
        final_stats = await get_dashboard_stats(client)
        
        print("\n" + "=" * 50)
        print("📊 SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully created: {len(successful_tickets)} tickets")
        print(f"❌ Failed to create: {len(failed_tickets)} tickets")
        
        if final_stats:
            print(f"\n📈 Database Statistics:")
            print(f"   Total tickets: {final_stats['total_tickets']}")
            print(f"   Open tickets: {final_stats['open_tickets']}")
            print(f"   Resolved tickets: {final_stats['resolved_tickets']}")
            print(f"   Average resolution time: {final_stats['average_resolution_time']} hours")
            print(f"   Classification accuracy: {final_stats['classification_accuracy']}%")
            
            print(f"\n🏢 Department Distribution:")
            for dept, count in final_stats['department_distribution'].items():
                print(f"   {dept.title()}: {count} tickets")
            
            print(f"\n⚠️  Severity Distribution:")
            for severity, count in final_stats['severity_distribution'].items():
                print(f"   {severity.title()}: {count} tickets")
        
        if successful_tickets:
            print(f"\n🎯 Sample created tickets:")
            for ticket in successful_tickets[:5]:  # Show first 5
                t = ticket['ticket']
                c = ticket['classification']
                print(f"   • {t['name'][:40]}... [{c['department'].upper()}/{c['severity'].upper()}]")
        
        print("\n🎉 Mock data generation complete!")
        print("🔗 You can now:")
        print("   • View the dashboard to see real statistics")
        print("   • Check the ticket list to see all created tickets")
        print("   • Submit new tickets to see real-time updates")

if __name__ == "__main__":
    asyncio.run(main())
