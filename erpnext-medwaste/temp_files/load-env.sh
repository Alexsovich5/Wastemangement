#!/bin/bash
# Environment Configuration Loader for ERPNext Medical Waste Management

ENVIRONMENT=${1:-development}

echo "🔧 Loading ${ENVIRONMENT} environment configuration..."

case $ENVIRONMENT in
    "production")
        if [ -f .env.production ]; then
            cp .env.production .env
            echo "✅ Production environment loaded"
        else
            echo "❌ Production environment file not found"
            exit 1
        fi
        ;;
    "staging")
        if [ -f .env.staging ]; then
            cp .env.staging .env
            echo "✅ Staging environment loaded"
        else
            echo "❌ Staging environment file not found"
            exit 1
        fi
        ;;
    "development")
        if [ -f .env.example ]; then
            cp .env.example .env
            echo "✅ Development environment loaded"
        else
            echo "❌ Development environment template not found"
            exit 1
        fi
        ;;
    *)
        echo "❌ Unknown environment: $ENVIRONMENT"
        echo "Available environments: development, staging, production"
        exit 1
        ;;
esac

echo "🔍 Current configuration:"
echo "  - Environment: $ENVIRONMENT"
source .env
echo "  - ERPNext Port: ${ERPNEXT_EXTERNAL_PORT}"
echo "  - Database Port: ${DB_EXTERNAL_PORT}"
echo "  - Site Name: ${FRAPPE_SITE_NAME}"
echo ""
echo "💡 Run './start.sh' to start the system with this configuration"