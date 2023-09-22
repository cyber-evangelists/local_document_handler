
USE file_data;

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255),
    file_url VARCHAR(255)
);

CREATE TABLE locked_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    file_name VARCHAR(255),
    file_url VARCHAR(255)
);

CREATE TABLE Logging (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Description VARCHAR(255),
    UserName VARCHAR(50),
    Machine VARCHAR(50),
    Filename VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
