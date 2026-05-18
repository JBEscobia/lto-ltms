# reports.py
# Wraps all 7 required SQL report queries for the LTO IMS.
#
# Rule: Functions here only RETURN data — no print() or input() allowed.
# All printing and user prompts happen in main.py only.
#
# All functions follow the same return pattern:
#   (True,  list_of_rows)  — query succeeded; list_of_rows is the result set
#   (False, error_message) — query failed; error_message explains why
#
# This file makes use of the views and stored procedures defined in db_objects.sql:
#   VIEWS:
#     driver_summary         — drivers joined with vehicle_count and violation_count (Report 1)
#     expired_registrations  — vehicles with expired registrations (Report 3)
#     violation_details      — violations joined with driver, vehicle, and fine info (Reports 5, 6, 7)
#   STORED PROCEDURES:
#     get_driver_violations(license_number, start_date, end_date)     — Report 5
#     get_violation_counts_by_year(year)                              — Report 6
#     get_vehicles_with_violations_in_location(location)             — Report 7
#
# Reports covered (7 total):
#   1. report_drivers_filtered()              — drivers filtered by license type, status, age, sex
#   2. report_vehicles_by_driver()            — all vehicles owned by a given driver
#   3. report_expired_registrations()         — vehicles with expired registrations as of a given date
#   4. report_expired_suspended_drivers()     — drivers with expired or suspended licenses
#   5. report_violations_by_driver()          — violations by a driver within a date range
#   6. report_violations_per_type()           — total violations per type for a given year
#   7. report_vehicles_in_violations_by_location() — vehicles in violations within a city/region
#
# Tables used:
#   DRIVER, VEHICLE, REGISTRATION, VIOLATION, VIOLATION_TYPE_LIST
#
# Column reference:
#   DRIVER:             license_number, full_name, date_of_birth, sex, address,
#                       license_type, license_status, issuance_date, expiration_date
#   VEHICLE:            plate_number, license_number, engine_number, chassis_number,
#                       vehicle_type, make, model, year_model, color
#   REGISTRATION:       registration_number, plate_number, registration_date,
#                       expiration_date, registration_status
#   VIOLATION:          violation_ticket_number, license_number, plate_number,
#                       violation_type, violation_date, location,
#                       apprehending_officer, violation_status
#   VIOLATION_TYPE_LIST: violation_type, corresponding_fine_amount


def report_drivers_filtered(connection, license_type=None, license_status=None,
                             age_min=None, age_max=None, sex=None):
    """
    Report 1: View all registered drivers filtered by one or more of:
              license type, license status, age range, and/or sex.

    Uses the `driver_summary` VIEW from db_objects.sql, which already computes
    each driver's age (via TIMESTAMPDIFF), vehicle_count, and violation_count.

    All filters are optional — only the ones you pass in will be applied.
    If no filters are passed, returns all drivers.

    Parameters:
        connection     - the active MariaDB connection object
        license_type   - (optional) e.g. 'Professional', 'Non-Professional', 'Student Permit'
        license_status - (optional) e.g. 'Valid', 'Expired', 'Suspended'
        age_min        - (optional) minimum age as an integer, e.g. 18
        age_max        - (optional) maximum age as an integer, e.g. 60
        sex            - (optional) 'M' or 'F'

    Returns:
        (True,  list_of_rows) — each row is a tuple:
                                (license_number, full_name, date_of_birth, age, sex,
                                 address, license_type, license_status,
                                 issuance_date, expiration_date,
                                 vehicle_count, violation_count)
        (False, error_message)

    Example usage in main.py:
        # Get all female professional drivers aged 25-40
        success, rows = report_drivers_filtered(conn,
                                                license_type='Professional',
                                                age_min=25, age_max=40,
                                                sex='F')
    """
    cursor = connection.cursor()

    # Query the driver_summary VIEW instead of the raw DRIVER table
    # The view already has the age column computed, so we don't need TIMESTAMPDIFF here
    query = """
        SELECT license_number, full_name, date_of_birth, age, sex,
               address, license_type, license_status,
               issuance_date, expiration_date,
               vehicle_count, violation_count
        FROM driver_summary
        WHERE 1=1
    """
    # WHERE 1=1 is a trick that lets us safely append AND conditions
    # without worrying about whether it's the first condition or not

    values = []

    if license_type is not None:
        query += " AND license_type = %s"
        values.append(license_type)

    if license_status is not None:
        query += " AND license_status = %s"
        values.append(license_status)

    if age_min is not None:
        # The view already has the `age` column so we can filter directly
        query += " AND age >= %s"
        values.append(age_min)

    if age_max is not None:
        query += " AND age <= %s"
        values.append(age_max)

    if sex is not None:
        query += " AND sex = %s"
        values.append(sex)

    query += " ORDER BY full_name ASC"  # Sort results alphabetically by name

    try:
        cursor.execute(query, values)
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_vehicles_by_driver(connection, license_number):
    """
    Report 2: View all vehicles owned by a given driver.
    Queries the VEHICLE table directly for all records
    linked to the given driver's license number.

    Parameters:
        connection     - the active MariaDB connection object
        license_number - the driver's license number, e.g. 'N01-12-123456'

    Returns:
        (True,  list_of_rows) — each row is a tuple:
                                (plate_number, engine_number, chassis_number,
                                 vehicle_type, make, model, year_model, color)
        (False, error_message)

    Example usage in main.py:
        success, rows = report_vehicles_by_driver(conn, 'N01-12-123456')
    """
    cursor = connection.cursor()

    query = """
        SELECT plate_number, engine_number, chassis_number,
               vehicle_type, make, model, year_model, color
        FROM VEHICLE
        WHERE license_number = %s
        ORDER BY year_model DESC
    """
    # ORDER BY year_model DESC — most recent vehicles appear first

    try:
        cursor.execute(query, (license_number,))
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_expired_registrations(connection, as_of_date):
    """
    Report 3: View all vehicles with expired registrations as of a given date.

    Uses the `expired_registrations` VIEW from db_objects.sql, which already
    joins REGISTRATION, VEHICLE, and DRIVER and filters for expired records.
    We then further filter by the given date so the user can check
    "what was expired as of X date?" (not just today).

    Parameters:
        connection - the active MariaDB connection object
        as_of_date - cutoff date as a string, e.g. '2024-01-01' (YYYY-MM-DD)
                     registrations expired on or before this date will be returned

    Returns:
        (True,  list_of_rows) — each row is a tuple:
                                (registration_number, plate_number, vehicle_type,
                                 make, model, year_model, color,
                                 owner_name, owner_license,
                                 registration_date, expiration_date, registration_status)
        (False, error_message)

    Example usage in main.py:
        success, rows = report_expired_registrations(conn, '2024-06-01')
    """
    cursor = connection.cursor()

    # The view already filters for expired registrations based on today's date.
    # We add an extra condition to also support checking as of a past/future date.
    query = """
        SELECT registration_number, plate_number, vehicle_type,
               make, model, year_model, color,
               owner_name, owner_license,
               registration_date, expiration_date, registration_status
        FROM expired_registrations
        WHERE expiration_date <= %s
        ORDER BY expiration_date ASC
    """
    # ORDER BY expiration_date ASC — oldest expiration first

    try:
        cursor.execute(query, (as_of_date,))
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_expired_suspended_drivers(connection):
    """
    Report 4: View all drivers with expired OR suspended licenses.
    No parameters needed — returns all drivers whose license_status
    is either 'Expired' or 'Suspended'.

    Queries the DRIVER table directly since there is no view for this report.

    Parameters:
        connection - the active MariaDB connection object

    Returns:
        (True,  list_of_rows) — each row is a tuple:
                                (license_number, full_name, license_type,
                                 license_status, expiration_date)
        (False, error_message)

    Example usage in main.py:
        success, rows = report_expired_suspended_drivers(conn)
    """
    cursor = connection.cursor()

    query = """
        SELECT license_number, full_name, license_type,
               license_status, expiration_date
        FROM DRIVER
        WHERE license_status IN ('Expired', 'Suspended')
        ORDER BY license_status ASC, full_name ASC
    """
    # IN ('Expired', 'Suspended') is shorthand for:
    # WHERE license_status = 'Expired' OR license_status = 'Suspended'

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_violations_by_driver(connection, license_number, date_from, date_to):
    """
    Report 5: View all traffic violations committed by a given driver
              within a specified date range.

    Calls the stored procedure `get_driver_violations` from db_objects.sql,
    which queries the `violation_details` VIEW filtered by license number and date range.

    Parameters:
        connection     - the active MariaDB connection object
        license_number - the driver's license number, e.g. 'N01-12-123456'
        date_from      - start of the date range, e.g. '2024-01-01' (YYYY-MM-DD, inclusive)
        date_to        - end of the date range,   e.g. '2024-12-31' (YYYY-MM-DD, inclusive)

    Returns:
        (True,  list_of_rows) — each row is a tuple:
                                (violation_ticket_number, plate_number, violation_type,
                                 fine_amount, violation_date, location,
                                 apprehending_officer, violation_status)
        (False, error_message)

    Example usage in main.py:
        success, rows = report_violations_by_driver(conn,
                                                    'N01-12-123456',
                                                    '2024-01-01',
                                                    '2024-12-31')
    """
    cursor = connection.cursor()

    # CALL executes the stored procedure defined in db_objects.sql
    # The procedure accepts 3 parameters: license_number, start_date, end_date
    query = "CALL get_driver_violations(%s, %s, %s)"

    try:
        cursor.execute(query, (license_number, date_from, date_to))
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_violations_per_type(connection, year):
    """
    Report 6: View the total number of violations per violation type for a given year.

    Calls the stored procedure `get_violation_counts_by_year` from db_objects.sql,
    which groups violations by type, counts them, and sums the fines for that year.

    Parameters:
        connection - the active MariaDB connection object
        year       - the year as an integer, e.g. 2024

    Returns:
        (True,  list_of_rows) — each row is a tuple:
                                (violation_type, total_violations, total_fines)
                                sorted from most to least violations
        (False, error_message)

    Example usage in main.py:
        success, rows = report_violations_per_type(conn, 2024)
    """
    cursor = connection.cursor()

    # CALL executes the stored procedure defined in db_objects.sql
    # The procedure accepts 1 parameter: the year
    query = "CALL get_violation_counts_by_year(%s)"

    try:
        cursor.execute(query, (year,))
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_vehicles_in_violations_by_location(connection, location_keyword):
    """
    Report 7: View all vehicles involved in violations within a given city or region.

    Calls the stored procedure `get_vehicles_with_violations_in_location` from db_objects.sql,
    which does a partial LIKE match on the location field of the violation_details VIEW.
    e.g. 'Laguna' will match 'Calamba, Laguna', 'Los Baños, Laguna', etc.

    Parameters:
        connection       - the active MariaDB connection object
        location_keyword - city or region to search for, e.g. 'Laguna', 'Calamba'

    Returns:
        (True,  list_of_rows) — each row is a tuple:
                                (plate_number, make, model,
                                 driver_name, license_number, violation_count)
                                sorted by violation_count descending
        (False, error_message)

    Example usage in main.py:
        success, rows = report_vehicles_in_violations_by_location(conn, 'Laguna')
    """
    cursor = connection.cursor()

    # CALL executes the stored procedure defined in db_objects.sql
    # The procedure accepts 1 parameter: the location keyword
    # The CONCAT('%', p_location, '%') for the LIKE match is handled inside the procedure
    query = "CALL get_vehicles_with_violations_in_location(%s)"

    try:
        cursor.execute(query, (location_keyword,))
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()