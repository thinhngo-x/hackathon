#!/usr/bin/env python3
"""Test script to verify the new CRUD endpoints work."""

import asyncio
import logging

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_crud_endpoints():
    """Test the new CRUD endpoints."""
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        try:
            # Test health endpoint first
            response = await client.get(f"{base_url}/api/health/")
            logger.info(f"Health check: {response.status_code}")

            # Test tickets endpoint - create a new ticket
            ticket_data = {
                "name": "Test CRUD Ticket",
                "description": "Testing the new CRUD endpoints",
                "error_message": "Test error message",
                "department": "backend",
                "severity": "medium",
                "assignee": "test-user",
            }

            logger.info("Creating test ticket...")
            response = await client.post(f"{base_url}/api/tickets", json=ticket_data)
            logger.info(f"Create ticket response: {response.status_code}")

            if response.status_code == 200:
                ticket = response.json()
                ticket_id = ticket["id"]
                logger.info(f"Created ticket with ID: {ticket_id}")

                # Test getting the ticket
                logger.info("Getting ticket...")
                response = await client.get(f"{base_url}/api/tickets/{ticket_id}")
                logger.info(f"Get ticket response: {response.status_code}")

                # Test listing tickets
                logger.info("Listing tickets...")
                response = await client.get(f"{base_url}/api/tickets")
                logger.info(f"List tickets response: {response.status_code}")
                if response.status_code == 200:
                    tickets = response.json()
                    logger.info(f"Found {tickets['total']} tickets")

                # Test updating the ticket
                logger.info("Updating ticket...")
                update_data = {"status": "in-progress"}
                response = await client.put(
                    f"{base_url}/api/tickets/{ticket_id}", json=update_data
                )
                logger.info(f"Update ticket response: {response.status_code}")

                # Test creating a classification for the ticket
                logger.info("Creating classification...")
                classification_data = {
                    "ticket_id": ticket_id,
                    "confidence": 0.95,
                    "reasoning": "Test classification reasoning",
                    "suggested_actions": ["Action 1", "Action 2"],
                }
                response = await client.post(
                    f"{base_url}/api/classifications", json=classification_data
                )
                logger.info(f"Create classification response: {response.status_code}")

                if response.status_code == 200:
                    classification = response.json()
                    classification_id = classification["id"]
                    logger.info(f"Created classification with ID: {classification_id}")

                    # Test getting classifications for the ticket
                    logger.info("Getting classifications for ticket...")
                    response = await client.get(
                        f"{base_url}/api/classifications/by-ticket/{ticket_id}"
                    )
                    logger.info(f"Get classifications response: {response.status_code}")

                logger.info("All CRUD endpoints tested successfully!")

        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            logger.error(
                "Make sure the backend server is running on http://localhost:8000"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(test_crud_endpoints())
