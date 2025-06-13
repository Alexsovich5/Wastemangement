#!/bin/bash
echo "🏗️  Setting up ERPNext site for Medical Waste Management..."

# Wait for services to be ready
echo "⏳ Waiting for database to be ready..."
sleep 30

# Create the site
docker compose exec erpnext bench new-site medwaste.local \
    --mariadb-root-password medwaste123 \
    --admin-password admin123 \
    --install-app erpnext

echo "✅ Site setup completed!"
echo "🔐 Admin credentials:"
echo "   Username: Administrator"
echo "   Password: admin123"
echo "📱 Access your system at: http://localhost"
