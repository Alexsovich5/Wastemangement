#!/bin/bash
echo "🔒 Validating Production Environment Configuration..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "🔍 Checking production security requirements..."

# Check for placeholder passwords
SECURITY_ISSUES=0

if [[ "${DB_ROOT_PASSWORD}" == "CHANGE_THIS_STRONG_ROOT_PASSWORD" ]]; then
    echo "❌ Database root password is still using placeholder"
    SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
fi

if [[ "${DB_PASSWORD}" == "CHANGE_THIS_STRONG_DB_PASSWORD" ]]; then
    echo "❌ Database password is still using placeholder"
    SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
fi

if [[ "${ADMIN_PASSWORD}" == "CHANGE_THIS_STRONG_ADMIN_PASSWORD" ]]; then
    echo "❌ Admin password is still using placeholder"
    SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
fi

if [[ "${FRAPPE_SITE_NAME}" == "your-domain.com" ]]; then
    echo "⚠️  Site name is still using placeholder (your-domain.com)"
fi

# Check password strength (basic checks)
if [ ${#DB_ROOT_PASSWORD} -lt 12 ] && [[ "${DB_ROOT_PASSWORD}" != "CHANGE_THIS_STRONG_ROOT_PASSWORD" ]]; then
    echo "⚠️  Database root password should be at least 12 characters"
fi

if [ ${#ADMIN_PASSWORD} -lt 12 ] && [[ "${ADMIN_PASSWORD}" != "CHANGE_THIS_STRONG_ADMIN_PASSWORD" ]]; then
    echo "⚠️  Admin password should be at least 12 characters"
fi

# Check port configuration
echo "🔍 Production port configuration:"
echo "  - HTTP: ${NGINX_HTTP_PORT}"
echo "  - HTTPS: ${NGINX_HTTPS_PORT}"
echo "  - ERPNext: ${ERPNEXT_EXTERNAL_PORT}"
echo "  - Database: ${DB_EXTERNAL_PORT}"

if [ "${NGINX_HTTP_PORT}" != "80" ] || [ "${NGINX_HTTPS_PORT}" != "443" ]; then
    echo "⚠️  Production should typically use standard ports (80/443)"
fi

# Check environment
echo "🔍 Environment settings:"
echo "  - Environment: ${ENVIRONMENT}"
echo "  - Timezone: ${TZ}"
echo "  - Database timeouts: ${DB_TIMEOUT}s"

if [ "${TZ}" != "UTC" ]; then
    echo "⚠️  Production should typically use UTC timezone"
fi

echo ""
if [ $SECURITY_ISSUES -gt 0 ]; then
    echo "❌ Production environment has ${SECURITY_ISSUES} security issues that must be resolved"
    echo "💡 Update .env.production with strong passwords before deployment"
    exit 1
else
    echo "✅ Production environment configuration structure is valid"
    echo "💡 Remember to update placeholder values before actual deployment"
fi