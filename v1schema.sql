-- Orbit v1 MySQL schema

CREATE DATABASE IF NOT EXISTS Orbit CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE Orbit;

CREATE TABLE Users (
    id CHAR(128) PRIMARY KEY,
    username VARCHAR(64),
    password VARCHAR(255),
    email VARCHAR(512),
    phone CHAR(10),
    DoB DATE,
    created TIMESTAMP
);

CREATE TABLE Solars (
    sl_id CHAR(128) PRIMARY KEY,
    configuration VARCHAR(255),
    created TIMESTAMP,
    SNRNCOUNT INT
);

CREATE TABLE Sessions (
    sessid CHAR(128),
    id CHAR(128) PRIMARY KEY,
    created TIMESTAMP,
    void BOOL DEFAULT FALSE
);

CREATE TABLE Orbits (
    orb_id CHAR(128) PRIMARY KEY,
    user_a CHAR(128),
    user_b CHAR(128),
    user_a_msgs INT,
    user_b_msgs INT,
    SNRNCOUNT INT,
    lastavg FLOAT,
    G FLOAT,
    M FLOAT,
    I INT,
    user_a_last_response TIMESTAMP,
    user_b_last_response TIMESTAMP
);

CREATE TABLE SolarMembers (
    sl_id CHAR(128),
    role VARCHAR(64),
    id CHAR(128),
    joined TIMESTAMP
);

CREATE TABLE OrbitMessages (
    msg_id CHAR(128) PRIMARY KEY,
    orb_id CHAR(128),
    id CHAR(128),
    data TEXT,
    at TIMESTAMP
);

CREATE TABLE SolarMessages (
    msg_id CHAR(128) PRIMARY KEY,
    sl_id CHAR(128),
    id CHAR(128),
    data TEXT,
    at TIMESTAMP,
    edited INT DEFAULT 0
);

CREATE TABLE QueryQueue (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    operation TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'processing', 'done') DEFAULT 'pending'
);