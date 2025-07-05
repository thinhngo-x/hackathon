#!/bin/bash

echo "🛑 Stopping Ticket Assistant API..."

# Find and kill processes using port 8000-8010
for port in {8000..8010}; do
    if lsof -i :$port >/dev/null 2>&1; then
        echo "🔍 Found process on port $port, stopping..."
        lsof -ti :$port | xargs kill -9 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Stopped process on port $port"
        fi
    fi
done

# Alternative: Kill all python processes with "ticket_assistant" in the command
echo "🔍 Looking for ticket-assistant processes..."
pkill -f "ticket_assistant" 2>/dev/null

echo "✅ Cleanup complete!"
echo "💡 You can now run: ./scripts/run.sh"
