# ERPNext Medical Waste Management System

> Complete containerized ERPNext deployment with specialized medical waste management features

## 🚀 One-Command Installation

For fresh installations (new machines):

```bash
git clone <repository-url>
cd erpnext-medwaste
./install.sh
```

**That's it!** The script automatically:
- ✅ Checks prerequisites and ports
- ✅ Downloads and starts ERPNext system  
- ✅ Creates site and installs medical waste features
- ✅ Sets up 33+ item groups, 6 warehouses, 7 custom fields

## 📋 Quick Access

After installation:
- **Web Interface**: http://localhost:8081
- **Username**: Administrator
- **Password**: admin

## 🛠️ Manual Management (Existing Installations)

## Management Commands

- **Start system:** `./start.sh`
- **Stop system:** `./stop.sh`
- **Restart system:** `./restart.sh`
- **View logs:** `./logs.sh`

## System Components

- **ERPNext Application:** Main business application (port 8000)
- **MariaDB Database:** Data storage
- **Redis:** Caching and queue management

## Default Credentials

- **Admin Username:** Administrator
- **Admin Password:** admin123
- **Database User:** erpnext
- **Database Password:** erpnext123

## Customization

After initial setup, follow the configuration guide to customize ERPNext for medical waste management operations.

## Environment Configuration

This project supports multiple environments (development, staging, production):

1. **Switch environments:**
   ```bash
   ./load-env.sh development  # Default
   ./load-env.sh staging
   ./load-env.sh production
   ```

2. **Environment files:**
   - `.env.example` - Template for development
   - `.env.staging` - Staging configuration
   - `.env.production` - Production configuration (requires strong passwords)

## Troubleshooting

1. **Port conflicts:** Use `./load-env.sh` to switch to different port configurations
2. **Memory issues:** Ensure Docker Desktop has at least 4GB RAM allocated
3. **Permission issues:** Make sure Docker Desktop is running with proper permissions
4. **Health check failures:** Services now have proper health checks - wait for all services to be healthy
5. **Database connection:** The setup script now validates database connectivity before site creation

## Data Persistence

All data is stored in Docker volumes and will persist between restarts:
- `db_data`: Database files
- `erpnext_data`: Application files and uploads
- `redis_cache_data` & `redis_queue_data`: Cache and queue data
