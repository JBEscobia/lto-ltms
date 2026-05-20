-- views, stored procedures, and triggers for the lto ims

USE lto_ims;

-- views

-- driver info with computed age, vehicle count, and violation count
CREATE OR REPLACE VIEW driver_summary AS
SELECT
    d.license_number,
    d.full_name,
    d.date_of_birth,
    TIMESTAMPDIFF(YEAR, d.date_of_birth, CURDATE()) AS age,
    d.sex,
    d.address,
    d.license_type,
    d.license_status,
    d.issuance_date,
    d.expiration_date,
    COUNT(DISTINCT v.plate_number)  AS vehicle_count,
    COUNT(DISTINCT vl.violation_ticket_number) AS violation_count
FROM DRIVER d
LEFT JOIN VEHICLE v  ON d.license_number = v.license_number
LEFT JOIN VIOLATION vl ON d.license_number = vl.license_number
GROUP BY
    d.license_number, d.full_name, d.date_of_birth, d.sex,
    d.address, d.license_type, d.license_status,
    d.issuance_date, d.expiration_date;


-- vehicles with expired registrations
CREATE OR REPLACE VIEW expired_registrations AS
SELECT
    r.registration_number,
    r.plate_number,
    v.vehicle_type,
    v.make,
    v.model,
    v.year_model,
    v.color,
    d.full_name       AS owner_name,
    d.license_number   AS owner_license,
    r.registration_date,
    r.expiration_date,
    r.registration_status
FROM REGISTRATION r
JOIN VEHICLE v ON r.plate_number = v.plate_number
JOIN DRIVER d  ON v.license_number = d.license_number
WHERE r.expiration_date < CURDATE()
   OR r.registration_status = 'Expired';


-- flattened violation info with driver, vehicle, and fine details
CREATE OR REPLACE VIEW violation_details AS
SELECT
    vl.violation_ticket_number,
    vl.license_number,
    d.full_name           AS driver_name,
    vl.plate_number,
    v.make,
    v.model,
    vl.violation_type,
    vtl.corresponding_fine_amount AS fine_amount,
    vl.violation_date,
    vl.location,
    vl.apprehending_officer,
    vl.violation_status
FROM VIOLATION vl
JOIN DRIVER d             ON vl.license_number = d.license_number
JOIN VEHICLE v            ON vl.plate_number   = v.plate_number
JOIN VIOLATION_TYPE_LIST vtl ON vl.violation_type  = vtl.violation_type;


-- stored procedures

-- get violations by a driver within a date range
DROP PROCEDURE IF EXISTS get_driver_violations;
DELIMITER //
CREATE PROCEDURE get_driver_violations(
    IN p_license_number VARCHAR(50),
    IN p_start_date     DATE,
    IN p_end_date       DATE
)
BEGIN
    SELECT
        violation_ticket_number,
        plate_number,
        violation_type,
        fine_amount,
        violation_date,
        location,
        apprehending_officer,
        violation_status
    FROM violation_details
    WHERE license_number = p_license_number
      AND violation_date BETWEEN p_start_date AND p_end_date
    ORDER BY violation_date;
END //
DELIMITER ;


-- get violation counts grouped by type for a given year
DROP PROCEDURE IF EXISTS get_violation_counts_by_year;
DELIMITER //
CREATE PROCEDURE get_violation_counts_by_year(
    IN p_year INT
)
BEGIN
    SELECT
        violation_type,
        COUNT(*) AS total_violations,
        SUM(fine_amount) AS total_fines
    FROM violation_details
    WHERE YEAR(violation_date) = p_year
    GROUP BY violation_type
    ORDER BY total_violations DESC;
END //
DELIMITER ;


-- get vehicles involved in violations matching a location keyword
DROP PROCEDURE IF EXISTS get_vehicles_with_violations_in_location;
DELIMITER //
CREATE PROCEDURE get_vehicles_with_violations_in_location(
    IN p_location VARCHAR(255)
)
BEGIN
    SELECT DISTINCT
        vd.plate_number,
        vd.make,
        vd.model,
        vd.driver_name,
        vd.license_number,
        COUNT(*) AS violation_count
    FROM violation_details vd
    WHERE vd.location LIKE CONCAT('%', p_location, '%')
    GROUP BY vd.plate_number, vd.make, vd.model,
             vd.driver_name, vd.license_number
    ORDER BY violation_count DESC;
END //
DELIMITER ;


-- triggers

-- auto-set registration status to expired if expiration date is past (on insert)
DROP TRIGGER IF EXISTS trg_registration_auto_expire_insert;
DELIMITER //
CREATE TRIGGER trg_registration_auto_expire_insert
BEFORE INSERT ON REGISTRATION
FOR EACH ROW
BEGIN
    IF NEW.expiration_date < CURDATE() AND NEW.registration_status != 'Expired' THEN
        SET NEW.registration_status = 'Expired';
    END IF;
END //
DELIMITER ;

-- same check on update
DROP TRIGGER IF EXISTS trg_registration_auto_expire_update;
DELIMITER //
CREATE TRIGGER trg_registration_auto_expire_update
BEFORE UPDATE ON REGISTRATION
FOR EACH ROW
BEGIN
    IF NEW.expiration_date < CURDATE() AND NEW.registration_status != 'Expired' THEN
        SET NEW.registration_status = 'Expired';
    END IF;
END //
DELIMITER ;

-- auto-expire driver license if expiration date is changed to a past date
DROP TRIGGER IF EXISTS trg_driver_license_auto_expire;
DELIMITER //
CREATE TRIGGER trg_driver_license_auto_expire
BEFORE UPDATE ON DRIVER
FOR EACH ROW
BEGIN
    IF NEW.expiration_date < CURDATE() AND NEW.license_status = 'Valid' THEN
        SET NEW.license_status = 'Expired';
    END IF;
END //
DELIMITER ;
