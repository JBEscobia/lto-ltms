# vehicle.py
# Handles all vehicle-related database operations.
#
# Rule: Functions here only RETURN data — no print() or input() allowed.
# All printing and user prompts happen in main.py only.
#
# All functions follow the same return pattern:
#   (True,  result)        — operation succeeded; result is a message or list of rows
#   (False, error_message) — operation failed; error_message explains why
#
# VEHICLE table columns (in order):
#   plate_number   VARCHAR(20)  — PRIMARY KEY, e.g. 'ABC-1234'
#   license_number VARCHAR(50)  — FOREIGN KEY → DRIVER(license_number)
#   engine_number  VARCHAR(50)  — UNIQUE, e.g. 'ENG98765'
#   chassis_number VARCHAR(50)  — UNIQUE, e.g. 'CHAS12345'
#   vehicle_type   VARCHAR(50)  — e.g. 'Private Car', 'Motorcycle'
#   make           VARCHAR(50)  — e.g. 'Toyota', 'Honda'
#   model          VARCHAR(50)  — e.g. 'Vios', 'Click'
#   year_model     INT(4)       — e.g. 2020
#   color          VARCHAR(30)  — e.g. 'Red'


def add_vehicle(connection, plate_number, license_number, engine_number,
                chassis_number, vehicle_type, make, model, year_model, color):
    """
    Inserts a brand new vehicle into the VEHICLE table.

    Parameters:
        connection     - the active MariaDB connection object (from db_connection.py)
        plate_number   - e.g. 'ABC-1234' (primary key, must be unique)
        license_number - the license number of the driver who owns this vehicle
                         must already exist in the DRIVER table (foreign key)
        engine_number  - e.g. 'ENG98765' (must be unique across all vehicles)
        chassis_number - e.g. 'CHAS12345' (must be unique across all vehicles)
        vehicle_type   - e.g. 'Private Car', 'Public Utility Vehicle', 'Motorcycle'
        make           - brand/manufacturer, e.g. 'Toyota', 'Honda', 'Isuzu'
        model          - e.g. 'Vios', 'Click', 'Crosswind'
        year_model     - 4-digit year, e.g. 2020
        color          - e.g. 'Red', 'White', 'Black'

    Returns:
        (True,  "Vehicle added successfully.")  — if insert worked
        (False, error_message)                  — if something went wrong, e.g.:
                                                  - plate_number already exists
                                                  - engine_number or chassis_number not unique
                                                  - license_number doesn't exist in DRIVER table

    Example usage in main.py:
        success, message = add_vehicle(conn, 'DEF-5678', 'N01-12-123456',
                                       'ENG00001', 'CHAS00001', 'Private Car',
                                       'Mitsubishi', 'Mirage', 2022, 'Blue')
        print(message)
    """
    cursor = connection.cursor()

    # %s placeholders are filled in safely by mysql-connector (prevents SQL injection)
    query = """
        INSERT INTO VEHICLE (
            plate_number, license_number, engine_number, chassis_number,
            vehicle_type, make, model, year_model, color
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (plate_number, license_number, engine_number, chassis_number,
              vehicle_type, make, model, year_model, color)

    try:
        cursor.execute(query, values)   # Run the INSERT statement
        connection.commit()             # Save changes to the database permanently
        return (True, "Vehicle added successfully.")
    except Exception as e:
        connection.rollback()           # Undo any partial changes if something failed
        return (False, str(e))
    finally:
        cursor.close()                  # Always release the cursor to free up resources


def update_vehicle(connection, plate_number, license_number=None, engine_number=None,
                   chassis_number=None, vehicle_type=None, make=None, model=None,
                   year_model=None, color=None):
    """
    Updates an existing vehicle's information in the VEHICLE table.
    Only the fields you pass in will be updated — fields left as None are skipped.
    This means you only need to provide the fields you want to change.

    Parameters:
        connection     - the active MariaDB connection object
        plate_number   - the vehicle to update (used in the WHERE clause, cannot be changed)
        license_number - (optional) new owner's license number (must exist in DRIVER table)
        engine_number  - (optional) new engine number (must remain unique)
        chassis_number - (optional) new chassis number (must remain unique)
        vehicle_type   - (optional) new vehicle type
        make           - (optional) new make/brand
        model          - (optional) new model
        year_model     - (optional) new year model
        color          - (optional) new color

    Returns:
        (True,  "Vehicle updated successfully.")           — if update worked
        (False, "No vehicle found with that plate number.") — if plate number doesn't exist
        (False, "No fields provided to update.")           — if no fields were passed in
        (False, error_message)                             — if a database error occurred

    Example usage in main.py:
        # Only updating the color and year — everything else stays the same
        success, message = update_vehicle(conn, 'ABC-1234', color='Blue', year_model=2023)
        print(message)
    """
    cursor = connection.cursor()

    # Dynamically build the SET clause — only include fields that were actually provided
    fields = []     # Holds strings like "color = %s", "make = %s"
    values = []     # Holds the actual new values in the same order as fields

    if license_number is not None:
        fields.append("license_number = %s")
        values.append(license_number)
    if engine_number is not None:
        fields.append("engine_number = %s")
        values.append(engine_number)
    if chassis_number is not None:
        fields.append("chassis_number = %s")
        values.append(chassis_number)
    if vehicle_type is not None:
        fields.append("vehicle_type = %s")
        values.append(vehicle_type)
    if make is not None:
        fields.append("make = %s")
        values.append(make)
    if model is not None:
        fields.append("model = %s")
        values.append(model)
    if year_model is not None:
        fields.append("year_model = %s")
        values.append(year_model)
    if color is not None:
        fields.append("color = %s")
        values.append(color)

    # If the caller didn't pass any fields to update, return early
    if not fields:
        return (False, "No fields provided to update.")

    # plate_number goes at the end — it's used in the WHERE clause, not the SET clause
    values.append(plate_number)

    # Build the final query, e.g.:
    # UPDATE VEHICLE SET color = %s, year_model = %s WHERE plate_number = %s
    query = f"UPDATE VEHICLE SET {', '.join(fields)} WHERE plate_number = %s"

    try:
        cursor.execute(query, values)
        connection.commit()

        # rowcount = number of rows actually changed
        # If 0, no vehicle matched the plate number
        if cursor.rowcount == 0:
            return (False, "No vehicle found with that plate number.")
        return (True, "Vehicle updated successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def delete_vehicle(connection, plate_number):
    """
    Deletes a vehicle record from the VEHICLE table by plate number.

    Important: This will FAIL if the vehicle has linked registration or violation
    records in the database (foreign key constraint). Those records must be
    deleted first before the vehicle can be removed.

    Parameters:
        connection   - the active MariaDB connection object
        plate_number - the plate number of the vehicle to delete, e.g. 'ABC-1234'

    Returns:
        (True,  "Vehicle deleted successfully.")            — if delete worked
        (False, "No vehicle found with that plate number.") — if no match found
        (False, error_message)                              — if a database error occurred
                                                              (e.g. foreign key violation from
                                                               linked registration/violation records)

    Example usage in main.py:
        success, message = delete_vehicle(conn, 'ABC-1234')
        print(message)
    """
    cursor = connection.cursor()
    query = "DELETE FROM VEHICLE WHERE plate_number = %s"

    try:
        cursor.execute(query, (plate_number,))  # The trailing comma makes it a tuple
        connection.commit()                     # required by mysql-connector for parameters

        # If no rows were deleted, the plate number didn't exist
        if cursor.rowcount == 0:
            return (False, "No vehicle found with that plate number.")
        return (True, "Vehicle deleted successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def search_vehicles(connection, keyword=None):
    """
    Retrieves vehicle records from the VEHICLE table.
    - If no keyword is given, returns ALL vehicles.
    - If a keyword is given, filters by plate number, make, or model (partial match).

    Parameters:
        connection - the active MariaDB connection object
        keyword    - (optional) search string, e.g. 'Toyota', 'ABC', 'Motor'

    Returns:
        (True,  list_of_rows)  — each row is a tuple of all VEHICLE columns in order:
                                 (plate_number, license_number, engine_number, chassis_number,
                                  vehicle_type, make, model, year_model, color)
        (False, error_message) — if a database error occurred

    Example usage in main.py:
        success, rows = search_vehicles(conn, keyword='Toyota')
        if success:
            for row in rows:
                print(row)
        else:
            print(rows)   # rows contains the error message in this case

    Example result:
        (True, [
            ('ABC-1234', 'N01-12-123456', 'ENG98765', 'CHAS12345',
             'Private Car', 'Toyota', 'Vios', 2020, 'Red'),
            ...
        ])
    """
    cursor = connection.cursor()

    try:
        if keyword:
            # LIKE %keyword% matches anything that contains the keyword anywhere
            # Searching across plate_number, make, and model for flexibility
            query = """
                SELECT plate_number, license_number, engine_number, chassis_number,
                       vehicle_type, make, model, year_model, color
                FROM VEHICLE
                WHERE plate_number LIKE %s
                   OR make LIKE %s
                   OR model LIKE %s
            """
            like = f"%{keyword}%"                       # e.g. keyword='Toyota' becomes '%Toyota%'
            cursor.execute(query, (like, like, like))   # passed 3 times, one for each LIKE
        else:
            # No keyword — return everything in the table
            query = """
                SELECT plate_number, license_number, engine_number, chassis_number,
                       vehicle_type, make, model, year_model, color
                FROM VEHICLE
            """
            cursor.execute(query)

        rows = cursor.fetchall()    # Retrieve all matching rows as a list of tuples
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()