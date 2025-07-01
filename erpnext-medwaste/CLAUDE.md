# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a containerized ERPNext deployment specifically configured for medical waste management operations. It uses Docker Compose to orchestrate multiple services including ERPNext application, MariaDB database, Redis caching, and Nginx proxy management.

## Common Commands

### System Management
- **Start system**: `./start.sh` (runs `docker compose up -d`)
- **Stop system**: `./stop.sh` (runs `docker compose down`)
- **Restart system**: `./restart.sh` (stop + start)
- **View logs**: `./logs.sh` (follows all container logs)
- **Initial setup**: `./setup-site.sh` (run once after first start)

### Testing & Configuration
- **Test configuration**: `./temp_files/test-config.sh` (validates all environments)
- **Test setup logic**: `./temp_files/test-setup.sh` (validates setup script)
- **Install test dependencies**: `npm install`
- **Run automated tests**: `node temp_files/test-site.js` (requires running services)
- **Login test**: `node temp_files/quick-login-test.js`
- **Styling test**: `node temp_files/test-styling.js`

### Docker Operations
- **View running containers**: `docker compose ps`
- **Access ERPNext container**: `docker compose exec erpnext bash`
- **Database access**: `docker compose exec db mysql -u erpnext -perpnext123 erpnext_db`
- **View specific service logs**: `docker compose logs -f [service_name]`

## Architecture

### Services (docker-compose.yml)
- **db**: MariaDB 10.3 database (port 3307 external)
- **redis_cache**: Redis cache service
- **redis_queue**: Redis queue service  
- **erpnext**: Main ERPNext application (port 8081→8000)
- **worker**: Background job processor
- **scheduler**: Cron job scheduler
- **nginx-proxy-manager**: Reverse proxy with web UI (ports 80, 443, 81)

### Access Points
- **ERPNext Application**: http://localhost:8000 (direct) or http://localhost (via proxy)
- **Proxy Manager UI**: http://localhost:81
- **Database**: localhost:3307

### Default Credentials  
- **ERPNext Admin**: Administrator / admin123
- **Database**: erpnext / erpnext123
- **DB Root**: root / medwaste123

## Data Persistence

All data persists in Docker volumes:
- `db_data`: Database files
- `erpnext_data`: Application files and uploads  
- `erpnext_logs`: Application logs
- `redis_cache_data` & `redis_queue_data`: Cache and queue data
- `npm_data` & `npm_letsencrypt`: Nginx proxy configuration

## Development Workflow

1. **First-time setup**:
   ```bash
   ./start.sh
   ./setup-site.sh  # Wait for services to be ready
   ```

2. **Testing setup**:
   ```bash
   npm install  # Install Puppeteer for automated testing
   ```

3. **Daily development**:
   ```bash
   ./start.sh      # Start all services
   ./logs.sh       # Monitor logs in separate terminal
   # ... make changes ...
   ./restart.sh    # Restart if needed
   ```

## Testing Infrastructure

The project includes automated testing with Puppeteer:
- **test-site.js**: Comprehensive site functionality testing
- **quick-login-test.js**: Fast login validation
- **test-styling.js**: UI/styling verification

Tests generate screenshots for visual validation and run in non-headless mode by default for debugging.

## Medical Waste Management Features

### Setup Commands
- **Complete medical waste setup**: `./run-setup.sh` (run after site creation)
- **Manual setup steps**: See `MEDICAL-WASTE-SETUP-GUIDE.md`

### Key Modules Configured
- **Stock Management**: Waste tracking from generation to disposal
- **Manufacturing**: Treatment workflows (autoclave, incineration, etc.)
- **Buying**: Vendor management for disposal companies
- **Compliance**: Custom doctypes for regulatory requirements

### Custom DocTypes Created
- **Medical Waste Manifest**: DOT compliance tracking
- **Waste Container Tracking**: Real-time monitoring
- **Compliance Inspection**: Regulatory audits
- **Training Record**: Employee certifications
- **Incident Report**: Safety documentation

### Sample Data Included
- Medical waste item categories (Infectious, Sharps, Pharmaceutical, etc.)
- Treatment workstations and processes
- Sample disposal vendors
- Compliance reporting templates

## Important Notes

- **Port 8000**: Direct ERPNext access (bypasses proxy)
- **Port 8081**: Internal Docker port mapped to 8000
- **Memory requirement**: Minimum 4GB RAM allocated to Docker
- **Site name**: medwaste.local (configured in setup)
- **Network**: All services communicate via `erpnext-network` bridge
- **Medical waste setup**: Run `./run-setup.sh` after initial site creation

## Project Organization

### Directory Structure
- **setup/scripts/**: Medical waste setup Python scripts
- **setup/templates/**: Configuration templates  
- **docs/**: Documentation and screenshots
- **temp_files/**: Development and testing files
- **Root level**: Core operational scripts and configuration

### Cleanup and Maintenance
- **Clean up project**: `./cleanup.sh` (removes temporary files)
- **Deep cleanup**: `./cleanup.sh --deep` (also removes node_modules)
- **Project structure**: See `PROJECT-STRUCTURE.md` for detailed organization

## Troubleshooting

- **Port conflicts**: Edit docker-compose.yml port mappings
- **Database connection issues**: Check service health with `docker compose ps`
- **Permission issues**: Ensure Docker Desktop has proper permissions
- **Performance issues**: Monitor resource usage with `docker stats`
- **Medical waste setup issues**: Check logs with `./logs.sh` during setup