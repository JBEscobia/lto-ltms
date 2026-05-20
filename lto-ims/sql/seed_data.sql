-- dummy data for testing

USE lto_ims;

START TRANSACTION;

INSERT INTO DRIVER VALUES
('N01-12-123456', 'Jeremias Gomez', '1995-05-15', 'M', 'Los Baños, Laguna', 'Non-Professional', 'Valid', '2021-05-15', '2031-05-15'),
('P02-09-987654', 'John Bryan Escobia', '1988-10-20', 'M', 'Calamba, Laguna', 'Professional', 'Expired', '2013-10-20', '2023-10-20'),
('S03-11-112233', 'Juan Pablo Regala', '2002-02-14', 'M', 'Sta. Cruz, Laguna', 'Student Permit', 'Suspended', '2023-02-14', '2024-02-14'),
('N04-08-445566', 'Maria Clara Santos', '1990-08-22', 'F', 'Bay, Laguna', 'Non-Professional', 'Valid', '2020-08-22', '2030-08-22'),
('P05-03-778899', 'Ricardo Dalisay', '1985-03-10', 'M', 'San Pablo, Laguna', 'Professional', 'Valid', '2019-03-10', '2029-03-10'),
('N06-11-334455', 'Angela Reyes', '1998-11-30', 'F', 'Makati, Manila', 'Non-Professional', 'Valid', '2022-11-30', '2032-11-30'),
('P07-06-221100', 'Jose Manalo', '1979-06-18', 'M', 'Quezon City, Manila', 'Professional', 'Expired', '2014-06-18', '2024-06-18'),
('N08-01-667788', 'Patricia Villanueva', '1993-01-05', 'F', 'Pasig, Manila', 'Non-Professional', 'Suspended', '2021-01-05', '2031-01-05'),
('S09-07-990011', 'Mark Andrei Torres', '2004-07-25', 'M', 'Los Baños, Laguna', 'Student Permit', 'Valid', '2025-01-10', '2026-01-10'),
('N10-04-556677', 'Sofia Gabriela Cruz', '1997-04-12', 'F', 'Sta. Rosa, Laguna', 'Non-Professional', 'Valid', '2023-04-12', '2033-04-12'),
('P11-09-112244', 'Roberto Garcia', '1982-09-03', 'M', 'Biñan, Laguna', 'Professional', 'Valid', '2020-09-03', '2030-09-03'),
('N12-12-889900', 'Carmela Diaz', '2000-12-20', 'F', 'Taguig, Manila', 'Non-Professional', 'Revoked', '2022-12-20', '2032-12-20');

INSERT INTO VEHICLE VALUES
('ABC-1234', 'N01-12-123456', 'ENG98765', 'CHAS12345', 'Private Car', 'Toyota', 'Vios', 2020, 'Red'),
('XYZ-9876', 'P02-09-987654', 'ENG11223', 'CHAS99887', 'Public Utility Vehicle', 'Isuzu', 'Crosswind', 2018, 'White'),
('MTC-5555', 'N01-12-123456', 'ENG44444', 'CHAS55555', 'Motorcycle', 'Honda', 'Click', 2022, 'Black'),
('DEF-5678', 'N04-08-445566', 'ENG22334', 'CHAS22334', 'Private Car', 'Honda', 'City', 2021, 'Silver'),
('GHI-9012', 'P05-03-778899', 'ENG55667', 'CHAS55667', 'Public Utility Vehicle', 'Toyota', 'Hiace', 2019, 'White'),
('JKL-3456', 'N06-11-334455', 'ENG88990', 'CHAS88990', 'Private Car', 'Mitsubishi', 'Mirage', 2023, 'Blue'),
('MNO-7890', 'P07-06-221100', 'ENG11445', 'CHAS11445', 'Public Utility Vehicle', 'Nissan', 'NV350', 2017, 'Yellow'),
('MTC-1111', 'N08-01-667788', 'ENG77889', 'CHAS77889', 'Motorcycle', 'Yamaha', 'Mio', 2022, 'Red'),
('PQR-2345', 'N10-04-556677', 'ENG33556', 'CHAS33556', 'Private Car', 'Toyota', 'Wigo', 2024, 'White'),
('STU-6789', 'P11-09-112244', 'ENG99001', 'CHAS99001', 'Public Utility Vehicle', 'Isuzu', 'NLR', 2020, 'Green'),
('MTC-2222', 'P05-03-778899', 'ENG66778', 'CHAS66778', 'Motorcycle', 'Honda', 'TMX', 2018, 'Black'),
('VWX-3344', 'N12-12-889900', 'ENG44557', 'CHAS44557', 'Private Car', 'Ford', 'EcoSport', 2021, 'Gray');

INSERT INTO REGISTRATION VALUES
('REG-001', 'ABC-1234', '2023-01-10', '2024-01-10', 'Expired'),
('REG-002', 'XYZ-9876', '2022-05-20', '2023-05-20', 'Expired'),
('REG-003', 'MTC-5555', '2024-08-15', '2025-08-15', 'Active'),
('REG-004', 'DEF-5678', '2024-03-01', '2025-03-01', 'Active'),
('REG-005', 'GHI-9012', '2024-06-10', '2025-06-10', 'Active'),
('REG-006', 'JKL-3456', '2024-01-15', '2025-01-15', 'Active'),
('REG-007', 'MNO-7890', '2022-09-01', '2023-09-01', 'Expired'),
('REG-008', 'MTC-1111', '2024-04-20', '2025-04-20', 'Suspended'),
('REG-009', 'PQR-2345', '2024-11-05', '2025-11-05', 'Active'),
('REG-010', 'STU-6789', '2024-07-18', '2025-07-18', 'Active'),
('REG-011', 'MTC-2222', '2023-02-28', '2024-02-28', 'Expired'),
('REG-012', 'VWX-3344', '2024-05-12', '2025-05-12', 'Suspended'),
('REG-013', 'ABC-1234', '2024-01-15', '2025-01-15', 'Active');

INSERT INTO VIOLATION_TYPE_LIST VALUES
('Overspeeding', 1000.00),
('Reckless Driving', 2000.00),
('Driving without License', 3000.00),
('Beating the Red Light', 1500.00),
('Illegal Parking', 500.00),
('No Helmet', 1500.00),
('Swerving', 1000.00),
('Overloading', 2000.00),
('Driving under the Influence', 5000.00),
('Expired Registration', 1000.00);

INSERT INTO VIOLATION VALUES
('TKT-9901', 'N01-12-123456', 'ABC-1234', 'Overspeeding', '2024-02-10', 'Calamba, Laguna', 'Officer Reyes', 'Unpaid'),
('TKT-9902', 'P02-09-987654', 'XYZ-9876', 'Reckless Driving', '2023-11-05', 'Los Baños, Laguna', 'Officer Santos', 'Paid'),
('TKT-9903', 'N01-12-123456', 'MTC-5555', 'Beating the Red Light', '2024-03-15', 'Calamba, Laguna', 'Officer Cruz', 'Contested'),
('TKT-9904', 'N04-08-445566', 'DEF-5678', 'Illegal Parking', '2024-05-20', 'Los Baños, Laguna', 'Officer Ramos', 'Paid'),
('TKT-9905', 'P05-03-778899', 'GHI-9012', 'Overloading', '2024-01-08', 'San Pablo, Laguna', 'Officer Bautista', 'Unpaid'),
('TKT-9906', 'N06-11-334455', 'JKL-3456', 'Overspeeding', '2024-06-12', 'Makati, Manila', 'Officer Mendoza', 'Paid'),
('TKT-9907', 'P07-06-221100', 'MNO-7890', 'Expired Registration', '2024-04-03', 'Quezon City, Manila', 'Officer Aquino', 'Unpaid'),
('TKT-9908', 'N08-01-667788', 'MTC-1111', 'No Helmet', '2024-07-22', 'Los Baños, Laguna', NULL, 'Unpaid'),
('TKT-9909', 'P05-03-778899', 'MTC-2222', 'No Helmet', '2024-08-14', 'Bay, Laguna', 'Officer Reyes', 'Paid'),
('TKT-9910', 'N10-04-556677', 'PQR-2345', 'Swerving', '2024-09-30', 'Sta. Rosa, Laguna', 'Officer Garcia', 'Contested'),
('TKT-9911', 'N12-12-889900', 'VWX-3344', 'Driving under the Influence', '2024-03-17', 'Taguig, Manila', 'Officer Dela Cruz', 'Unpaid'),
('TKT-9912', 'P11-09-112244', 'STU-6789', 'Overloading', '2024-10-05', 'Biñan, Laguna', NULL, 'Unpaid'),
('TKT-9913', 'N01-12-123456', 'ABC-1234', 'Illegal Parking', '2024-11-18', 'Los Baños, Laguna', 'Officer Santos', 'Paid'),
('TKT-9914', 'P02-09-987654', 'XYZ-9876', 'Driving without License', '2024-04-25', 'Calamba, Laguna', 'Officer Cruz', 'Unpaid'),
('TKT-9915', 'N06-11-334455', 'JKL-3456', 'Beating the Red Light', '2024-12-01', 'Pasay, Manila', 'Officer Tan', 'Contested');

COMMIT;
