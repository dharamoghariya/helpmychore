import psycopg2
import os


def get_db_connection():
    conn = psycopg2.connect(
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        host=os.environ.get("SERVER"),
        port=os.environ.get("PORT"),
        database=os.environ.get("DATABASE"),
    )
    return conn, conn.cursor()
