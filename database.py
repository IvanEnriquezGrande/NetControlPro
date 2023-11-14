import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConnectionError(Exception):
    def __init__(self, host, port, message):
        self.message = f"Error de conexión en la base de datos en {host}:{port}. \
            Error: {message}"
        super().__init__(self.message)

def conectar_db():
    try:
        conn = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_DATABASE'),
            port = os.getenv('DB_PORT')
        )
        return conn
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(os.getenv('DB_HOST'), os.getenv('DB_PORT'), str(e))
