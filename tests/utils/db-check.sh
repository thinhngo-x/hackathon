#!/bin/bash

# Database Health Check Script for Ticket Assistant
# This script provides various commands to check database health

echo "🔍 TICKET ASSISTANT DATABASE CHECKER"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "success" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "error" ]; then
        echo -e "${RED}❌ $message${NC}"
    elif [ "$status" = "warning" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    elif [ "$status" = "info" ]; then
        echo -e "${BLUE}ℹ️  $message${NC}"
    else
        echo "$message"
    fi
}

# Check if we can find the backend directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

if [ ! -d "$BACKEND_DIR" ]; then
    print_status "error" "Backend directory not found at $BACKEND_DIR"
    print_status "info" "Please ensure you're running from the correct location"
    exit 1
fi

cd "$BACKEND_DIR"

# Function to check database file
check_database_file() {
    echo
    print_status "info" "Checking database file..."

    if [ -f "ticket_assistant.db" ]; then
        size=$(ls -lh ticket_assistant.db | awk '{print $5}')
        print_status "success" "Database file exists (Size: $size)"
        return 0
    else
        print_status "error" "Database file not found"
        print_status "warning" "Run 'python setup_database.py' to create the database"
        return 1
    fi
}

# Function to check Python environment
check_python_env() {
    echo
    print_status "info" "Checking Python environment..."

    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        print_status "success" "Python available: $python_version"
    else
        print_status "error" "Python3 not found"
        return 1
    fi

    # Check if required packages are available
    if python3 -c "import sqlite3" 2>/dev/null; then
        print_status "success" "SQLite3 module available"
    else
        print_status "error" "SQLite3 module not available"
        return 1
    fi
}

# Function to run database health check
run_health_check() {
    echo
    print_status "info" "Running comprehensive database health check..."

    if [ -f "check_database_simple.py" ]; then
        python3 check_database_simple.py
    else
        print_status "error" "check_database_simple.py not found"
        return 1
    fi
}

# Function to check API health
check_api_health() {
    echo
    print_status "info" "Checking API health..."

    if command -v curl &> /dev/null; then
        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null)
        if [ "$response" = "200" ]; then
            print_status "success" "API is responding (HTTP 200)"
        else
            print_status "warning" "API not responding (HTTP $response or connection failed)"
            print_status "info" "Start the backend with: python -m uvicorn src.ticket_assistant.api.main:app --reload"
        fi
    else
        print_status "warning" "curl not available, cannot check API health"
    fi
}

# Function to show quick database stats
quick_stats() {
    echo
    print_status "info" "Quick database statistics..."

    if [ -f "ticket_assistant.db" ]; then
        echo "📊 Database Statistics:"

        # Count tickets
        ticket_count=$(sqlite3 ticket_assistant.db "SELECT COUNT(*) FROM tickets;" 2>/dev/null || echo "0")
        echo "   Total tickets: $ticket_count"

        # Count classifications
        class_count=$(sqlite3 ticket_assistant.db "SELECT COUNT(*) FROM classifications;" 2>/dev/null || echo "0")
        echo "   Total classifications: $class_count"

        # Show departments
        echo "   Departments:"
        sqlite3 ticket_assistant.db "SELECT department, COUNT(*) FROM tickets GROUP BY department;" 2>/dev/null | while read line; do
            echo "      $line"
        done

        # Show status distribution
        echo "   Status distribution:"
        sqlite3 ticket_assistant.db "SELECT status, COUNT(*) FROM tickets GROUP BY status;" 2>/dev/null | while read line; do
            echo "      $line"
        done
    else
        print_status "error" "Database file not found"
    fi
}

# Function to create test data
create_test_data() {
    echo
    print_status "info" "Creating test data..."

    if [ -f "simple_mock_generator.py" ]; then
        python3 simple_mock_generator.py
    else
        print_status "error" "simple_mock_generator.py not found"
        return 1
    fi
}

# Function to setup database
setup_database() {
    echo
    print_status "info" "Setting up database..."

    if [ -f "setup_database.py" ]; then
        python3 setup_database.py
    else
        print_status "error" "setup_database.py not found"
        return 1
    fi
}

# Function to show help
show_help() {
    echo
    echo "🔧 Available Commands:"
    echo "===================="
    echo "  check       - Run comprehensive database health check"
    echo "  stats       - Show quick database statistics"
    echo "  setup       - Setup/initialize database with sample data"
    echo "  test-data   - Create additional test data"
    echo "  api         - Check API health"
    echo "  all         - Run all checks"
    echo "  help        - Show this help message"
    echo
    echo "📝 Examples:"
    echo "  ./db-check.sh check     # Run full health check"
    echo "  ./db-check.sh stats     # Quick stats only"
    echo "  ./db-check.sh setup     # Initialize database"
    echo "  ./db-check.sh all       # Run everything"
}

# Main script logic
case "${1:-help}" in
    "check")
        check_python_env && check_database_file && run_health_check
        ;;
    "stats")
        check_database_file && quick_stats
        ;;
    "setup")
        check_python_env && setup_database
        ;;
    "test-data")
        check_python_env && check_database_file && create_test_data
        ;;
    "api")
        check_api_health
        ;;
    "all")
        echo "🚀 Running all checks..."
        check_python_env
        check_database_file
        check_api_health
        quick_stats
        run_health_check
        ;;
    "help"|*)
        show_help
        ;;
esac

echo
print_status "info" "Database check complete!"
