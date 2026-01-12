CREATE DATABASE IF NOT EXISTS demo;
USE demo;

CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  price INT
);

INSERT INTO products (name, price)
VALUES
('Product-1', 10),
('Product-2', 20),
('Product-3', 30),
('Product-4', 40),
('Product-5', 50);
