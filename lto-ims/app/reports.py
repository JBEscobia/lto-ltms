#reports.py - sql-based report queries for the lto ims
#uses views and stored procedures from db_objects.sql

def report_drivers_filtered(connection, license_type=None, license_status=None,
                             age_min=None, age_max=None, sex=None):
    #report 1: drivers filtered by license type, status, age range, sex
    cursor = connection.cursor()

    query = """
        SELECT license_number, full_name, date_of_birth, age, sex,
               address, license_type, license_status,
               issuance_date, expiration_date,
               vehicle_count, violation_count
        FROM driver_summary
        WHERE 1=1
    """
    values = []

    if license_type is not None:
        query += " AND license_type = %s"
        values.append(license_type)
    if license_status is not None:
        query += " AND license_status = %s"
        values.append(license_status)
    if age_min is not None:
        query += " AND age >= %s"
        values.append(age_min)
    if age_max is not None:
        query += " AND age <= %s"
        values.append(age_max)
    if sex is not None:
        query += " AND sex = %s"
        values.append(sex)

    query += " ORDER BY full_name ASC"

    try:
        cursor.execute(query, values)
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_vehicles_by_driver(connection, license_number):
    #report 2: all vehicles owned by a given driver
    cursor = connection.cursor()

    query = """
        SELECT plate_number, engine_number, chassis_number,
               vehicle_type, make, model, year_model, color
        FROM VEHICLE
        WHERE license_number = %s
        ORDER BY year_model DESC
    """

    try:
        cursor.execute(query, (license_number,))
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_expired_registrations(connection, as_of_date):
    #report 3: vehicles with expired registrations as of the given date
    cursor = connection.cursor()

    query = """
        SELECT registration_number, plate_number, vehicle_type,
               make, model, year_model, color,
               owner_name, owner_license,
               registration_date, expiration_date, registration_status
        FROM expired_registrations
        WHERE expiration_date <= %s
        ORDER BY expiration_date ASC
    """

    try:
        cursor.execute(query, (as_of_date,))
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_expired_suspended_drivers(connection):
    #report 4: drivers with expired or suspended licenses
    cursor = connection.cursor()

    query = """
        SELECT license_number, full_name, license_type,
               license_status, expiration_date
        FROM DRIVER
        WHERE license_status IN ('Expired', 'Suspended')
        ORDER BY license_status ASC, full_name ASC
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_violations_by_driver(connection, license_number, date_from, date_to):
    #report 5: violations by a driver within a date range (uses stored procedure)
    cursor = connection.cursor()
    query = "CALL get_driver_violations(%s, %s, %s)"

    try:
        cursor.execute(query, (license_number, date_from, date_to))
        rows = cursor.fetchall()
        while cursor.nextset():
            pass
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_violations_per_type(connection, year):
    #report 6: total violations per type for a given year (uses stored procedure)
    cursor = connection.cursor()
    query = "CALL get_violation_counts_by_year(%s)"

    try:
        cursor.execute(query, (year,))
        rows = cursor.fetchall()
        while cursor.nextset():
            pass
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()


def report_vehicles_in_violations_by_location(connection, location_keyword):
    #report 7: vehicles involved in violations within a city/region (uses stored procedure)
    cursor = connection.cursor()
    query = "CALL get_vehicles_with_violations_in_location(%s)"

    try:
        cursor.execute(query, (location_keyword,))
        rows = cursor.fetchall()
        while cursor.nextset():
            pass
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()
