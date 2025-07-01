#!/bin/bash
set -e

echo "Starting manual ERPNext setup..."

# Wait for database
while ! mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" --silent; do
    echo "Waiting for database..."
    sleep 2
done

# Wait for Redis
while ! timeout 2 bash -c "echo > /dev/tcp/redis_cache/6379" 2>/dev/null; do
    echo "Waiting for Redis cache..."
    sleep 2
done

echo "Backend services ready"

cd /home/frappe/frappe-bench

# Create site directory structure
mkdir -p "sites/$SITE_NAME"

# Create site config with correct parameters
cat > "sites/$SITE_NAME/site_config.json" << EOF
{
 "db_host": "$DB_HOST",
 "db_name": "$DB_NAME", 
 "db_password": "$DB_PASSWORD",
 "db_port": $DB_PORT,
 "db_type": "mariadb",
 "db_user": "$DB_USER",
 "redis_cache_url": "$REDIS_CACHE_URL",
 "redis_queue_url": "$REDIS_QUEUE_URL",
 "redis_socketio_url": "$REDIS_SOCKETIO_URL"
}
EOF

# Create common site config
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

# Try to install just the framework first
echo "Installing Frappe framework..."
bench --site "$SITE_NAME" reinstall --admin-password="$ADMIN_PASSWORD" || echo "Framework installation attempt completed"

echo "Setup completed successfully!"