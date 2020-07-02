from app import utils
import flask
import os

TOKEN_API = flask.Blueprint(f"API_{os.environ.get('VERSION')}_TOKEN_OPS", __name__)


@TOKEN_API.route("/buy_token_request")
def buy_token_request():
    """
    Buy tokens for a given requester_id.

    Request: application/json
        requester_id int
            Requester ID who is buying the tokens
        tokens int
            Number of tokens bought by the requester
    """
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    token_update_query = (
        "UPDATE requester_details"
        f"SET tokens = tokens+{data['tokens']}, updated_at='{timestamp}' "
        f"WHERE requester_id={data['requester_id']}"
    )
    cursor.execute(token_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@TOKEN_API.route("/refund_token_request")
def refund_token_request():
    """
    Refund tokens for a given requester_id.

    Request: application/json
        requester_id int
            Requester ID who is requesting refund of the tokens
        tokens int
            Number of tokens refunded to requester
    """
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    token_update_query = (
        "UPDATE requester_details"
        f"SET tokens = tokens-{data['tokens']}, updated_at='{timestamp}' "
        f"WHERE requester_id={data['requester_id']}"
    )
    cursor.execute(token_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)
