-- LTO IMS Seed Data
-- Run this after schema.sql to populate tables with dummy data

USE lto_ims;

START TRANSACTION;

INSERT INTO DRIVER VALUES 
('N01-12-123456', 'Jeremias Gomez', '1995-05-15', 'M', 'Los Baños, Laguna', 'Non-Professional', 'Valid', '2021-05-15', '2031-05-15'),
('P02-09-987654', 'John Bryan Escobia', '1988-10-20', 'M', 'Calamba, Laguna', 'Professional', 'Expired', '2013-10-20', '2023-10-20'),
('S03-11-112233', 'Juan Pablo Regala', '2002-02-14', 'M', 'Sta Cruz, Laguna', 'Student Permit', 'Suspended', '2023-02-14', '2024-02-14');

INSERT INTO VEHICLE VALUES
('ABC-1234', 'N01-12-123456', 'ENG98765', 'CHAS12345', 'Private Car', 'Toyota', 'Vios', 2020, 'Red'),
('XYZ-9876', 'P02-09-987654', 'ENG11223', 'CHAS99887', 'Public Utility Vehicle', 'Isuzu', 'Crosswind', 2018, 'White'),
('MTC-5555', 'N01-12-123456', 'ENG44444', 'CHAS55555', 'Motorcycle', 'Honda', 'Click', 2022, 'Black');

INSERT INTO REGISTRATION VALUES
('REG-001', 'ABC-1234', '2023-01-10', '2024-01-10', 'Active'),
('REG-002', 'XYZ-9876', '2022-05-20', '2023-05-20', 'Expired'),
('REG-003', 'MTC-5555', '2023-08-15', '2024-08-15', 'Active');

INSERT INTO VIOLATION_TYPE_LIST VALUES
('Overspeeding', 1000.00),
('Reckless Driving', 2000.00),
('Driving without License', 3000.00),
('Beating the Red Light', 1500.00);

INSERT INTO VIOLATION VALUES
('TKT-9901', 'N01-12-123456', 'ABC-1234', 'Overspeeding', '2024-02-10', 'Calamba, Laguna', 'Officer Reyes', 'Unpaid'),
('TKT-9902', 'P02-09-987654', 'XYZ-9876', 'Reckless Driving', '2023-11-05', 'Los Baños, Laguna', 'Officer Santos', 'Paid'),
('TKT-9903', 'N01-12-123456', 'MTC-5555', 'Beating the Red Light', '2024-03-15', 'Calamba, Laguna', 'Officer Cruz', 'Contested');

COMMIT;
