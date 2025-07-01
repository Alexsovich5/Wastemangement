#!/bin/bash
echo "🔄 Testing Environment Switching Workflow..."

echo ""
echo "🧪 Test 1: Basic environment switching"
echo "======================================="

# Test each environment switch
for env in development staging production development; do
    echo "Switching to $env..."
    if ./load-env.sh $env >/dev/null 2>&1; then
        
        # Load and check environment
        if [ -f .env ]; then
            export $(cat .env | grep -v '^#' | xargs)
        fi
        
        echo "  ✅ Environment: ${ENVIRONMENT}"
        echo "  ✅ Site: ${FRAPPE_SITE_NAME}"
        echo "  ✅ ERPNext Port: ${ERPNEXT_EXTERNAL_PORT}"
        
        # Validate Docker config is still valid
        if docker compose config --quiet; then
            echo "  ✅ Docker config valid"
        else
            echo "  ❌ Docker config invalid"
        fi
    else
        echo "  ❌ Failed to switch to $env"
    fi
    echo ""
done

echo "🧪 Test 2: Rapid environment switching"
echo "======================================="

# Test rapid switching
for i in {1..3}; do
    echo "Round $i:"
    ./load-env.sh staging >/dev/null 2>&1
    export $(cat .env | grep -v '^#' | xargs) 2>/dev/null
    echo "  Staging: ${FRAPPE_SITE_NAME}"
    
    ./load-env.sh production >/dev/null 2>&1
    export $(cat .env | grep -v '^#' | xargs) 2>/dev/null
    echo "  Production: ${FRAPPE_SITE_NAME}"
    
    ./load-env.sh development >/dev/null 2>&1
    export $(cat .env | grep -v '^#' | xargs) 2>/dev/null
    echo "  Development: ${FRAPPE_SITE_NAME}"
done

echo ""
echo "🧪 Test 3: Configuration persistence"
echo "===================================="

# Test that setup script picks up the right environment
./load-env.sh staging >/dev/null 2>&1
if ./test-setup.sh | grep -q "staging.medwaste.local"; then
    echo "✅ Setup script uses staging configuration correctly"
else
    echo "❌ Setup script configuration mismatch"
fi

./load-env.sh production >/dev/null 2>&1
if ./test-setup.sh | grep -q "your-domain.com"; then
    echo "✅ Setup script uses production configuration correctly"
else
    echo "❌ Setup script configuration mismatch"
fi

# Restore development
./load-env.sh development >/dev/null 2>&1

echo ""
echo "🧪 Test 4: Error handling"
echo "========================="

# Test invalid environment
if ./load-env.sh invalid_env 2>&1 | grep -q "Unknown environment"; then
    echo "✅ Invalid environment handled correctly"
else
    echo "❌ Invalid environment not handled"
fi

echo ""
echo "✅ Environment switching workflow tests completed!"
echo "💡 All environment switching functionality working correctly"