#driver.py - crud operations for the DRIVER table

def add_driver(connection, license_number, full_name, date_of_birth, sex,
               address, license_type, license_status, issuance_date, expiration_date):
    #inserts a new driver record
    cursor = connection.cursor()
    query = """
        INSERT INTO DRIVER (
            license_number, full_name, date_of_birth, sex,
            address, license_type, license_status, issuance_date, expiration_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (license_number, full_name, date_of_birth, sex,
              address, license_type, license_status, issuance_date, expiration_date)
    try:
        cursor.execute(query, values)
        connection.commit()
        return (True, "Driver added successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def update_driver(connection, license_number, full_name=None, date_of_birth=None,
                  sex=None, address=None, license_type=None, license_status=None,
                  issuance_date=None, expiration_date=None):
    #updates fields of an existing driver; only non-None fields are changed
    cursor = connection.cursor()

    fields = []
    values = []

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

    if not fields:
        return (False, "No fields provided to update.")

    values.append(license_number)
    query = f"UPDATE DRIVER SET {', '.join(fields)} WHERE license_number = %s"

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            return (False, "No driver found with that license number.")
        return (True, "Driver updated successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def delete_driver(connection, license_number):
    #deletes a driver by license number; fails if there are linked vehicles/violations
    cursor = connection.cursor()
    query = "DELETE FROM DRIVER WHERE license_number = %s"
    try:
        cursor.execute(query, (license_number,))
        connection.commit()
        if cursor.rowcount == 0:
            return (False, "No driver found with that license number.")
        return (True, "Driver deleted successfully.")
    except Exception as e:
        connection.rollback()
        return (False, str(e))
    finally:
        cursor.close()


def search_drivers(connection, keyword=None):
    #returns all drivers, or filters by license number / name if keyword is given
    cursor = connection.cursor()
    try:
        if keyword:
            query = """
                SELECT license_number, full_name, date_of_birth, sex,
                       address, license_type, license_status, issuance_date, expiration_date
                FROM DRIVER
                WHERE license_number LIKE %s OR full_name LIKE %s
            """
            like = f"%{keyword}%"
            cursor.execute(query, (like, like))
        else:
            query = """
                SELECT license_number, full_name, date_of_birth, sex,
                       address, license_type, license_status, issuance_date, expiration_date
                FROM DRIVER
            """
            cursor.execute(query)

        rows = cursor.fetchall()
        return (True, rows)
    except Exception as e:
        return (False, str(e))
    finally:
        cursor.close()
