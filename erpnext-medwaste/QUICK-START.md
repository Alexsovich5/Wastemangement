# Quick Start Guide

## One-Command Installation

For a fresh installation on any machine:

```bash
git clone <repository-url>
cd erpnext-medwaste
./install.sh
```

That's it! The script will:

1. ✅ Check prerequisites (Docker, ports)
2. ✅ Set up environment configuration 
3. ✅ Download and start ERPNext system
4. ✅ Wait for services to be ready
5. ✅ Install medical waste management features
6. ✅ Validate installation

## Prerequisites

- **Docker Desktop** installed and running
- **Available ports**: 8081, 3307, 80, 443, 81
- **4GB+ RAM** allocated to Docker
- **10GB+ disk space** for Docker images and data

## Installation Options

### Standard Installation
```bash
./install.sh
```

### With Testing Dependencies
```bash
./install.sh --with-testing
```

## After Installation

### Access the System
- **Web Interface**: http://localhost:8081
- **Username**: Administrator  
- **Password**: admin

### Medical Waste Features
- Navigate to **Stock > Item Group** to see waste categories
- Go to **Stock > Warehouse** for storage areas
- Create items with custom waste classification fields

### System Management
```bash
./start.sh    # Start system
./stop.sh     # Stop system  
./restart.sh  # Restart system
./logs.sh     # View logs
./cleanup.sh  # Clean temporary files
```

## Troubleshooting

### Port Conflicts
If ports are in use, either:
1. Stop conflicting services
2. Edit `.env` file to change ports
3. Continue installation (may cause issues)

### Docker Issues
```bash
docker system prune -f    # Clean Docker cache
docker compose down       # Stop all containers
docker compose up -d      # Restart system
```

### Installation Fails
```bash
./logs.sh                 # Check system logs
docker compose ps         # Check service status
```

## What Gets Installed

### ERPNext System
- Full ERPNext v15.66.1 application
- MariaDB database
- Redis caching and queues
- Nginx proxy manager
- Automated site creation

### Medical Waste Features
- **33+ Item Groups**: Complete waste category hierarchy
- **6 Warehouses**: Specialized storage areas
- **7 Custom Fields**: Waste classification, hazard levels, treatment methods
- **Compliance Tools**: Regulatory tracking and manifest generation

### Project Structure
```
erpnext-medwaste/
├── setup/scripts/     # Installation scripts
├── docs/              # Documentation  
├── temp_files/        # Development files
└── *.sh              # Management scripts
```

## Next Steps

1. **Explore the Interface**: Login and navigate the medical waste features
2. **Create Sample Data**: Add waste items using the custom fields
3. **Configure Workflows**: Set up treatment and disposal processes
4. **Read Documentation**: Check `docs/` for detailed guides
5. **Customize Further**: Modify setup scripts for specific needs

## Support

- **Documentation**: See `docs/` directory
- **Development Guide**: Check `CLAUDE.md`
- **Project Structure**: Review `PROJECT-STRUCTURE.md`
- **Issues**: Check logs with `./logs.sh`

The installation is fully automated and should work on any machine with Docker installed!