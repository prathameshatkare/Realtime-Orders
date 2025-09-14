
CREATE DATABASE IF NOT EXISTS realtime_demo;
USE realtime_demo;

CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_name VARCHAR(255) NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  status ENUM('pending','shipped','delivered') NOT NULL DEFAULT 'pending',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_events (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  op VARCHAR(10) NOT NULL,        
  row_data JSON NULL,             
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  processed TINYINT(1) DEFAULT 0  
);


DELIMITER $$
CREATE TRIGGER orders_after_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  INSERT INTO order_events (op, row_data) VALUES ('INSERT', JSON_OBJECT(
    'id', NEW.id,
    'customer_name', NEW.customer_name,
    'product_name', NEW.product_name,
    'status', NEW.status,
    'updated_at', DATE_FORMAT(NEW.updated_at, '%Y-%m-%dT%H:%i:%s')
  ));
END$$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER orders_after_update
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
  INSERT INTO order_events (op, row_data) VALUES ('UPDATE', JSON_OBJECT(
    'id', NEW.id,
    'customer_name', NEW.customer_name,
    'product_name', NEW.product_name,
    'status', NEW.status,
    'updated_at', DATE_FORMAT(NEW.updated_at, '%Y-%m-%dT%H:%i:%s')
  ));
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER orders_after_delete
AFTER DELETE ON orders
FOR EACH ROW
BEGIN
  INSERT INTO order_events (op, row_data) VALUES ('DELETE', JSON_OBJECT(
    'id', OLD.id,
    'customer_name', OLD.customer_name,
    'product_name', OLD.product_name,
    'status', OLD.status,
    'updated_at', DATE_FORMAT(OLD.updated_at, '%Y-%m-%dT%H:%i:%s')
  ));
END$$
DELIMITER ;
