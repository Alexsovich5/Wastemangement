# Deployment Guide - ERPNext Medical Waste Management

## Environment-Specific Deployment

### Development Environment

**Configuration:**
- Port: http://localhost:8090 (Nginx) or http://localhost:8081 (direct ERPNext)
- Database: localhost:3307
- Admin UI: http://localhost:8191

**Setup:**
```bash
./load-env.sh development
./start.sh
./setup-site.sh
```

**Notes:**
- Uses development credentials (admin123, medwaste123)
- Non-standard ports to avoid conflicts
- Suitable for local development and testing

### Staging Environment

**Configuration:**
- Port: http://localhost:8080
- Database: localhost:3308
- Admin UI: http://localhost:8181
- Site: staging.medwaste.local

**Setup:**
```bash
./load-env.sh staging
./start.sh
./setup-site.sh
```

**Notes:**
- Uses staging-specific credentials
- Alternative ports for parallel development
- Database name: erpnext_medwaste_staging
- Suitable for integration testing and UAT

### Production Environment

**Configuration:**
- Port: http://localhost (80) / https://localhost (443)
- Database: localhost:3306 (standard port)
- Admin UI: http://localhost:81
- Site: your-domain.com (must be configured)

**Pre-deployment Checklist:**
```bash
./load-env.sh production
./validate-production.sh
```

**Security Requirements:**
1. **Update .env.production** with strong passwords:
   - `DB_ROOT_PASSWORD` - Strong database root password
   - `DB_PASSWORD` - Strong database user password
   - `ADMIN_PASSWORD` - Strong ERPNext admin password

2. **Update site configuration:**
   - `FRAPPE_SITE_NAME` - Your actual domain name

3. **SSL/TLS Setup:**
   - Configure Let's Encrypt via Nginx Proxy Manager
   - Update DNS records for your domain

**Production Deployment:**
```bash
./load-env.sh production
# Verify all security requirements are met
./validate-production.sh
./start.sh
./setup-site.sh
```

## Port Configuration Summary

| Environment | ERPNext | Database | HTTP | HTTPS | Admin |
|-------------|---------|----------|------|-------|-------|
| Development| 8081    | 3307     | 8090 | 8453  | 8191  |
| Staging     | 8082    | 3308     | 8080 | 8443  | 8181  |
| Production  | 8000    | 3306     | 80   | 443   | 81    |

## Testing and Validation

**Configuration Testing:**
```bash
./test-config.sh           # Test all configurations
./validate-ports.sh        # Check port conflicts
./test-environment-switching.sh  # Test switching workflow
```

**Production Validation:**
```bash
./validate-production.sh   # Security and configuration check
```

**Automated Testing:**
```bash
npm install               # Install test dependencies
node test-site.js        # Full site functionality test
node quick-login-test.js # Quick login verification
```

## Environment Variables Reference

### Database Configuration
- `DB_ROOT_PASSWORD` - MariaDB root password
- `DB_NAME` - Database name
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host (usually 'db')
- `DB_PORT` - Database port (internal: 3306)

### ERPNext Configuration
- `ADMIN_PASSWORD` - ERPNext administrator password
- `FRAPPE_SITE_NAME` - Site domain name
- `INSTALL_APPS` - Apps to install (usually 'erpnext')

### Port Configuration
- `ERPNEXT_EXTERNAL_PORT` - External ERPNext port
- `DB_EXTERNAL_PORT` - External database port
- `NGINX_HTTP_PORT` - HTTP port
- `NGINX_HTTPS_PORT` - HTTPS port
- `NGINX_ADMIN_PORT` - Nginx Proxy Manager admin port

### System Configuration
- `ENVIRONMENT` - Environment name (development/staging/production)
- `TZ` - Timezone (UTC for production, local for development)

## Backup and Maintenance

### Database Backup
```bash
docker compose exec db mysqldump -u root -p${DB_ROOT_PASSWORD} ${DB_NAME} > backup.sql
```

### File Backup
```bash
docker cp erpnext-medwaste-erpnext-1:/home/frappe/frappe-bench/sites ./sites-backup
```

### Log Monitoring
```bash
./logs.sh                # ERPNext logs
docker compose logs -f   # All service logs
```

### Health Checks
```bash
docker compose ps       # Service status
curl http://localhost/health  # Health endpoint
```

## Troubleshooting

### Common Issues

1. **Port Conflicts:**
   - Use different environments for parallel deployments
   - Check port availability: `netstat -an | grep :8080`

2. **Database Connection:**
   - Verify database is healthy: `docker compose ps`
   - Check connectivity: `docker compose exec db mysqladmin ping`

3. **Site Setup Failures:**
   - Ensure all services are healthy before running setup
   - Check logs: `./logs.sh`

4. **Environment Switching:**
   - Always run `./load-env.sh <environment>` before other commands
   - Verify configuration: `./test-config.sh`

### Support Commands

```bash
# Service management
./start.sh              # Start all services
./stop.sh               # Stop all services
./restart.sh            # Restart all services

# Environment management
./load-env.sh <env>     # Switch environment
./test-config.sh        # Validate configuration
./validate-ports.sh     # Check port usage

# Testing
npm install             # Install test dependencies
node test-site.js       # Run full tests
```

## Security Notes

- **Never commit .env files** containing real credentials
- **Use strong passwords** in production (minimum 12 characters)
- **Enable HTTPS** in production environments
- **Regular backups** are essential for production systems
- **Monitor logs** for security incidents
- **Update passwords** regularly