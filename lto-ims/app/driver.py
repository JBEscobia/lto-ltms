# driver.py
# Handles all driver-related database operations.
#
# Rule: Functions here only RETURN data — no print() or input() allowed.
# All printing and user prompts happen in main.py only.
#
# All functions follow the same return pattern:
#   (True,  result)        — operation succeeded; result is a message or list of rows
#   (False, error_message) — operation failed; error_message explains why
#
# DRIVER table columns (in order):
#   license_number  VARCHAR(50)  — PRIMARY KEY, e.g. 'N01-12-123456'
#   full_name       VARCHAR(100) — e.g. 'Juan Dela Cruz'
#   date_of_birth   DATE         — e.g. '1995-05-15' (YYYY-MM-DD)
#   sex             CHAR(1)      — 'M' or 'F'
#   address         VARCHAR(255) — e.g. 'Calamba, Laguna'
#   license_type    VARCHAR(50)  — e.g. 'Professional', 'Non-Professional', 'Student Permit'
#   license_status  VARCHAR(20)  — e.g. 'Valid', 'Expired', 'Suspended'
#   issuance_date   DATE         — e.g. '2021-05-15' (YYYY-MM-DD)
#   expiration_date DATE         — e.g. '2031-05-15' (YYYY-MM-DD)


def add_driver(connection, license_number, full_name, date_of_birth, sex,
               address, license_type, license_status, issuance_date, expiration_date):
    """
    Inserts a brand new driver into the DRIVER table.

    Parameters:
        connection      - the active MariaDB connection object (from db_connection.py)
        license_number  - e.g. 'N01-12-123456' (primary key, must be unique)
        full_name       - e.g. 'Juan Dela Cruz'
        date_of_birth   - e.g. '1995-05-15' (YYYY-MM-DD format)
        sex             - 'M' or 'F'
        address         - e.g. 'Calamba, Laguna'
        license_type    - e.g. 'Professional', 'Non-Professional', 'Student Permit'
        license_status  - e.g. 'Valid', 'Expired', 'Suspended'
        issuance_date   - e.g. '2021-05-15' (YYYY-MM-DD format)
        expiration_date - e.g. '2031-05-15' (YYYY-MM-DD format)

    Returns:
        (True,  "Driver added successfully.")  — if insert worked
        (False, error_message)                 — if something went wrong (e.g. duplicate license number)
    """
    cursor = connection.cursor()

    # %s are placeholders — mysql-connector fills them in safely to prevent SQL injection
    query = """
        INSERT INTO DRIVER (
            license_number, full_name, date_of_birth, sex,
            address, license_type, license_status, issuance_date, expiration_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (license_number, full_name, date_of_birth, sex,
              address, license_type, license_status, issuance_date, expiration_date)

    try:
        cursor.execute(query, values)   # Run the INSERT
        connection.commit()             # Save changes to the database
        return (True, "Driver added successfully.")
    except Exception as e:
        connection.rollback()           # Undo any partial changes if something failed
        return (False, str(e))
    finally:
        cursor.close()                  # Always close the cursor to free up resources


def update_driver(connection, license_number, full_name=None, date_of_birth=None,
                  sex=None, address=None, license_type=None, license_status=None,
                  issuance_date=None, expiration_date=None):
    """
    Updates an existing driver's information in the DRIVER table.
    Only the fields you pass in will be updated — fields left as None are ignored.
    This way you don't have to re-enter every field just to change one thing.

    Parameters:
        connection      - the active MariaDB connection object
        license_number  - the driver to update (used in the WHERE clause)
        full_name       - (optional) new full name
        date_of_birth   - (optional) new date of birth
        sex             - (optional) new sex
        address         - (optional) new address
        license_type    - (optional) new license type
        license_status  - (optional) new license status
        issuance_date   - (optional) new issuance date
        expiration_date - (optional) new expiration date

    Returns:
        (True,  "Driver updated successfully.")              — if update worked
        (False, "No driver found with that license number.") — if license number doesn't exist
        (False, "No fields provided to update.")             — if no fields were passed in
        (False, error_message)                               — if a database error occurred
    """
    cursor = connection.cursor()

    # Dynamically build the SET clause based on which fields were provided
    fields = []     # Will hold strings like "full_name = %s"
    values = []     # Will hold the actual values in the same order

    if full_name is not None:
        fields.append("full_name = %s")
        values.append(full_name)
    if date_of_birth is not None:
        fields.append("date_of_birth = %s")
        values.append(date_of_birth)
    if sex is not None:
        fields.append("sex = %s")
        values.append(sex)
    if address is not None:
        fields.append("address = %s")
        values.append(address)
    if license_type is not None:
        fields.append("license_type = %s")
        values.append(license_type)
    if license_status is not None:
        fields.append("license_status = %s")
        values.append(license_status)
    if issuance_date is not None:
        fields.append("issuance_date = %s")
        values.append(issuance_date)
    if expiration_date is not None:
        fields.append("expiration_date = %s")
        values.append(expiration_date)

    # If nothing was passed in, there's nothing to update
    if not fields:
        return (False, "No fields provided to update.")

    # Append license_number last since it goes in the WHERE clause
    values.append(license_number)

    # Build the final query dynamically, e.g.:
    # UPDATE DRIVER SET full_name = %s, address = %s WHERE license_number = %s
    query = f"UPDATE DRIVER SET {', '.join(fields)} WHERE license_number = %s"

    try:
        cursor.execute(query, values)
        connection.commit()

        # rowcount tells us how many rows were actually changed
        # If 0, the license number didn't match any record
        if cursor.rowcount == 0:
            return (False, "No driver found with that license number.")
        return (True, "Driver updated successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def delete_driver(connection, license_number):
    """
    Deletes a driver record from the DRIVER table by license number.

    Important: This will FAIL if the driver has linked vehicles or violations
    in the database (foreign key constraint). You must delete those records
    first, or handle the cascade in the database schema.

    Parameters:
        connection     - the active MariaDB connection object
        license_number - the license number of the driver to delete

    Returns:
        (True,  "Driver deleted successfully.")              — if delete worked
        (False, "No driver found with that license number.") — if no match found
        (False, error_message)                               — if a database error occurred
                                                               (e.g. foreign key violation)
    """
    cursor = connection.cursor()
    query = "DELETE FROM DRIVER WHERE license_number = %s"

    try:
        cursor.execute(query, (license_number,))    # The comma makes it a tuple (required by the library)
        connection.commit()

        # If no rows were deleted, the license number didn't exist
        if cursor.rowcount == 0:
            return (False, "No driver found with that license number.")
        return (True, "Driver deleted successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def search_drivers(connection, keyword=None):
    """
    Retrieves driver records from the DRIVER table.
    - If no keyword is given, returns ALL drivers.
    - If a keyword is given, filters by license number OR full name (partial match).

    Parameters:
        connection - the active MariaDB connection object
        keyword    - (optional) search string, e.g. 'Juan' or 'N01-12'

    Returns:
        (True,  list_of_rows) — each row is a tuple of all DRIVER columns in order:
                                (license_number, full_name, date_of_birth, sex,
                                 address, license_type, license_status, issuance_date, expiration_date)
        (False, error_message) — if a database error occurred

    Example result:
        (True, [
            ('N01-12-123456', 'Jeremias Gomez', datetime(1995,5,15), 'M',
             'Los Baños, Laguna', 'Non-Professional', 'Valid', ...),
            ...
        ])
    """
    cursor = connection.cursor()

    try:
        if keyword:
            # LIKE %keyword% means "contains keyword anywhere in the value"
            query = """
                SELECT license_number, full_name, date_of_birth, sex,
                       address, license_type, license_status, issuance_date, expiration_date
                FROM DRIVER
                WHERE license_number LIKE %s OR full_name LIKE %s
            """
            like = f"%{keyword}%"           # Wrap keyword with % for partial matching
            cursor.execute(query, (like, like))
        else:
            # No keyword — fetch everything
            query = """
                SELECT license_number, full_name, date_of_birth, sex,
                       address, license_type, license_status, issuance_date, expiration_date
                FROM DRIVER
            """
            cursor.execute(query)

        rows = cursor.fetchall()            # Get all matching rows as a list of tuples
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()