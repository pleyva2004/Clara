import mysql.connector
from mysql.connector import Error
# Connect to the database otherwise return None
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
            return conn
    except Error as e:
        print(f"Failed to connect to MySQL: {e}")
        return None