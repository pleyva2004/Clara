import mysql.connector
from mysql.connector import Error

def get_connection(servername, username, password, dbname):
    try:
        # Establishing the connection
        conn = mysql.connector.connect(
            host=servername,
            user=username,
            password=password,
            database=dbname
        )
        if conn.is_connected():
            print("CONNECTED")
    except Error as e:
        print(f"Failed to connect to MySQL: {e}")
    finally:
        # Closing the connection
        if 'conn' in locals() and conn.is_connected():
            conn.close()