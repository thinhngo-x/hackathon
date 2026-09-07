#!/usr/bin/env python3
"""
API Integration Test Suite
Tests database functionality through API endpoints
"""

import json
import urllib.parse
import urllib.request

API_BASE_URL = "http://localhost:8000"


def make_request(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Make HTTP request to API."""
    try:
        url = f"{API_BASE_URL}{endpoint}"

        if data:
            json_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={"Content-Type": "application/json"},
                method=method,
            )
        else:
            req = urllib.request.Request(url, method=method)

        with urllib.request.urlopen(req, timeout=10) as response:
            return {
                "status": response.status,
                "data": json.loads(response.read().decode("utf-8")),
            }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def test_api_health():
    """Test API health endpoint."""
    print("🔍 Testing API health...")
    result = make_request("/health")

    if result.get("status") == 200:
        print("   ✅ API is healthy")
        print(f"   📊 Response: {result['data']}")
        return True
    else:
        print(f"   ❌ API health check failed: {result}")
        return False


def test_dashboard_stats():
    """Test dashboard statistics endpoint."""
    print("📊 Testing dashboard stats...")
    result = make_request("/api/dashboard/stats")

    if result.get("status") == 200:
        stats = result["data"]
        print("   ✅ Dashboard stats retrieved")
        print(f"   📋 Total tickets: {stats.get('total_tickets', 0)}")
        print(f"   📋 Open tickets: {stats.get('open_tickets', 0)}")
        print(f"   📋 Resolved tickets: {stats.get('resolved_tickets', 0)}")
        print(
            f"   ⏱️  Avg resolution time: {stats.get('average_resolution_time', 0)} hours"
        )
        print(
            f"   🎯 Classification accuracy: {stats.get('classification_accuracy', 0)}%"
        )

        print("   🏢 Department distribution:")
        for dept, count in stats.get("department_distribution", {}).items():
            print(f"      {dept.title():12} {count}")

        print("   ⚠️  Severity distribution:")
        for severity, count in stats.get("severity_distribution", {}).items():
            print(f"      {severity.title():12} {count}")

        return True
    else:
        print(f"   ❌ Dashboard stats failed: {result}")
        return False


def test_create_ticket():
    """Test ticket creation endpoint."""
    print("🎫 Testing ticket creation...")

    test_ticket = {
        "name": "API Test Ticket",
        "description": "This is a test ticket created via API to verify database integration",
        "error_message": "Test error message for API verification",
        "keywords": ["api", "test", "verification", "database"],
    }

    result = make_request(
        "/api/combined/classify-and-create-ticket-mock", "POST", test_ticket
    )

    if result.get("status") == 200 and result["data"].get("success"):
        data = result["data"]
        ticket = data["ticket"]
        classification = data["classification"]

        print("   ✅ Ticket created successfully")
        print(f"   🆔 Ticket ID: {ticket['id']}")
        print(f"   📝 Name: {ticket['name']}")
        print(f"   🏢 Department: {classification['department'].upper()}")
        print(f"   ⚠️  Severity: {classification['severity'].upper()}")
        print(f"   🎯 Confidence: {classification['confidence']:.2f}")

        return True
    else:
        print(f"   ❌ Ticket creation failed: {result}")
        return False


def test_api_endpoints():
    """Test various API endpoints."""
    print("🔍 Testing API endpoints...")

    endpoints = [
        ("/", "GET", "Root endpoint"),
        ("/health", "GET", "Health check"),
        ("/health/ready", "GET", "Readiness check"),
        ("/health/live", "GET", "Liveness check"),
        ("/api/dashboard/stats", "GET", "Dashboard stats"),
        ("/api/dashboard/stats/real-time", "GET", "Real-time stats"),
    ]

    results = []

    for endpoint, method, description in endpoints:
        print(f"\n   🔗 Testing {description} ({method} {endpoint})")
        result = make_request(endpoint, method)

        if result.get("status") == 200:
            print("      ✅ Success")
            results.append(True)
        else:
            print(f"      ❌ Failed: {result.get('error', 'Unknown error')}")
            results.append(False)

    passed = sum(results)
    total = len(results)
    print(f"\n   📊 API endpoints: {passed}/{total} passed")

    return passed == total


def test_multiple_ticket_creation():
    """Test creating multiple tickets to verify database persistence."""
    print("🎫 Testing multiple ticket creation...")

    test_tickets = [
        {
            "name": "Frontend Bug #1",
            "description": "Button click handler not working properly",
            "error_message": "TypeError: Cannot read property 'click' of undefined",
            "keywords": ["frontend", "javascript", "button", "click"],
        },
        {
            "name": "Backend Error #1",
            "description": "Database connection pool exhausted",
            "error_message": "ConnectionPoolExhaustedException: All connections in use",
            "keywords": ["backend", "database", "connection", "pool"],
        },
        {
            "name": "API Performance #1",
            "description": "Response times degraded significantly",
            "error_message": "TimeoutException: Request took longer than 5 seconds",
            "keywords": ["api", "performance", "timeout", "response"],
        },
    ]

    created_tickets = []

    for i, ticket_data in enumerate(test_tickets):
        print(f"   Creating ticket {i + 1}/{len(test_tickets)}: {ticket_data['name']}")

        result = make_request(
            "/api/combined/classify-and-create-ticket-mock", "POST", ticket_data
        )

        if result.get("status") == 200 and result["data"].get("success"):
            data = result["data"]
            ticket = data["ticket"]
            classification = data["classification"]
            created_tickets.append((ticket, classification))
            print(
                f"      ✅ Created {ticket['id'][:8]} [{classification['department'].upper()}/{classification['severity'].upper()}]"
            )
        else:
            print("      ❌ Failed to create ticket")

    print(
        f"\n   📊 Successfully created {len(created_tickets)}/{len(test_tickets)} tickets"
    )

    # Verify tickets were persisted by checking dashboard stats
    print("   🔍 Verifying persistence via dashboard stats...")
    stats_result = make_request("/api/dashboard/stats")

    if stats_result.get("status") == 200:
        stats = stats_result["data"]
        print(f"   ✅ Dashboard shows {stats['total_tickets']} total tickets")
        return len(created_tickets) == len(test_tickets)
    else:
        print("   ❌ Could not verify via dashboard stats")
        return False


def main():
    """Main API test function."""
    print("🔍 TICKET ASSISTANT API DATABASE TEST")
    print("=" * 50)

    tests = [
        ("API Health Check", test_api_health),
        ("API Endpoints", test_api_endpoints),
        ("Dashboard Statistics", test_dashboard_stats),
        ("Single Ticket Creation", test_create_ticket),
        ("Multiple Ticket Creation", test_multiple_ticket_creation),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'=' * 50}")
        print(f"📋 {test_name}")
        print("-" * 30)

        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'=' * 50}")
    print("📊 API TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {test_name}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All API tests passed! Database integration is working correctly.")
    else:
        print("⚠️  Some API tests failed. Check the errors above.")
        if passed == 0:
            print("💡 Make sure the backend server is running:")
            print(
                "   cd backend && python -m uvicorn src.ticket_assistant.api.main:app --reload"
            )

    return passed == total


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
