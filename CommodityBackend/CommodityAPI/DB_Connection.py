import mysql.connector
import os

class DBConnection:
    @classmethod
    def database_connection(cls):
        # Database configuration
        db_config = {
            'user': 'root',       # Replace with your MySQL username
            'password': 'admin',   # Replace with your MySQL password
            'host': 'localhost',   # Replace with your MySQL host
            'database': 'commoditydataanaylsis'  # Replace with your MySQL database name
        }

        try:
            # Try to establish the connection
            connection = mysql.connector.connect(**db_config)
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
