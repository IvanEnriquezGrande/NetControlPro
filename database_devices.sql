CREATE DATABASE devices;
use  devices;

CREATE TABLE devices(
    device_id INT NOT NULL AUTO_INCREMENT,
    device_name varchar(30) UNIQUE NOT NULL,
    device_username varchar(40) NOT NULL,
    device_password varchar(30) NOT NULL,
    device_ip varchar(15) UNIQUE NOT NULL,
    device_type varchar(20) NOT NULL,
    add_date DATE NOT NULL,
    PRIMARY KEY (device_id) 
);

INSERT INTO devices(device_name, device_username, device_password, device_ip, device_type, add_date)
VALUES("SWITCH1", "ivan", "root", "10.10.10.10", "switch", CURRENT_DATE);

INSERT INTO devices(device_name, device_username, device_password, device_ip, device_type, add_date)
VALUES("ROUTER1", "ivan", "root", "10.10.10.11", "router", CURRENT_DATE);

INSERT INTO devices(device_name, device_username, device_password, device_ip, device_type, add_date)
VALUES("SWITCH2", "ivan", "root", "10.10.10.12", "switch", CURRENT_DATE);

INSERT INTO devices(device_name, device_username, device_password, device_ip, device_type, add_date)
VALUES("ROUTER2", "ivan", "root", "10.10.10.13", "router", CURRENT_DATE);

INSERT INTO devices(device_name, device_username, device_password, device_ip, device_type, add_date)
VALUES("SWITCH3", "ivan", "root", "10.10.10.14", "switch", CURRENT_DATE);
