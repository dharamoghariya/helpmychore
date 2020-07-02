from app.extensions import db_object
import datetime
import flask

global database_conn
global cursor
database_conn = None
cursor = None


def make_response(msg, status):
    return flask.jsonify(msg), status


def get_utc_timestamp_now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def get_database_connection():
    global database_conn
    if database_conn is None:
        database_conn, cursor = db_object.get_db_connection()
        return database_conn, database_conn.cursor()
    else:
        return database_conn, database_conn.cursor()
