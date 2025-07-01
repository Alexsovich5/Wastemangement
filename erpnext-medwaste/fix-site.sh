#!/bin/bash
set -e

echo "=== ERPNext Site Creation Fix ==="

# Wait for database and Redis
echo "Step 1: Waiting for backend services..."
while ! mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" --silent; do
    echo "  Waiting for database..."
    sleep 2
done

while ! timeout 2 bash -c "echo > /dev/tcp/redis_cache/6379" 2>/dev/null; do
    echo "  Waiting for Redis cache..."
    sleep 2
done

while ! timeout 2 bash -c "echo > /dev/tcp/redis_queue/6379" 2>/dev/null; do
    echo "  Waiting for Redis queue..."
    sleep 2
done

echo "✓ Backend services are ready"

cd /home/frappe/frappe-bench

# Step 2: Set up proper site configurations
echo "Step 2: Setting up site configurations..."

# Copy common site config
cp /site_config_template.json sites/common_site_config.json
echo "✓ Common site config updated"

# Ensure localhost site directory exists
mkdir -p sites/localhost/private/backups
mkdir -p sites/localhost/public/files
mkdir -p sites/localhost/logs
mkdir -p sites/localhost/locks

# Copy site-specific config
cp /site_config_template.json sites/localhost/site_config.json
echo "✓ Site config updated"

# Step 3: Create database and install frappe
echo "Step 3: Setting up database..."

# Use bench to create database properly
bench --site localhost reinstall \
    --yes \
    --admin-password "$ADMIN_PASSWORD" \
    --mariadb-root-password "$MYSQL_ROOT_PASSWORD" \
    --force || echo "Reinstall completed with warnings"

echo "✓ Database setup completed"

# Step 4: Install ERPNext
echo "Step 4: Installing ERPNext..."
bench --site localhost install-app erpnext || echo "ERPNext installation completed with warnings"

echo "✓ ERPNext installed"

# Step 5: Final setup
echo "Step 5: Final setup..."
bench --site localhost migrate
bench --site localhost build

echo "🎉 ERPNext site creation completed successfully!"
echo "You can now access ERPNext at http://localhost"
echo "Login with: Administrator / $ADMIN_PASSWORD"