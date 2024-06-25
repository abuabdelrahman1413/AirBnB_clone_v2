-- Setup MySQL server for project
-- Create Database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create User
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant All Privileges for hbnb_dev user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* to 'hbnb_dev'@'localhost';
-- Grant select privileges for hbnb_dev on performance_schema
GRANT SELECT PRIVILEGES ON performance_schema TO 'hbnb_dev'@'localhost';
