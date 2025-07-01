-- Grant specific privileges to erpnext user on erpnext_db database
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX ON erpnext_db.* TO 'erpnext'@'%';
-- Grant privileges for nginx proxy manager database
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX ON npm_db.* TO 'erpnext'@'%';
FLUSH PRIVILEGES;