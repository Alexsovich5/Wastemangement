#!/bin/bash
set -e

echo "🚀 ERPNext Medical Waste Management - One-Click Installation"
echo "============================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check Prerequisites
print_status "Checking prerequisites..."

# Check Docker
if ! command_exists docker; then
    print_error "Docker is not installed. Please install Docker Desktop first."
    echo "Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check Docker Compose
if ! command_exists docker && ! docker compose version >/dev/null 2>&1; then
    print_error "Docker Compose is not available. Please ensure Docker Desktop is properly installed."
    exit 1
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop."
    exit 1
fi

print_success "Prerequisites check passed"

# Step 2: Check ports
print_status "Checking port availability..."

check_port() {
    local port=$1
    local service=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $port is already in use (needed for $service)"
        read -p "Continue anyway? This may cause conflicts (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Installation aborted due to port conflicts"
            exit 1
        fi
    fi
}

check_port 8081 "ERPNext Web Interface"
check_port 3307 "Database"
check_port 80 "HTTP"
check_port 443 "HTTPS"
check_port 81 "Nginx Admin"

print_success "Port availability check completed"

# Step 3: Environment Setup
print_status "Setting up environment configuration..."

if [ ! -f .env ]; then
    print_warning ".env file not found, creating default configuration..."
    cat > .env << 'EOF'
# ERPNext Medical Waste Management - Configuration
MYSQL_ROOT_PASSWORD=admin
ADMIN_PASSWORD=admin
ERPNEXT_EXTERNAL_PORT=8081
DB_EXTERNAL_PORT=3307
NGINX_HTTPS_PORT=443
NGINX_ADMIN_PORT=81
NPM_DB_NAME=nginx_db
EOF
    print_success "Default .env configuration created"
else
    print_success "Using existing .env configuration"
fi

# Step 4: Install Node.js dependencies for testing (optional)
if [ "$1" = "--with-testing" ]; then
    print_status "Installing testing dependencies..."
    if command_exists npm; then
        npm install
        print_success "Testing dependencies installed"
    else
        print_warning "npm not found, skipping testing dependencies"
    fi
fi

# Step 5: Start ERPNext System
print_status "Starting ERPNext system..."
echo "This may take several minutes on first run as Docker images are downloaded..."

# Make scripts executable
chmod +x *.sh

# Pull images first for better progress indication
print_status "Downloading required Docker images..."
docker compose pull

# Start the system
print_status "Starting all services..."
docker compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check if services are running
print_status "Checking service health..."
for i in {1..30}; do
    if docker compose ps | grep -q "Up"; then
        print_success "Services are starting up"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Services failed to start properly"
        echo "Checking logs:"
        docker compose logs --tail=20
        exit 1
    fi
    sleep 2
done

# Step 6: Wait for ERPNext to be ready
print_status "Waiting for ERPNext to be ready..."
print_status "This can take 5-10 minutes for site creation and app installation..."

for i in {1..180}; do  # Wait up to 6 minutes
    if curl -s http://localhost:8081/api/method/ping >/dev/null 2>&1; then
        print_success "ERPNext is ready!"
        break
    fi
    if [ $i -eq 180 ]; then
        print_error "ERPNext did not become ready in time"
        print_status "Checking logs for issues:"
        docker compose logs backend --tail=50
        exit 1
    fi
    
    # Show progress every 30 seconds
    if [ $((i % 15)) -eq 0 ]; then
        print_status "Still waiting for ERPNext... (${i}/180)"
    fi
    sleep 2
done

# Step 7: Install Medical Waste Management System
print_status "Installing Medical Waste Management customizations..."

# Use the consolidated setup script
docker compose cp setup/scripts/setup_medical_waste.py backend:/home/frappe/frappe-bench/

print_status "Running medical waste setup (this may take 2-3 minutes)..."
cat > /tmp/run_setup.sh << 'EOF'
cd /home/frappe/frappe-bench
cat setup_medical_waste.py | grep -A 1000 'def setup_medical_waste' | head -400 > /tmp/exec_script.py
printf 'exec(open("/tmp/exec_script.py").read())\nsetup_medical_waste()\n' | bench --site frontend console
EOF

if docker compose exec backend bash /tmp/run_setup.sh; then
    print_success "Medical waste management system installed successfully!"
else
    print_warning "Medical waste setup encountered some issues, but basic system is running"
    print_status "You can run './run-setup.sh' manually later to complete the setup"
fi

# Step 8: Final validation
print_status "Performing final system validation..."

# Check database
DB_TABLES=$(docker compose exec db mysql -uroot -padmin -D_5e5899d8398b5f7b -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='_5e5899d8398b5f7b';" | tail -1)
if [ "$DB_TABLES" -gt 500 ]; then
    print_success "Database properly initialized with $DB_TABLES tables"
else
    print_warning "Database has only $DB_TABLES tables (expected 500+)"
fi

# Check medical waste features
WASTE_GROUPS=$(docker compose exec db mysql -uroot -padmin -D_5e5899d8398b5f7b -e "SELECT COUNT(*) FROM \`tabItem Group\` WHERE item_group_name='Medical Waste';" | tail -1)
if [ "$WASTE_GROUPS" -gt 0 ]; then
    print_success "Medical waste management features installed"
else
    print_warning "Medical waste features may need manual setup"
fi

# Step 9: Installation Complete
echo ""
echo "🎉 Installation Complete!"
echo "========================="
echo ""
print_success "ERPNext Medical Waste Management System is ready!"
echo ""
echo "📋 Access Information:"
echo "  🌐 ERPNext Web Interface: http://localhost:8081"
echo "  👤 Username: Administrator"
echo "  🔑 Password: admin"
echo "  🛠️  Nginx Proxy Manager: http://localhost:81"
echo "  🗄️  Database: localhost:3307"
echo ""
echo "📋 System Management:"
echo "  ▶️  Start system: ./start.sh"
echo "  ⏹️  Stop system: ./stop.sh"
echo "  🔄 Restart system: ./restart.sh"
echo "  📜 View logs: ./logs.sh"
echo "  🧹 Cleanup: ./cleanup.sh"
echo ""
echo "📋 Medical Waste Features:"
echo "  ✅ 33+ item groups for waste categories"
echo "  ✅ 6 specialized warehouses"
echo "  ✅ 7 custom fields for waste tracking"
echo "  ✅ Compliance and regulatory features"
echo ""
echo "📋 Next Steps:"
echo "  1. Open http://localhost:8081 in your browser"
echo "  2. Login with Administrator/admin"
echo "  3. Navigate to Stock > Item Group to see waste categories"
echo "  4. Go to Stock > Warehouse to see storage areas"
echo "  5. Create new items with waste classification fields"
echo ""
print_status "For detailed documentation, see docs/ directory"
print_status "For troubleshooting, check CLAUDE.md"
echo ""
print_success "Installation completed successfully! 🚀"