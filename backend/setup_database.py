#!/usr/bin/env python3
"""
Setup script to initialize the database and populate it with sample data.
Run this script to set up the database for the first time.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ticket_assistant.database.seed_data import seed_database


async def main():
    """Main setup function."""
    print("🚀 Setting up Ticket Assistant Database...")
    print("=" * 50)
    
    try:
        await seed_database()
        print("=" * 50)
        print("✅ Database setup completed successfully!")
        print("📊 Your dashboard should now show real data from the database.")
        print("🔗 You can now start the backend server and view the dashboard.")
        
    except Exception as e:
        print("=" * 50)
        print(f"❌ Error setting up database: {e}")
        print("Please check your environment and try again.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
