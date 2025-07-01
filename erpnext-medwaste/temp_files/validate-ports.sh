#!/bin/bash
echo "🔌 Validating Port Configurations Across Environments..."

echo ""
echo "📋 Port Configuration Summary:"
echo "=================================================="

# Test each environment
for env in development staging production; do
    echo ""
    echo "🔧 $(echo $env | tr '[:lower:]' '[:upper:]') Environment:"
    ./load-env.sh $env >/dev/null 2>&1
    
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    echo "  ERPNext:        localhost:${ERPNEXT_EXTERNAL_PORT}"
    echo "  Database:       localhost:${DB_EXTERNAL_PORT}"
    echo "  Nginx HTTP:     localhost:${NGINX_HTTP_PORT}"
    echo "  Nginx HTTPS:    localhost:${NGINX_HTTPS_PORT}"
    echo "  Nginx Admin:    localhost:${NGINX_ADMIN_PORT}"
    
    # Check for port conflicts
    if [ "$env" = "development" ]; then
        DEV_PORTS="${ERPNEXT_EXTERNAL_PORT} ${DB_EXTERNAL_PORT} ${NGINX_HTTP_PORT} ${NGINX_HTTPS_PORT} ${NGINX_ADMIN_PORT}"
    elif [ "$env" = "staging" ]; then
        STAGING_PORTS="${ERPNEXT_EXTERNAL_PORT} ${DB_EXTERNAL_PORT} ${NGINX_HTTP_PORT} ${NGINX_HTTPS_PORT} ${NGINX_ADMIN_PORT}"
    else
        PROD_PORTS="${ERPNEXT_EXTERNAL_PORT} ${DB_EXTERNAL_PORT} ${NGINX_HTTP_PORT} ${NGINX_HTTPS_PORT} ${NGINX_ADMIN_PORT}"
    fi
done

echo ""
echo "🔍 Port Conflict Analysis:"
echo "=================================================="

# Check for conflicts between environments
CONFLICTS=0

# Compare dev vs staging
for dev_port in $DEV_PORTS; do
    for staging_port in $STAGING_PORTS; do
        if [ "$dev_port" = "$staging_port" ]; then
            echo "⚠️  Port conflict: $dev_port (development & staging)"
            CONFLICTS=$((CONFLICTS + 1))
        fi
    done
done

# Compare dev vs production
for dev_port in $DEV_PORTS; do
    for prod_port in $PROD_PORTS; do
        if [ "$dev_port" = "$prod_port" ]; then
            echo "⚠️  Port conflict: $dev_port (development & production)"
            CONFLICTS=$((CONFLICTS + 1))
        fi
    done
done

# Compare staging vs production  
for staging_port in $STAGING_PORTS; do
    for prod_port in $PROD_PORTS; do
        if [ "$staging_port" = "$prod_port" ]; then
            echo "⚠️  Port conflict: $staging_port (staging & production)"
            CONFLICTS=$((CONFLICTS + 1))
        fi
    done
done

if [ $CONFLICTS -eq 0 ]; then
    echo "✅ No port conflicts detected between environments"
else
    echo "❌ Found $CONFLICTS port conflicts"
fi

echo ""
echo "💡 Port Usage Recommendations:"
echo "=================================================="
echo "✅ Development: Uses non-standard ports (8081, 3307, etc.)"
echo "✅ Staging: Uses alternative ports (8082, 3308, 8080, etc.)"
echo "✅ Production: Uses standard ports (80, 443, 3306, etc.)"
echo ""
echo "🌐 URL Access Patterns:"
echo "  Development: http://localhost:8081 (direct) or http://localhost (via proxy)"
echo "  Staging:     http://localhost:8080"
echo "  Production:  http://localhost or https://localhost"

# Restore development environment
./load-env.sh development >/dev/null 2>&1