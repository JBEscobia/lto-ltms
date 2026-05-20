#vehicle.py - crud operations for the VEHICLE table

def add_vehicle(connection, plate_number, license_number, engine_number,
                chassis_number, vehicle_type, make, model, year_model, color):
    #inserts a new vehicle record
    cursor = connection.cursor()
    query = """
        INSERT INTO VEHICLE (
            plate_number, license_number, engine_number, chassis_number,
            vehicle_type, make, model, year_model, color
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (plate_number, license_number, engine_number, chassis_number,
              vehicle_type, make, model, year_model, color)
    try:
        cursor.execute(query, values)
        connection.commit()
        return (True, "Vehicle added successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def update_vehicle(connection, plate_number, license_number=None, engine_number=None,
                   chassis_number=None, vehicle_type=None, make=None, model=None,
                   year_model=None, color=None):
    #updates fields of an existing vehicle; only non-None fields are changed
    cursor = connection.cursor()

    fields = []
    values = []

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

    if not fields:
        return (False, "No fields provided to update.")

    values.append(plate_number)
    query = f"UPDATE VEHICLE SET {', '.join(fields)} WHERE plate_number = %s"

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            return (False, "No vehicle found with that plate number.")
        return (True, "Vehicle updated successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def delete_vehicle(connection, plate_number):
    #deletes a vehicle by plate number; fails if there are linked registrations/violations
    cursor = connection.cursor()
    query = "DELETE FROM VEHICLE WHERE plate_number = %s"
    try:
        cursor.execute(query, (plate_number,))
        connection.commit()
        if cursor.rowcount == 0:
            return (False, "No vehicle found with that plate number.")
        return (True, "Vehicle deleted successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def search_vehicles(connection, keyword=None):
    #returns all vehicles, or filters by plate number / make / model if keyword is given
    cursor = connection.cursor()
    try:
        if keyword:
            query = """
                SELECT plate_number, license_number, engine_number, chassis_number,
                       vehicle_type, make, model, year_model, color
                FROM VEHICLE
                WHERE plate_number LIKE %s
                   OR make LIKE %s
                   OR model LIKE %s
            """
            like = f"%{keyword}%"
            cursor.execute(query, (like, like, like))
        else:
            query = """
                SELECT plate_number, license_number, engine_number, chassis_number,
                       vehicle_type, make, model, year_model, color
                FROM VEHICLE
            """
            cursor.execute(query)

        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()
