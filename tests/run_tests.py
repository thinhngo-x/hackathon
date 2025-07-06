#!/usr/bin/env python3
"""
Main test runner for the Ticket Assistant system.
This script provides various testing and inspection options.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Get the project root directory
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
TESTS_DIR = SCRIPT_DIR

def run_command(cmd, description, cwd=None):
    """Run a command and return success status."""
    print(f"\n🔧 {description}")
    print(f"   Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout.strip():
                print(f"   📄 Output:\n{result.stdout}")
            return True
        else:
            print(f"   ❌ Failed (exit code: {result.returncode})")
            if result.stderr.strip():
                print(f"   🚨 Error:\n{result.stderr}")
            if result.stdout.strip():
                print(f"   📄 Output:\n{result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Command timed out")
        return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def test_database_health():
    """Test database health and connectivity."""
    print("\n🏥 DATABASE HEALTH TESTS")
    print("=" * 50)
    
    # Test with the async health checker
    health_script = TESTS_DIR / "database" / "test_health.py"
    if health_script.exists():
        success = run_command([sys.executable, str(health_script)], "Running database health check")
        if not success:
            return False
    
    # Test with the simple checker
    simple_script = TESTS_DIR / "database" / "check_database_simple.py"
    if simple_script.exists():
        success = run_command([sys.executable, str(simple_script)], "Running simple database check")
        if not success:
            return False
    
    return True

def test_api_integration():
    """Test API integration and endpoints."""
    print("\n🌐 API INTEGRATION TESTS")
    print("=" * 50)
    
    api_script = TESTS_DIR / "api" / "test_api_integration.py"
    if api_script.exists():
        return run_command([sys.executable, str(api_script)], "Running API integration tests")
    else:
        print("   ❌ API integration test script not found")
        return False

def generate_mock_data():
    """Generate mock data for testing."""
    print("\n🎭 MOCK DATA GENERATION")
    print("=" * 50)
    
    # Try the httpx-based generator first
    httpx_generator = TESTS_DIR / "mock" / "generate_mock_data.py"
    if httpx_generator.exists():
        success = run_command([sys.executable, str(httpx_generator)], "Generating mock data with httpx")
        if success:
            return True
    
    # Fall back to simple generator
    simple_generator = TESTS_DIR / "mock" / "simple_mock_generator.py"
    if simple_generator.exists():
        return run_command([sys.executable, str(simple_generator)], "Generating mock data with simple generator")
    
    print("   ❌ No mock data generators found")
    return False

def inspect_database():
    """Inspect database contents and structure."""
    print("\n🔍 DATABASE INSPECTION")
    print("=" * 50)
    
    inspector_script = TESTS_DIR / "database" / "test_inspector.py"
    if inspector_script.exists():
        return run_command([sys.executable, str(inspector_script)], "Running database inspector")
    else:
        print("   ❌ Database inspector script not found")
        return False

def run_shell_check():
    """Run the shell-based database check."""
    print("\n🐚 SHELL DATABASE CHECK")
    print("=" * 50)
    
    shell_script = TESTS_DIR / "utils" / "db-check.sh"
    if shell_script.exists():
        return run_command(["bash", str(shell_script), "all"], "Running shell database check")
    else:
        print("   ❌ Shell check script not found")
        return False

def run_backend_tests():
    """Run the backend unit and integration tests."""
    print("\n🧪 BACKEND UNIT TESTS")
    print("=" * 50)
    
    backend_tests = BACKEND_DIR / "tests"
    if backend_tests.exists():
        return run_command([sys.executable, "-m", "pytest", "tests/", "-v"], "Running backend pytest suite", cwd=BACKEND_DIR)
    else:
        print("   ❌ Backend tests directory not found")
        return False

def setup_environment():
    """Set up the testing environment."""
    print("\n⚙️  ENVIRONMENT SETUP")
    print("=" * 50)
    
    # Check if database exists, create if not
    db_file = BACKEND_DIR / "ticket_assistant.db"
    if not db_file.exists():
        setup_script = BACKEND_DIR / "setup_database.py"
        if setup_script.exists():
            success = run_command([sys.executable, str(setup_script)], "Setting up database", cwd=BACKEND_DIR)
            if not success:
                return False
        else:
            print("   ❌ Database setup script not found")
            return False
    else:
        print("   ✅ Database file already exists")
    
    return True

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Ticket Assistant Test Runner")
    parser.add_argument("--setup", action="store_true", help="Set up the testing environment")
    parser.add_argument("--health", action="store_true", help="Run database health checks")
    parser.add_argument("--api", action="store_true", help="Run API integration tests")
    parser.add_argument("--mock", action="store_true", help="Generate mock data")
    parser.add_argument("--inspect", action="store_true", help="Inspect database contents")
    parser.add_argument("--shell", action="store_true", help="Run shell-based checks")
    parser.add_argument("--backend", action="store_true", help="Run backend unit tests")
    parser.add_argument("--all", action="store_true", help="Run all tests and checks")
    parser.add_argument("--interactive", action="store_true", help="Run database inspector in interactive mode")
    
    args = parser.parse_args()
    
    print("🧪 TICKET ASSISTANT TEST RUNNER")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Backend Dir:  {BACKEND_DIR}")
    print(f"Tests Dir:    {TESTS_DIR}")
    
    success_count = 0
    total_count = 0
    
    if args.setup or args.all:
        total_count += 1
        if setup_environment():
            success_count += 1
    
    if args.health or args.all:
        total_count += 1
        if test_database_health():
            success_count += 1
    
    if args.api or args.all:
        total_count += 1
        if test_api_integration():
            success_count += 1
    
    if args.mock:
        total_count += 1
        if generate_mock_data():
            success_count += 1
    
    if args.inspect:
        total_count += 1
        if inspect_database():
            success_count += 1
    
    if args.interactive:
        inspector_script = TESTS_DIR / "database" / "test_inspector.py"
        if inspector_script.exists():
            print("\n🔧 Starting interactive database inspector...")
            subprocess.run([sys.executable, str(inspector_script), "--interactive"])
        else:
            print("   ❌ Database inspector script not found")
    
    if args.shell or args.all:
        total_count += 1
        if run_shell_check():
            success_count += 1
    
    if args.backend or args.all:
        total_count += 1
        if run_backend_tests():
            success_count += 1
    
    # If no specific arguments, show help
    if not any([args.setup, args.health, args.api, args.mock, args.inspect, 
                args.shell, args.backend, args.all, args.interactive]):
        parser.print_help()
        print("\nExample usage:")
        print("  python run_tests.py --all          # Run all tests")
        print("  python run_tests.py --setup --mock # Set up environment and generate mock data")
        print("  python run_tests.py --health --api # Check database health and test API")
        print("  python run_tests.py --interactive  # Interactive database inspector")
        return 0
    
    # Print summary
    if total_count > 0:
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print(f"   Passed: {success_count}/{total_count}")
        
        if success_count == total_count:
            print("   🎉 All tests passed!")
            return 0
        else:
            print("   ⚠️  Some tests failed!")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
