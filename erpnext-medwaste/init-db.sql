-- Create databases if they don't exist
CREATE DATABASE IF NOT EXISTS erpnext_db;
CREATE DATABASE IF NOT EXISTS nginx_db;

-- Grant specific privileges to erpnext user on erpnext_db database
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX ON erpnext_db.* TO 'erpnext'@'%';
-- Grant privileges for nginx proxy manager database  
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX ON nginx_db.* TO 'erpnext'@'%';
FLUSH PRIVILEGES;