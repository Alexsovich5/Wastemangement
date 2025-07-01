#!/bin/bash
set -e

echo "Starting ERPNext initialization..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" --silent; do
    echo "Waiting for database..."
    sleep 2
done

echo "Database is ready"

# Wait for Redis to be ready using network connectivity
echo "Waiting for Redis to be ready..."
while ! timeout 2 bash -c "echo > /dev/tcp/redis_cache/6379" 2>/dev/null; do
    echo "Waiting for Redis cache..."
    sleep 2
done

while ! timeout 2 bash -c "echo > /dev/tcp/redis_queue/6379" 2>/dev/null; do
    echo "Waiting for Redis queue..."
    sleep 2
done

echo "Redis is ready"

# Change to frappe-bench directory
cd /home/frappe/frappe-bench

# Clean up any existing corrupted site
if [ -d "sites/$SITE_NAME" ]; then
    echo "Removing existing site to recreate from scratch..."
    rm -rf "sites/$SITE_NAME"
fi

# Always create new site
echo "Creating new site: $SITE_NAME"

# Create the site with proper credentials
bench new-site "$SITE_NAME" \
    --admin-password "$ADMIN_PASSWORD" \
    --db-root-password "$MYSQL_ROOT_PASSWORD" \
    --db-name "$DB_NAME" \
    --db-password "$DB_PASSWORD" \
    --db-user "$DB_USER" \
    --db-host "$DB_HOST" \
    --db-port "$DB_PORT" \
    --mariadb-user-host-login-scope='%' \
    --force

echo "Site created successfully"

# Update common site configuration
cat > "sites/common_site_config.json" << EOF
{
 "db_host": "$DB_HOST",
 "db_port": $DB_PORT,
 "default_site": "$SITE_NAME",
 "redis_cache_url": "$REDIS_CACHE_URL",
 "redis_queue_url": "$REDIS_QUEUE_URL",
 "redis_socketio_url": "$REDIS_SOCKETIO_URL"
}
EOF

echo "Updated common site configuration"

# Install ERPNext app if not already installed
if ! bench --site "$SITE_NAME" list-apps | grep -q "erpnext"; then
    echo "Installing ERPNext app..."
    bench --site "$SITE_NAME" install-app erpnext
    echo "ERPNext app installed"
else
    echo "ERPNext app already installed"
fi

# Migrate the site
echo "Running database migrations..."
bench --site "$SITE_NAME" migrate

echo "ERPNext initialization completed successfully!"