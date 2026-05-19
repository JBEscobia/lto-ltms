# this file contains functions for managing vehicle registrations in the database

def add_registration(connection, registration_number, plate_number, registration_date, expiration_date, registration_status):
   
    cursor = connection.cursor()

    query = """
        INSERT INTO REGISTRATION (
            registration_number, plate_number,
            registration_date, expiration_date, registration_status
        ) VALUES (%s, %s, %s, %s, %s)
    """
    values = (registration_number, plate_number,
              registration_date, expiration_date, registration_status)

    try:
        cursor.execute(query, values)   # Run the INSERT
        connection.commit()             # Save changes to the database
        return (True, "Registration added successfully.")
    except Exception as e:
        connection.rollback()           # Undo any partial changes if something failed
        return (False, str(e))
    finally:
        cursor.close()                  # Always close the cursor to free up resources


def update_registration(connection, registration_number, plate_number=None, registration_date=None, 
                        expiration_date=None, registration_status=None):
    cursor = connection.cursor()

    # Dynamically build the SET clause — only include fields that were actually provided
    fields = []     # Holds strings like "registration_status = %s"
    values = []     # Holds the actual new values in the same order as fields

    if plate_number is not None:
        fields.append("plate_number = %s")
        values.append(plate_number)
    if registration_date is not None:
        fields.append("registration_date = %s")
        values.append(registration_date)
    if expiration_date is not None:
        fields.append("expiration_date = %s")
        values.append(expiration_date)
    if registration_status is not None:
        fields.append("registration_status = %s")
        values.append(registration_status)

    # If nothing was passed in, there's nothing to update
    if not fields:
        return (False, "No fields provided to update.")

    # registration_number goes at the end — it goes in the WHERE clause, not SET
    values.append(registration_number)

    # Build the final query dynamically, e.g.:
    # UPDATE REGISTRATION SET expiration_date = %s, registration_status = %s
    # WHERE registration_number = %s
    query = f"UPDATE REGISTRATION SET {', '.join(fields)} WHERE registration_number = %s"

    try:
        cursor.execute(query, values)
        connection.commit()

        # rowcount tells us how many rows were actually changed
        # If 0, the registration_number didn't match any record
        if cursor.rowcount == 0:
            return (False, "No registration found with that number.")
        return (True, "Registration updated successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def delete_registration(connection, registration_number):
    cursor = connection.cursor()
    query = "DELETE FROM REGISTRATION WHERE registration_number = %s"

    try:
        cursor.execute(query, (registration_number,))   # Trailing comma makes it a tuple
        connection.commit()

        # If no rows were deleted, the registration number didn't exist
        if cursor.rowcount == 0:
            return (False, "No registration found with that number.")
        return (True, "Registration deleted successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def search_registrations(connection, keyword=None, plate_number=None, registration_status=None):
    cursor = connection.cursor()

    # Base query — WHERE 1=1 lets us safely append AND conditions
    # without worrying about whether it's the first condition or not
    query = """
        SELECT registration_number, plate_number,
               registration_date, expiration_date, registration_status
        FROM REGISTRATION
        WHERE 1=1
    """
    values = []

    if keyword is not None:
        # LIKE %keyword% matches registration numbers that contain the keyword
        query += " AND registration_number LIKE %s"
        values.append(f"%{keyword}%")

    if plate_number is not None:
        # Exact match — a vehicle's plate number is a fixed identifier
        query += " AND plate_number = %s"
        values.append(plate_number)

    if registration_status is not None:
        query += " AND registration_status = %s"
        values.append(registration_status)

    # Show most recent registrations first
    query += " ORDER BY registration_date DESC"

    try:
        cursor.execute(query, values)
        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()