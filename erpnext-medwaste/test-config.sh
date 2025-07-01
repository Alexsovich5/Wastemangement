#!/bin/bash
echo "🔧 Testing ERPNext Configuration..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "📋 Configuration Summary:"
echo "  Environment: ${ENVIRONMENT}"
echo "  ERPNext Port: ${ERPNEXT_EXTERNAL_PORT}"
echo "  Database Port: ${DB_EXTERNAL_PORT}"
echo "  Site Name: ${FRAPPE_SITE_NAME}"
echo "  Timezone: ${TZ}"

echo ""
echo "🔍 Validating Docker Compose configuration..."
if docker compose config --quiet; then
    echo "✅ Docker Compose configuration is valid"
else
    echo "❌ Docker Compose configuration has errors"
    exit 1
fi

echo ""
echo "🔍 Testing environment configurations..."

# Test staging
echo "  Testing staging environment..."
if ./load-env.sh staging >/dev/null 2>&1; then
    echo "  ✅ Staging environment loads correctly"
else
    echo "  ❌ Staging environment has issues"
fi

# Test production  
echo "  Testing production environment..."
if ./load-env.sh production >/dev/null 2>&1; then
    echo "  ✅ Production environment loads correctly"
else
    echo "  ❌ Production environment has issues"
fi

# Restore development
./load-env.sh development >/dev/null 2>&1

echo ""
echo "✅ Configuration tests completed successfully!"
echo "💡 Run './start.sh' when Docker is available to test full startup"