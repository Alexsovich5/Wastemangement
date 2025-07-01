#!/bin/bash
echo "🚀 Starting ERPNext Medical Waste Management System..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Load environment variables securely
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Start the system
docker compose up -d

if [ $? -eq 0 ]; then
    echo "✅ System started successfully!"
    echo "📱 Access your system at: http://localhost"
    echo "🔧 Admin login will be available after initial setup"
    echo ""
    echo "💡 Use './logs.sh' to monitor logs"
    echo "💡 Use 'docker compose ps' to check service status"
else
    echo "❌ Failed to start system. Check Docker logs for details."
    exit 1
fi
