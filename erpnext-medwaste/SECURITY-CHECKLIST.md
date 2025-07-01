# Security Checklist for Production Deployment

## ⚠️ BEFORE PRODUCTION DEPLOYMENT

### 1. Change Default Passwords
- [ ] Update `ADMIN_PASSWORD` in `.env.production`
- [ ] Update `MYSQL_ROOT_PASSWORD` in `.env.production`
- [ ] Update `DB_PASSWORD` in `.env.production`

### 2. Database Security
- [ ] Restrict database user privileges (already implemented)
- [ ] Consider using separate database users for ERPNext and NPM
- [ ] Enable MySQL/MariaDB SSL connections

### 3. Network Security
- [ ] Configure proper firewall rules
- [ ] Use HTTPS for all external connections
- [ ] Set up proper SSL certificates via nginx-proxy-manager

### 4. Environment Variables
- [ ] Never commit production `.env` files to git
- [ ] Use Docker secrets or external secret management
- [ ] Rotate passwords regularly

### 5. Container Security
- [ ] Run containers with non-root users where possible
- [ ] Keep base images updated
- [ ] Scan images for vulnerabilities

### 6. Monitoring
- [ ] Set up log monitoring
- [ ] Configure security alerts
- [ ] Monitor for failed login attempts

## Current Security Improvements Made
- ✅ Fixed unsafe environment variable loading in shell scripts
- ✅ Reduced database privileges from ALL to specific needed permissions
- ✅ Standardized password configuration across environments
- ✅ Separated ERPNext and NPM database privileges