import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        user=os.environ.get('DB_USER'),
        password = os.environ.get('DB_PASSWORD'),
        host = os.environ.get('DB_SERVER'),
        port = os.environ.get('DB_PORT'),
        database = os.environ.get('DATABASE_NAME')
    )
    return conn