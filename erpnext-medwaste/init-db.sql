-- Grant all privileges to erpnext user on npm_db database
GRANT ALL PRIVILEGES ON npm_db.* TO 'erpnext'@'%';
FLUSH PRIVILEGES;