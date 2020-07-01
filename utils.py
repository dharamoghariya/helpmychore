from app.extensions import db_object
import datetime
import flask

global database_conn
database_conn = None

def make_response(status, msg):
    return flask.jsonify(msg), status


def get_utc_timestamp_now():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def get_database_connection():
    if database_conn is None:
        database_conn, cur = db_object.get_db_connection()
    else:
        return database_conn
