#db_connection.py - handles database connection to mariadb

import mysql.connector
from config import db_config

def get_connection():
    #opens and returns a new mariadb connection using credentials from db_config
    connection = mysql.connector.connect(
        host=db_config.DB_HOST,
        port=db_config.DB_PORT,
        database=db_config.DB_NAME,
        user=db_config.DB_USER,
        password=db_config.DB_PASSWORD,
        autocommit=False,
        connection_timeout=300
    )
    return connection

def close_connection(connection):
    #closes the connection if still open
    if connection.is_connected():
        connection.close()

def get_cursor(connection):
    #returns a cursor from the given connection
    return connection.cursor()
