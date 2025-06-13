#!/bin/bash
echo "🔄 Restarting ERPNext Medical Waste Management System..."
docker compose down
docker compose up -d
echo "✅ System restarted successfully!"
