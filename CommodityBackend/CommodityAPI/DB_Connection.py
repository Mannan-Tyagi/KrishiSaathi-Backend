from dotenv import load_dotenv
import mysql.connector
import os

# Load environment variables from .env file
load_dotenv()

class DBConnection:
    keyword = os.getenv('DB_KEYWORD')
    print(f"DB_KEYWORD: {keyword}")

    @classmethod
    def database_connection(cls):
        if cls.keyword == "Azure":
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_config = {
                'host': os.getenv('AZURE_DB_HOST'),
                'user': os.getenv('AZURE_DB_USER'),
                'password': os.getenv('AZURE_DB_PASSWORD'),
                'database': os.getenv('AZURE_DB_NAME'),
                'client_flags': [mysql.connector.ClientFlag.SSL],
                'ssl_ca': os.path.join(BASE_DIR, 'certificates', os.getenv('AZURE_DB_SSL_CA'))
            }
            print("Azure DB Config:", db_config)
        else:
            db_config = {
                'host': os.getenv('LOCAL_DB_HOST'),
                'user': os.getenv('LOCAL_DB_USER'),
                'password': os.getenv('LOCAL_DB_PASSWORD'),
                'database': os.getenv('LOCAL_DB_NAME')
            }
            print("Local DB Config:", db_config)
        
        # CONNECTING TO DATABASE
        try:
            connection = mysql.connector.connect(**db_config)
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None