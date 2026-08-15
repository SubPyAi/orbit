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
    id CHAR(128),
    name varchar(64),
    configuration JSON,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    msgdata JSON
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
    user_a_msgs INT DEFAULT 0,
    user_b_msgs INT DEFAULT 0,
    last_var_assignment TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    G FLOAT DEFAULT 0,
    M FLOAT DEFAULT 0,
    I INT DEFAULT 0,
    user_a_last_response TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_b_last_response TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SolarMembers (
    sl_id CHAR(128),
    role VARCHAR(64),
    id CHAR(128),
    joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE OrbitMessages (
    msg_id CHAR(128) PRIMARY KEY,
    orb_id CHAR(128),
    id CHAR(128),
    data TEXT,
    at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited INT DEFAULT 0
);

CREATE TABLE SolarMessages (
    msg_id CHAR(128) PRIMARY KEY,
    sl_id CHAR(128),
    id CHAR(128),
    data TEXT,
    at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited INT DEFAULT 0
);
