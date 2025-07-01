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

# Step 2: Set up common site configuration
echo "Step 2: Setting up common site configuration..."

# Copy common site config
cp /common_site_config_template.json sites/common_site_config.json
echo "✓ Common site config updated"

# Step 3: Create site and install ERPNext
echo "Step 3: Creating new site..."

# Remove any existing site first
if [ -d "sites/localhost" ]; then
    echo "Removing existing site directory..."
    rm -rf sites/localhost
fi

# Create new site WITHOUT installing apps first
bench new-site localhost \
    --mariadb-root-password "$MYSQL_ROOT_PASSWORD" \
    --admin-password "$ADMIN_PASSWORD" \
    --no-mariadb-socket

if [ $? -ne 0 ]; then
    echo "❌ Site creation failed"
    exit 1
fi

echo "✓ Site created successfully"

# Step 3.5: Apply proper site configuration
echo "Step 3.5: Applying site configuration..."
cp /site_config_template.json sites/localhost/site_config.json
echo "✓ Site configuration applied"

# Step 3.6: Install ERPNext app
echo "Step 3.6: Installing ERPNext..."
bench --site localhost install-app erpnext

if [ $? -ne 0 ]; then
    echo "❌ ERPNext installation failed"
    exit 1
fi

echo "✓ ERPNext installed successfully"

# Step 4: Database migration
echo "Step 4: Running database migration..."
bench --site localhost migrate

if [ $? -ne 0 ]; then
    echo "❌ Database migration failed"
    exit 1
fi

echo "✓ Database migration completed"

# Step 5: Build assets
echo "Step 5: Building assets..."
bench --site localhost build

if [ $? -ne 0 ]; then
    echo "❌ Asset build failed"
    exit 1
fi

echo "✓ Assets built successfully"

# Step 6: Validate database tables were created
echo "Step 6: Validating database setup..."
TABLES_COUNT=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$MYSQL_ROOT_USER" -p"$MYSQL_ROOT_PASSWORD" -D"$DB_NAME" -se "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME';")

if [ "$TABLES_COUNT" -lt 50 ]; then
    echo "❌ Database validation failed - only $TABLES_COUNT tables found (expected 50+)"
    exit 1
fi

echo "✓ Database validation passed - $TABLES_COUNT tables created"

echo "🎉 ERPNext site creation completed successfully!"
echo "You can now access ERPNext at http://localhost"
echo "Login with: Administrator / $ADMIN_PASSWORD"