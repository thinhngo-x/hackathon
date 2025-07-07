#!/usr/bin/env python3
"""
Simple mock data generator using only Python standard library.
This script generates mock tickets by hitting the API endpoints.
"""

import json
import random
import time
import urllib.request
import urllib.parse
from typing import Dict

# Configuration
API_BASE_URL = "http://localhost:8000"

# Mock ticket data
TICKET_TEMPLATES = [
    {
        "name": "Authentication service down",
        "description": "Users cannot log in due to authentication service failures",
        "error_message": "Internal Server Error: Authentication service unavailable",
        "keywords": ["auth", "login", "service", "down"],
    },
    {
        "name": "Frontend validation broken",
        "description": "Form validation is not working on the registration page",
        "error_message": "TypeError: Cannot read property 'validate' of undefined",
        "keywords": ["frontend", "validation", "form", "error"],
    },
    {
        "name": "Database timeout issues",
        "description": "Database queries are timing out during peak hours",
        "error_message": "Connection timeout after 30 seconds",
        "keywords": ["database", "timeout", "performance", "peak"],
    },
    {
        "name": "API rate limiting failure",
        "description": "Rate limiting is not being enforced properly",
        "error_message": "Rate limit bypass detected",
        "keywords": ["api", "rate", "limiting", "security"],
    },
    {
        "name": "Mobile app crashes",
        "description": "iOS app crashes on startup consistently",
        "error_message": "Fatal Exception: NSInvalidArgumentException",
        "keywords": ["mobile", "ios", "crash", "startup"],
    },
]


def make_http_request(url: str, data: Dict = None, method: str = "GET") -> Dict:
    """Make HTTP request using urllib."""
    try:
        if data:
            # POST request
            json_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={"Content-Type": "application/json"},
                method=method,
            )
        else:
            # GET request
            req = urllib.request.Request(url, method=method)

        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    except Exception as e:
        print(f"HTTP request failed: {e}")
        return None


def check_api_health() -> bool:
    """Check if API is running."""
    try:
        result = make_http_request(f"{API_BASE_URL}/health")
        return result is not None
    except Exception:
        return False


def generate_mock_ticket() -> Dict:
    """Generate a random mock ticket."""
    template = random.choice(TICKET_TEMPLATES)
    ticket_number = random.randint(1, 999)

    return {
        "name": f"{template['name']} #{ticket_number}",
        "description": template["description"],
        "error_message": template["error_message"],
        "keywords": template["keywords"] + [f"issue-{ticket_number}"],
    }


def create_ticket(ticket_data: Dict) -> Dict:
    """Create a ticket using the API."""
    url = f"{API_BASE_URL}/api/combined/classify-and-create-ticket-mock"
    return make_http_request(url, ticket_data, "POST")


def get_dashboard_stats() -> Dict:
    """Get dashboard statistics."""
    url = f"{API_BASE_URL}/api/dashboard/stats"
    return make_http_request(url)


def main():
    """Main function."""
    print("🚀 Simple Mock Data Generator")
    print("=" * 40)

    # Check API health
    print("Checking API...")
    if not check_api_health():
        print("❌ API not running! Start backend first:")
        print(
            "cd backend && python -m uvicorn src.ticket_assistant.api.main:app --reload"
        )
        return

    print("✅ API is running!")

    # Get initial stats
    initial_stats = get_dashboard_stats()
    if initial_stats:
        print(f"📊 Initial tickets: {initial_stats['total_tickets']}")

    # Generate tickets
    num_tickets = 20
    print(f"\n🎲 Creating {num_tickets} mock tickets...")

    successful = 0
    failed = 0

    for i in range(num_tickets):
        ticket_data = generate_mock_ticket()
        print(f"  {i + 1:2d}. {ticket_data['name'][:40]}...")

        result = create_ticket(ticket_data)
        if result and result.get("success"):
            successful += 1
            ticket = result["ticket"]
            classification = result["classification"]
            print(
                f"      ✅ {ticket['id'][:8]} [{classification['department'].upper()}/{classification['severity'].upper()}]"
            )
        else:
            failed += 1
            print("      ❌ Failed")

        time.sleep(0.2)  # Small delay

    # Final stats
    final_stats = get_dashboard_stats()

    print("\n" + "=" * 40)
    print("📊 RESULTS")
    print("=" * 40)
    print(f"✅ Created: {successful} tickets")
    print(f"❌ Failed:  {failed} tickets")

    if final_stats:
        print("\n📈 Database totals:")
        print(f"   Total: {final_stats['total_tickets']} tickets")
        print(f"   Open:  {final_stats['open_tickets']} tickets")
        print(f"   Resolved: {final_stats['resolved_tickets']} tickets")

        print("\n🏢 Departments:")
        for dept, count in final_stats["department_distribution"].items():
            print(f"   {dept.capitalize():12} {count:3d}")

    print("\n🎉 Mock data generation complete!")
    print("🔗 Check the dashboard to see updates!")


if __name__ == "__main__":
    main()
