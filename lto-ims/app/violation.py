# this file contains functions for managing traffic violations in the database
def add_violation(connection, violation_ticket_number, license_number,
                  plate_number, violation_type, violation_date,
                  location, violation_status, apprehending_officer=None):

    cursor = connection.cursor()
    query = """
        INSERT INTO VIOLATION (
            violation_ticket_number, license_number, plate_number,
            violation_type, violation_date, location,
            apprehending_officer, violation_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (violation_ticket_number, license_number, plate_number,
              violation_type, violation_date, location,
              apprehending_officer, violation_status)
    try:
        cursor.execute(query, values)
        connection.commit()
        return (True, "Violation record added successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()

def update_violation(connection, violation_ticket_number, license_number=None,
                     plate_number=None, violation_type=None, violation_date=None,
                     location=None, apprehending_officer=None, violation_status=None):

    cursor = connection.cursor()

    fields = []
    values = []

    if license_number is not None:
        fields.append("license_number = %s")
        values.append(license_number)
    if plate_number is not None:
        fields.append("plate_number = %s")
        values.append(plate_number)
    if violation_type is not None:
        fields.append("violation_type = %s")
        values.append(violation_type)
    if violation_date is not None:
        fields.append("violation_date = %s")
        values.append(violation_date)
    if location is not None:
        fields.append("location = %s")
        values.append(location)
    if apprehending_officer is not None:
        fields.append("apprehending_officer = %s")
        values.append(apprehending_officer)
    if violation_status is not None:
        fields.append("violation_status = %s")
        values.append(violation_status)

    if not fields:
        return (False, "No fields provided to update.")

    values.append(violation_ticket_number)
    query = f"UPDATE VIOLATION SET {', '.join(fields)} WHERE violation_ticket_number = %s"

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            return (False, "No violation found with that ticket number.")
        return (True, "Violation record updated successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def delete_violation(connection, violation_ticket_number):

    cursor = connection.cursor()
    query = "DELETE FROM VIOLATION WHERE violation_ticket_number = %s"

    try:
        cursor.execute(query, (violation_ticket_number,))
        connection.commit()
        if cursor.rowcount == 0:
            return (False, "No violation found with that ticket number.")
        return (True, "Violation record deleted successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def search_violations(connection, keyword=None, license_number=None,
                      plate_number=None, violation_status=None, violation_type=None):

    cursor = connection.cursor()

    # JOIN with VIOLATION_TYPE_LIST so we can show the fine amount in results
    query = """
        SELECT v.violation_ticket_number, v.license_number, v.plate_number,
               v.violation_type, vtl.corresponding_fine_amount,
               v.violation_date, v.location,
               v.apprehending_officer, v.violation_status
        FROM VIOLATION v
        JOIN VIOLATION_TYPE_LIST vtl ON v.violation_type = vtl.violation_type
        WHERE 1=1
    """
    values = []

    if keyword is not None:
        query += " AND v.violation_ticket_number LIKE %s"
        values.append(f"%{keyword}%")
    if license_number is not None:
        query += " AND v.license_number = %s"
        values.append(license_number)
    if plate_number is not None:
        query += " AND v.plate_number = %s"
        values.append(plate_number)
    if violation_status is not None:
        query += " AND v.violation_status = %s"
        values.append(violation_status)
    if violation_type is not None:
        query += " AND v.violation_type = %s"
        values.append(violation_type)

    query += " ORDER BY v.violation_date DESC"

    try:
        cursor.execute(query, values)
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()