# ERPNext Medical Waste Management System

## Quick Start

1. **Start the system:**
   ```bash
   ./start.sh
   ```

2. **Setup the site (run once after first start):**
   ```bash
   ./setup-site.sh
   ```

3. **Access the system:**
   - URL: http://localhost
   - Username: Administrator
   - Password: admin123

## Management Commands

- **Start system:** `./start.sh`
- **Stop system:** `./stop.sh`
- **Restart system:** `./restart.sh`
- **View logs:** `./logs.sh`

## System Components

- **ERPNext Application:** Main business application
- **MariaDB Database:** Data storage
- **Redis:** Caching and queue management
- **Nginx:** Web server and reverse proxy

## Default Credentials

- **Admin Username:** Administrator
- **Admin Password:** admin123
- **Database User:** erpnext
- **Database Password:** erpnext123

## Customization

After initial setup, follow the configuration guide to customize ERPNext for medical waste management operations.

## Troubleshooting

1. **Port conflicts:** If port 80 is in use, edit docker-compose.yml to change nginx ports
2. **Memory issues:** Ensure Docker Desktop has at least 4GB RAM allocated
3. **Permission issues:** Make sure Docker Desktop is running with proper permissions

## Data Persistence

All data is stored in Docker volumes and will persist between restarts:
- `db_data`: Database files
- `erpnext_data`: Application files and uploads
- `redis_cache_data` & `redis_queue_data`: Cache and queue data
