#!/usr/bin/env python3
"""
Simple database inspector using raw SQLite
No external dependencies required
"""

import sqlite3
import os
import sys


def get_database_path():
    """Get the path to the database file."""
    # Database should be in backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
    return os.path.join(backend_dir, "ticket_assistant.db")


def check_database_file():
    """Check if database file exists."""
    db_path = get_database_path()
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"✅ Database file exists: {db_path}")
        print(f"📁 File size: {size:,} bytes")
        return True, db_path
    else:
        print(f"❌ Database file not found: {db_path}")
        print("💡 Run 'python backend/setup_database.py' first to create the database")
        return False, db_path


def connect_database(db_path):
    """Connect to SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        print("✅ Database connection successful")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None


def check_tables(conn):
    """Check if tables exist and show their structure."""
    print("\n📋 Checking database tables...")

    try:
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if not tables:
            print("❌ No tables found in database")
            return False

        print(f"📊 Found {len(tables)} tables:")

        for table in tables:
            table_name = table[0]
            print(f"\n🔹 Table: {table_name}")

            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            print(f"   Columns ({len(columns)}):")
            for col in columns:
                print(f"      • {col[1]} ({col[2]})")

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   📊 Rows: {count:,}")

        return True

    except Exception as e:
        print(f"❌ Table check failed: {e}")
        return False


def show_ticket_statistics(conn):
    """Show ticket statistics from database."""
    print("\n📊 TICKET STATISTICS")
    print("-" * 30)

    try:
        cursor = conn.cursor()

        # Total tickets
        cursor.execute("SELECT COUNT(*) FROM tickets")
        total = cursor.fetchone()[0]
        print(f"📋 Total tickets: {total:,}")

        if total == 0:
            print("📝 No tickets in database")
            return True

        # Status distribution
        cursor.execute("""
            SELECT status, COUNT(*)
            FROM tickets
            GROUP BY status
            ORDER BY COUNT(*) DESC
        """)
        status_data = cursor.fetchall()

        print("\n📈 Status Distribution:")
        for row in status_data:
            print(f"   {row[0].title():12} {row[1]:,}")

        # Department distribution
        cursor.execute("""
            SELECT department, COUNT(*)
            FROM tickets
            GROUP BY department
            ORDER BY COUNT(*) DESC
        """)
        dept_data = cursor.fetchall()

        print("\n🏢 Department Distribution:")
        for row in dept_data:
            print(f"   {row[0].title():12} {row[1]:,}")

        # Severity distribution
        cursor.execute("""
            SELECT severity, COUNT(*)
            FROM tickets
            GROUP BY severity
            ORDER BY
                CASE severity
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                END
        """)
        severity_data = cursor.fetchall()

        print("\n⚠️  Severity Distribution:")
        for row in severity_data:
            print(f"   {row[0].title():12} {row[1]:,}")

        # Recent tickets
        cursor.execute("""
            SELECT name, department, severity, status, created_at
            FROM tickets
            ORDER BY created_at DESC
            LIMIT 5
        """)
        recent = cursor.fetchall()

        print("\n🕐 Recent Tickets:")
        for row in recent:
            name = row[0][:40] + "..." if len(row[0]) > 40 else row[0]
            print(f"   • {name}")
            print(f"     [{row[1].upper()}/{row[2].upper()}] {row[3]} - {row[4][:19]}")

        return True

    except Exception as e:
        print(f"❌ Statistics query failed: {e}")
        return False


def show_classification_statistics(conn):
    """Show classification statistics."""
    print("\n🤖 CLASSIFICATION STATISTICS")
    print("-" * 30)

    try:
        cursor = conn.cursor()

        # Total classifications
        cursor.execute("SELECT COUNT(*) FROM classifications")
        total = cursor.fetchone()[0]
        print(f"🔍 Total classifications: {total:,}")

        if total == 0:
            print("📝 No classifications in database")
            return True

        # Average confidence
        cursor.execute("SELECT AVG(confidence) FROM classifications")
        avg_confidence = cursor.fetchone()[0]
        print(f"📊 Average confidence: {avg_confidence:.2f}")

        # Confidence distribution
        cursor.execute("""
            SELECT
                CASE
                    WHEN confidence >= 0.9 THEN 'High (0.9+)'
                    WHEN confidence >= 0.7 THEN 'Medium (0.7-0.9)'
                    ELSE 'Low (<0.7)'
                END as confidence_range,
                COUNT(*)
            FROM classifications
            GROUP BY confidence_range
            ORDER BY MIN(confidence) DESC
        """)
        confidence_data = cursor.fetchall()

        print("\n📈 Confidence Distribution:")
        for row in confidence_data:
            print(f"   {row[0]:15} {row[1]:,}")

        return True

    except Exception as e:
        print(f"❌ Classification statistics failed: {e}")
        return False


def run_custom_query(conn, query):
    """Run a custom SQL query."""
    print(f"\n🔍 Running query: {query}")
    print("-" * 50)

    try:
        cursor = conn.cursor()
        cursor.execute(query)

        # Get column names
        columns = (
            [description[0] for description in cursor.description]
            if cursor.description
            else []
        )

        results = cursor.fetchall()

        if not results:
            print("📝 No results returned")
            return True

        # Print header
        if columns:
            header = " | ".join(f"{col:15}" for col in columns)
            print(header)
            print("-" * len(header))

        # Print results
        for row in results:
            if isinstance(row, sqlite3.Row):
                values = [str(row[i])[:15] for i in range(len(row))]
            else:
                values = [str(val)[:15] for val in row]
            print(" | ".join(f"{val:15}" for val in values))

        print(f"\n📊 {len(results)} rows returned")
        return True

    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False


def main():
    """Main database check function."""
    print("🔍 TICKET ASSISTANT DATABASE INSPECTOR")
    print("=" * 50)

    # Check if database file exists
    exists, db_path = check_database_file()
    if not exists:
        return False

    # Connect to database
    conn = connect_database(db_path)
    if not conn:
        return False

    try:
        # Run checks
        checks = [
            ("Tables", lambda: check_tables(conn)),
            ("Ticket Statistics", lambda: show_ticket_statistics(conn)),
            ("Classification Statistics", lambda: show_classification_statistics(conn)),
        ]

        results = []
        for check_name, check_func in checks:
            print(f"\n{'=' * 50}")
            result = check_func()
            results.append((check_name, result))

        # Summary
        print(f"\n{'=' * 50}")
        print("📊 INSPECTION SUMMARY")
        print("=" * 50)

        passed = sum(1 for _, result in results if result)
        total = len(results)

        for check_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status:8} {check_name}")

        print(f"\n🎯 Overall: {passed}/{total} checks passed")

        # Interactive mode
        while True:
            print(f"\n{'=' * 50}")
            print("🔧 INTERACTIVE MODE")
            print("Commands:")
            print("  stats    - Show statistics")
            print("  query    - Run custom SQL query")
            print("  exit     - Exit")

            try:
                cmd = input("\n➤ Enter command: ").strip().lower()

                if cmd == "exit":
                    break
                elif cmd == "stats":
                    show_ticket_statistics(conn)
                    show_classification_statistics(conn)
                elif cmd == "query":
                    query = input("➤ Enter SQL query: ").strip()
                    if query:
                        run_custom_query(conn, query)
                else:
                    print("❌ Unknown command")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                break

        return passed == total

    finally:
        conn.close()
        print("\n🔒 Database connection closed")


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
