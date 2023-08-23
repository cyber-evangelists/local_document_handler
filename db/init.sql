CREATE DATABASE file_data;

-- Switch to the created database
USE file_data;

-- Create the 'files' table
CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255),
    url VARCHAR(255)
);