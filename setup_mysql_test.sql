-- Create Database if not exists
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create User if not exists
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant All Privileges on hbnb_dev_db to hbnb_dev user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_dev user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
