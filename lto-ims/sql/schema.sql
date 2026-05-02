-- LTO IMS Schema
-- Run this file first to initialize all tables

CREATE DATABASE IF NOT EXISTS lto_ims;
USE lto_ims;

-- DRIVER Table
CREATE TABLE DRIVER (
    license_number VARCHAR(50),
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    sex CHAR(1),
    address VARCHAR(255),
    license_type VARCHAR(50),
    license_status VARCHAR(20),
    issuance_date DATE,
    expiration_date DATE,
    CONSTRAINT driver_licensenumber_pk PRIMARY KEY (license_number)
);

-- VEHICLE Table
CREATE TABLE VEHICLE (
    plate_number VARCHAR(20),
    license_number VARCHAR(50),
    engine_number VARCHAR(50) NOT NULL,
    chassis_number VARCHAR(50) NOT NULL,
    vehicle_type VARCHAR(50),
    make VARCHAR(50),
    model VARCHAR(50),
    year_model INT(4),
    color VARCHAR(30),
    CONSTRAINT vehicle_platenumber_pk PRIMARY KEY (plate_number),
    CONSTRAINT vehicle_enginenumber_uk UNIQUE (engine_number),
    CONSTRAINT vehicle_chassisnumber_uk UNIQUE (chassis_number),
    CONSTRAINT vehicle_licensenumber_fk FOREIGN KEY (license_number) REFERENCES DRIVER(license_number)
);

-- REGISTRATION Table
CREATE TABLE REGISTRATION (
    registration_number VARCHAR(50),
    plate_number VARCHAR(20),
    registration_date DATE,
    expiration_date DATE,
    registration_status VARCHAR(20),
    CONSTRAINT registration_registrationnumber_pk PRIMARY KEY (registration_number),
    CONSTRAINT registration_platenumber_fk FOREIGN KEY (plate_number) REFERENCES VEHICLE(plate_number)
);

-- VIOLATION_TYPE_LIST Table
CREATE TABLE VIOLATION_TYPE_LIST (
    violation_type VARCHAR(100),
    corresponding_fine_amount DECIMAL(10, 2),
    CONSTRAINT violationtypelist_violationtype_pk PRIMARY KEY (violation_type)
);

-- VIOLATION Table
CREATE TABLE VIOLATION (
    violation_ticket_number VARCHAR(50),
    license_number VARCHAR(50),
    plate_number VARCHAR(20),
    violation_type VARCHAR(100),
    violation_date DATE,
    location VARCHAR(255),
    apprehending_officer VARCHAR(100),
    violation_status VARCHAR(20),
    CONSTRAINT violation_violationticketnumber_pk PRIMARY KEY (violation_ticket_number),
    CONSTRAINT violation_licensenumber_fk FOREIGN KEY (license_number) REFERENCES DRIVER(license_number),
    CONSTRAINT violation_platenumber_fk FOREIGN KEY (plate_number) REFERENCES VEHICLE(plate_number),
    CONSTRAINT violation_violationtype_fk FOREIGN KEY (violation_type) REFERENCES VIOLATION_TYPE_LIST(violation_type)
);
