#!/bin/bash
echo "🏗️  Setting up ERPNext site for Medical Waste Management..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Wait for services to be ready
echo "⏳ Waiting for database to be ready..."
sleep 30

# Check if database is accessible
echo "🔍 Checking database connectivity..."
docker compose exec db mysqladmin ping -h localhost --silent
if [ $? -ne 0 ]; then
    echo "❌ Database is not ready. Please wait and try again."
    exit 1
fi

# Create the site
echo "🏗️ Creating ERPNext site: ${FRAPPE_SITE_NAME}"
docker compose exec erpnext bench new-site ${FRAPPE_SITE_NAME} \
    --mariadb-root-password ${DB_ROOT_PASSWORD} \
    --admin-password ${ADMIN_PASSWORD} \
    --install-app ${INSTALL_APPS}

if [ $? -eq 0 ]; then
    echo "✅ Site setup completed!"
    echo "🔐 Admin credentials:"
    echo "   Username: Administrator"
    echo "   Password: ${ADMIN_PASSWORD}"
    echo "📱 Access your system at: http://localhost"
    echo "🌐 Site name: ${FRAPPE_SITE_NAME}"
else
    echo "❌ Site setup failed. Check the logs for more details."
    exit 1
fi
