#!/usr/bin/env python3
"""
Database health check script - Verify database connection and basic operations
"""

import asyncio
import os
import sys

# Add the backend src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../backend/src"))

from sqlalchemy import text
from ticket_assistant.database.connection import AsyncSessionLocal, engine, init_db
from ticket_assistant.database.repositories.ticket_repository import TicketRepository


async def test_database_connection():
    """Test basic database connection."""
    print("🔗 Testing database connection...")
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            if value == 1:
                print("   ✅ Database connection successful")
                return True
            else:
                print("   ❌ Unexpected result from database")
                return False
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        return False


async def test_table_existence():
    """Check if required tables exist."""
    print("📋 Checking database tables...")
    try:
        async with AsyncSessionLocal() as session:
            # Check tickets table
            result = await session.execute(
                text(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'"
                )
            )
            if result.fetchone():
                print("   ✅ tickets table exists")
            else:
                print("   ❌ tickets table missing")
                return False

            # Check classifications table
            result = await session.execute(
                text(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='classifications'"
                )
            )
            if result.fetchone():
                print("   ✅ classifications table exists")
            else:
                print("   ❌ classifications table missing")
                return False

            return True
    except Exception as e:
        print(f"   ❌ Table check failed: {e}")
        return False


async def test_repository_operations():
    """Test repository operations."""
    print("🔧 Testing repository operations...")
    try:
        async with AsyncSessionLocal() as session:
            repo = TicketRepository(session)

            # Test count operations
            total_count = await repo.get_total_count()
            open_count = await repo.get_open_tickets_count()
            resolved_count = await repo.get_resolved_tickets_count()

            print(f"   📊 Total tickets: {total_count}")
            print(f"   📊 Open tickets: {open_count}")
            print(f"   📊 Resolved tickets: {resolved_count}")

            # Test distribution queries
            dept_dist = await repo.get_department_distribution()
            severity_dist = await repo.get_severity_distribution()

            print(f"   📊 Department distribution: {dict(dept_dist)}")
            print(f"   📊 Severity distribution: {dict(severity_dist)}")

            # Test average resolution time
            avg_time = await repo.get_average_resolution_time()
            print(f"   📊 Average resolution time: {avg_time} hours")

            print("   ✅ Repository operations successful")
            return True

    except Exception as e:
        print(f"   ❌ Repository operations failed: {e}")
        return False


async def show_sample_data():
    """Show sample data from database."""
    print("📝 Sample database content...")
    try:
        async with AsyncSessionLocal() as session:
            # Get first 5 tickets
            result = await session.execute(
                text("""
                SELECT id, name, department, severity, status, created_at
                FROM tickets
                ORDER BY created_at DESC
                LIMIT 5
            """)
            )

            tickets = result.fetchall()
            if tickets:
                print("   📋 Recent tickets:")
                for ticket in tickets:
                    print(
                        f"      • {ticket[1][:40]}... [{ticket[2].upper()}/{ticket[3].upper()}] ({ticket[4]})"
                    )
            else:
                print("   📋 No tickets found in database")

            # Get classification count
            result = await session.execute(text("SELECT COUNT(*) FROM classifications"))
            classification_count = result.scalar()
            print(f"   🤖 Classifications: {classification_count} records")

            return True

    except Exception as e:
        print(f"   ❌ Sample data query failed: {e}")
        return False


async def test_database_schema():
    """Test database schema details."""
    print("🏗️  Checking database schema...")
    try:
        async with AsyncSessionLocal() as session:
            # Check tickets table schema
            result = await session.execute(text("PRAGMA table_info(tickets)"))
            tickets_columns = result.fetchall()

            expected_columns = [
                "id",
                "name",
                "description",
                "error_message",
                "department",
                "severity",
                "status",
                "assignee",
                "screenshot_url",
                "created_at",
                "updated_at",
                "resolved_at",
            ]

            actual_columns = [col[1] for col in tickets_columns]

            print(f"   📋 Tickets table columns: {len(actual_columns)}")
            for col in expected_columns:
                if col in actual_columns:
                    print(f"      ✅ {col}")
                else:
                    print(f"      ❌ {col} (missing)")

            # Check classifications table schema
            result = await session.execute(text("PRAGMA table_info(classifications)"))
            class_columns = result.fetchall()

            expected_class_columns = [
                "id",
                "ticket_id",
                "confidence",
                "reasoning",
                "suggested_actions",
                "created_at",
            ]

            actual_class_columns = [col[1] for col in class_columns]

            print(f"   🤖 Classifications table columns: {len(actual_class_columns)}")
            for col in expected_class_columns:
                if col in actual_class_columns:
                    print(f"      ✅ {col}")
                else:
                    print(f"      ❌ {col} (missing)")

            return True

    except Exception as e:
        print(f"   ❌ Schema check failed: {e}")
        return False


async def main():
    """Main database health check function."""
    print("🔍 TICKET ASSISTANT DATABASE HEALTH CHECK")
    print("=" * 50)

    # Initialize database
    try:
        await init_db()
        print("✅ Database initialization successful")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

    # Run all tests
    tests = [
        ("Database Connection", test_database_connection),
        ("Table Existence", test_table_existence),
        ("Database Schema", test_database_schema),
        ("Repository Operations", test_repository_operations),
        ("Sample Data", show_sample_data),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 HEALTH CHECK SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {test_name}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 Database is healthy and working correctly!")
        return True
    else:
        print("⚠️  Some database issues detected. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
