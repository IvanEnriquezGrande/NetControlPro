import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def conectar_db():
    return mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_DATABASE'),
        port = os.getenv('DB_PORT')
    )
