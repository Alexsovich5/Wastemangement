#!/bin/bash
echo "🏗️  Running Medical Waste Management Setup..."

# Ensure ERPNext is running
if ! docker compose ps | grep -q "Up"; then
    echo "❌ ERPNext containers are not running. Please start them first:"
    echo "   ./start.sh"
    exit 1
fi

# Wait for ERPNext to be ready
echo "⏳ Waiting for ERPNext to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8081/api/method/ping >/dev/null 2>&1; then
        echo "✅ ERPNext is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ ERPNext did not become ready in time"
        exit 1
    fi
    sleep 2
done

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "🔧 Running setup scripts..."

# Copy setup scripts to container
echo "📁 Copying setup scripts to container..."
docker compose cp setup/scripts/setup-item-categories.py backend:/home/frappe/frappe-bench/
docker compose cp setup/scripts/setup-stock-module.py backend:/home/frappe/frappe-bench/
docker compose cp setup/scripts/create-custom-doctypes.py backend:/home/frappe/frappe-bench/
docker compose cp setup/scripts/setup-manufacturing-workflows.py backend:/home/frappe/frappe-bench/
docker compose cp setup/scripts/setup-buying-module.py backend:/home/frappe/frappe-bench/
docker compose cp setup/scripts/create-compliance-reports.py backend:/home/frappe/frappe-bench/

# Run the setup scripts in sequence
echo "📦 Step 1/6: Setting up item categories..."
docker compose exec backend bench --site frontend execute setup-item-categories.main

echo "📊 Step 2/6: Configuring stock module..."
docker compose exec backend bench --site frontend execute setup-stock-module.main

echo "📋 Step 3/6: Creating custom doctypes..."
docker compose exec backend bench --site frontend execute create-custom-doctypes.main

echo "🔄 Migrating database after custom doctypes..."
docker compose exec backend bench --site frontend migrate

echo "🏭 Step 4/6: Setting up manufacturing workflows..."
docker compose exec backend bench --site frontend execute setup-manufacturing-workflows.main

echo "🛒 Step 5/6: Configuring buying module..."
docker compose exec backend bench --site frontend execute setup-buying-module.main

echo "📊 Step 6/6: Creating compliance reports..."
docker compose exec backend bench --site frontend execute create-compliance-reports.main

echo "🔄 Final database migration..."
docker compose exec backend bench --site frontend migrate

echo "✅ Medical waste management setup completed!"
echo ""
echo "🌐 Access your system at: http://localhost:8081"
echo "🔐 Login credentials:"
echo "   Username: Administrator"
echo "   Password: ${ADMIN_PASSWORD}"
echo ""
echo "📋 Next steps:"
echo "   1. Log into ERPNext"
echo "   2. Navigate to Stock > Item to see waste categories"
echo "   3. Check Stock > Warehouse for waste storage areas"
echo "   4. Review the medical waste items created"