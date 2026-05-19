# =============================================================================
# db_connection.py
# =============================================================================
# PURPOSE:
#   This file is the single place where the app connects to and disconnects
#   from the MariaDB database. No other file should call mysql.connector
#   directly — they all go through this file instead.
#
# HOW IT FITS IN THE PROJECT:
#   db_config.py  →  db_connection.py  →  driver.py, vehicle.py, reports.py, main.py
#   (credentials)     (connection)         (all use the connection object)
#
# HOW TO USE IT IN YOUR FILES:
#   from app import db_connection
#
#   conn = db_connection.get_connection()   # open connection
#   # ... pass conn into your driver/vehicle/report functions ...
#   db_connection.close_connection(conn)    # close when done
#
# NOTE:
#   This is a temporary working version for local testing.
#   JB owns and will finalize this file — do not commit it to Git.
# =============================================================================

import mysql.connector      # The library that lets Python talk to MariaDB
                            # Installed via: pip install mysql-connector-python

from config import db_config  # Imports DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
                               # from config/db_config.py (your local credentials file)
                               # db_config.py is gitignored — everyone has their own copy


# -----------------------------------------------------------------------------
# get_connection()
# -----------------------------------------------------------------------------
# What it does:
#   Opens a new connection to the MariaDB database using the credentials
#   stored in db_config.py. Think of this like "logging in" to the database.
#
# When to call it:
#   At the START of any operation that needs the database.
#   Typically called once in main.py when the app starts up.
#
# Returns:
#   A connection object — pass this into all your driver/vehicle/report functions.
#
# Raises:
#   An exception if the connection fails. Common causes:
#     - MariaDB service is not running
#     - Wrong password in db_config.py
#     - Wrong database name or user
#
# Example:
#   conn = get_connection()
#   # conn is now ready to use
# -----------------------------------------------------------------------------
def get_connection():
    connection = mysql.connector.connect(
        host=db_config.DB_HOST,         # e.g. "localhost"
        port=db_config.DB_PORT,         # e.g. 3306 (MariaDB default port)
        database=db_config.DB_NAME,     # e.g. "lto_ims"
        user=db_config.DB_USER,         # e.g. "lto_user"
        password=db_config.DB_PASSWORD,  # e.g. "pass1234"
        autocommit=True,                      # Automatically save changes without needing connection.commit()
        connection_timeout=300               # Wait up to 5 minutes for the connection to succeed before giving up
    )
    return connection


# -----------------------------------------------------------------------------
# close_connection(connection)
# -----------------------------------------------------------------------------
# What it does:
#   Closes an open database connection. Think of this like "logging out".
#   Always close the connection when you're done — leaving connections open
#   wastes database resources and can cause issues over time.
#
# When to call it:
#   At the END of any operation, or when the app is about to exit.
#   Typically called once in main.py when the user chooses to quit.
#
# Parameters:
#   connection — the connection object returned by get_connection()
#
# Returns:
#   Nothing. Just closes the connection silently.
#
# Example:
#   close_connection(conn)
#   # conn is now closed and can no longer be used
# -----------------------------------------------------------------------------
def close_connection(connection):
    if connection.is_connected():   # Only close if it's actually still open
        connection.close()          # Frees up the database connection slot


# -----------------------------------------------------------------------------
# get_cursor(connection)
# -----------------------------------------------------------------------------
# What it does:
#   Creates and returns a cursor from an active connection.
#   A cursor is the object you use to actually run SQL queries.
#   Think of the connection as the "phone line" and the cursor as the
#   "person speaking" — you need both to get anything done.
#
# When to call it:
#   Inside any function that needs to run a SQL query.
#   Each function in driver.py, vehicle.py, etc. calls this at the start.
#
# Parameters:
#   connection — the connection object returned by get_connection()
#
# Returns:
#   A cursor object. Use cursor.execute(query, values) to run queries.
#   Always call cursor.close() when done with it (the finally block handles this).
#
# Example:
#   cursor = get_cursor(conn)
#   cursor.execute("SELECT * FROM DRIVER")
#   rows = cursor.fetchall()
#   cursor.close()
# -----------------------------------------------------------------------------
def get_cursor(connection):
    return connection.cursor()