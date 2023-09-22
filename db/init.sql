
USE file_data;


CREATE TABLE locked_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    file_name VARCHAR(255),
    file_url VARCHAR(255)
);

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255),
    file_url VARCHAR(255)
);
