#!/usr/bin/env python3
"""
Example script demonstrating the Ticket Assistant API usage
"""

import asyncio
import httpx
import json
from typing import Dict, Any


class TicketAssistantClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    async def send_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a report to the ticket system"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/reports/mock",  # Using mock endpoint for demo
                json=report_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def classify_error(self, classification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify an error (requires Groq API key)"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/classify",
                json=classification_data,
                timeout=30.0
            )
            if response.status_code == 500:
                print("⚠️  Groq API not available - skipping classification demo")
                return {"error": "Groq API not available"}
            response.raise_for_status()
            return response.json()
    
    async def classify_and_send(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify and send a report in one operation"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/reports/classify-and-send",
                json=report_data,
                timeout=30.0
            )
            if response.status_code == 500:
                print("⚠️  Groq API not available - skipping combined demo")
                return {"error": "Groq API not available"}
            response.raise_for_status()
            return response.json()


async def main():
    """Demo the Ticket Assistant API"""
    print("🎫 Ticket Assistant API Demo")
    print("=" * 40)
    
    client = TicketAssistantClient()
    
    # Test data
    sample_reports = [
        {
            "name": "Database Connection Timeout",
            "keywords": ["database", "connection", "timeout", "postgresql"],
            "description": "Users are experiencing timeouts when trying to connect to the PostgreSQL database. The application becomes unresponsive after 30 seconds.",
            "error_message": "psycopg2.OperationalError: could not connect to server: timeout expired",
            "screenshot_url": "https://example.com/db-timeout-screenshot.png"
        },
        {
            "name": "React Component Rendering Issue",
            "keywords": ["react", "frontend", "rendering", "javascript"],
            "description": "The main dashboard component is not rendering properly for users on mobile devices. The layout appears broken.",
            "error_message": "TypeError: Cannot read property 'map' of undefined",
            "screenshot_url": "https://example.com/react-error-screenshot.png"
        },
        {
            "name": "API Integration Failure",
            "keywords": ["api", "integration", "third-party", "payment"],
            "description": "Payment processing API calls are failing intermittently, causing checkout process to fail.",
            "error_message": "requests.exceptions.ConnectionError: Connection timeout",
            "screenshot_url": "https://example.com/api-error-screenshot.png"
        }
    ]
    
    classification_examples = [
        {
            "error_description": "Docker container fails to start due to port conflict",
            "error_message": "Error response from daemon: port is already allocated",
            "context": "Deployment to staging environment"
        },
        {
            "error_description": "SQL injection attempt detected in user input",
            "error_message": "Suspicious query pattern detected: ' OR '1'='1",
            "context": "Login form submission"
        }
    ]
    
    try:
        # Demo 1: Send Reports
        print("\n📝 Demo 1: Sending Reports")
        print("-" * 30)
        
        for i, report in enumerate(sample_reports, 1):
            print(f"\n{i}. Sending report: {report['name']}")
            result = await client.send_report(report)
            print(f"   ✅ Success: {result['message']}")
            print(f"   🎫 Ticket ID: {result['ticket_id']}")
        
        # Demo 2: Error Classification
        print("\n\n🤖 Demo 2: Error Classification")
        print("-" * 35)
        
        for i, classification in enumerate(classification_examples, 1):
            print(f"\n{i}. Classifying: {classification['error_description'][:50]}...")
            result = await client.classify_error(classification)
            
            if "error" in result:
                print(f"   ⚠️  {result['error']}")
                continue
                
            print(f"   🏢 Department: {result['department']}")
            print(f"   🚨 Severity: {result['severity']}")
            print(f"   📊 Confidence: {result['confidence']:.1%}")
            print(f"   💡 Reasoning: {result['reasoning'][:100]}...")
        
        # Demo 3: Combined Operation
        print("\n\n🔄 Demo 3: Classify and Send Report")
        print("-" * 40)
        
        combined_report = sample_reports[0]  # Use first report
        print(f"Processing: {combined_report['name']}")
        
        result = await client.classify_and_send(combined_report)
        
        if "error" not in result:
            print("✅ Combined operation successful!")
            print(f"🏢 Classified as: {result['classification']['department']}")
            print(f"🚨 Severity: {result['classification']['severity']}")
            print(f"🎫 Ticket ID: {result['report_result']['ticket_id']}")
        else:
            print(f"⚠️  {result['error']}")
    
    except httpx.ConnectError:
        print("❌ Could not connect to Ticket Assistant API")
        print("   Make sure the API server is running on http://localhost:8000")
        print("   Run: ./run.sh or uv run python main.py")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
    
    print("\n" + "=" * 40)
    print("🎉 Demo completed!")
    print("\n📚 For more information:")
    print("   - API docs: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")


if __name__ == "__main__":
    asyncio.run(main())
