#!/bin/bash
echo "🧪 Testing setup script validation logic..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "🔍 Environment variables loaded:"
echo "  Site name: ${FRAPPE_SITE_NAME}"
echo "  Admin password: ${ADMIN_PASSWORD}"
echo "  Database root password: ${DB_ROOT_PASSWORD}"
echo "  Apps to install: ${INSTALL_APPS}"

echo ""
echo "🔍 Testing setup script components..."

# Test environment variable export
if [ -n "${FRAPPE_SITE_NAME}" ] && [ -n "${ADMIN_PASSWORD}" ] && [ -n "${DB_ROOT_PASSWORD}" ]; then
    echo "✅ All required environment variables are set"
else
    echo "❌ Missing required environment variables"
    exit 1
fi

# Test bench command structure (dry run)
echo "🔍 Setup command that would be executed:"
echo "docker compose exec erpnext bench new-site ${FRAPPE_SITE_NAME} \\"
echo "    --mariadb-root-password ${DB_ROOT_PASSWORD} \\"
echo "    --admin-password ${ADMIN_PASSWORD} \\"
echo "    --install-app ${INSTALL_APPS}"

echo ""
echo "✅ Setup script validation completed successfully!"
echo "💡 Actual setup requires running services: './start.sh' then './setup-site.sh'"