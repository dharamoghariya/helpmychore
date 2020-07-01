from app import utils
import flask
import os

REQUEST_API = flask.Blueprint(f"API_{os.environ.get('VERSION')}_REQUEST_OPS", __name__ )

@REQUEST_API.route('/submit_requests', methods=["POST"])
def submit_request():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()

    timestamp = utils.get_utc_timestamp_now()
    transaction_query = (
        "INSERT INTO token_transactions (volunteer_id, requester_id, request_id, tokens, "
        f"is_complete, created_at, updated_at) VALUES ({data.get('volunteer_id', None)}, "
        f"{data.get('requester_id', None)}, {data.get('request_id', None)}, {data['tokens']}, "
        f"'{data.get('is_complete', 'false')}', '{timestamp}', '{timestamp}') "
        "RETURNING transaction_id"
    )
    transaction_id = None
    cursor.execute(transaction_query)
    transaction_id = cursor.fetchone()[0]

    request_query = (
        "INSERT INTO request_details (request_date, request_type, request_information, "
        "request_note, requester_id, volunteer_id, transaction_id, is_cancelled, is_commenced, "
        f"is_completed, created_at, updated_at) VALUES ('{timestamp}', '{data['request_type']}', "
        f"'{data['request_information']}', '{data.get('request_note', 'NULL')}', "
        f"'{data['request_id']}', '{data.get('volunteer_id', 'NULL')}', {transaction_id}, "
        f"'{data.get('is_cancelled', 'false')}', '{data.get('is_commenced', 'false')}', "
        f"'{data.get('is_completed', 'false')}', '{timestamp}', '{timestamp}')"
    )
    cursor.execute(request_query)
    conn.commit()

    #TODO: Update request_id into transaction table.
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route('/get_requests', methods=["POST"])
def get_requests():
    data = flask.request.get_json()
    _, cursor = utils.get_database_connection()

    volunteer_postal_query = (
        "SELECT b.postal_code FROM volunteer_details as a "
        "INNER JOIN address_dir b ON a.login_id = b.login_id "
        f"WHERE a.volunteer_id = '{data['volunteer_id']}'"
    )
    cursor.execute(volunteer_postal_query)
    postal_code = cursor.fetchone()[0][:3]

    request_queries = (
        "SELECT a.request_id ,a.request_type, a.request_date, b.unit_no, b.street_number, "
        "b.street_name, b.city, b.postal_code, e.token FROM request_details as a"
        "INNER JOIN ("
            "SELECT c.requester_id, d.unit_no, d.street_number, d.street_name, d.city, "
            "d.postal_code FROM requester_details as c INNER JOIN address_dir as d "
            "ON c.login_id = d.login_id"
        ") as b ON a.requester_id = b.requester_id "
        "INNER JOIN token_transactions c ON a.transaction_id = c.transaction_id "
        f"WHERE LEFT(b.postal_code, 3) = {postal_code}"
    )
    cursor.execute(request_queries)
    requests_list = cursor.fetchall()
    return utils.make_response(requests_list, 200)


@REQUEST_API.route('/cancel_request')
def cancel_requests():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    transaction_update_query = (
        f"DELETE FROM token_transactions WHERE request_id = {data['request_id']} RETURNING tokens"
    )
    cursor.execute(transaction_update_query)
    tokens = cursor.fetchone()[0]

    request_update_query = (
        "UPDATE request_details "
        f"SET is_cancelled='true', updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']} RETURNING requester_id"
    )
    cursor.execute(request_update_query)
    requester_id = cursor.fetchone()[0]

    token_update_query = (
        f"UPDATE requester_details SET tokens=tokens+{tokens} WHERE requester_id = {requester_id}"
    )
    cursor.execute(token_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route('/commenced_request')
def commenced_requests():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    query = (
        "UPDATE request_details "
        f"SET is_commenced='true', updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']}"
    )
    cursor.execute(query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route('/completed_request')
def completed_requests():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    request_update_query = (
        "UPDATE request_details "
        f"SET is_completed='true', updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']}"
    )
    cursor.execute(request_update_query)

    transaction_update_query = (
        f"UPDATE token_transactions SET is_complete='true', updated_at='{timestamp}' "
        f"WHERE request_id={data['request_id']} RETURNING volunteer_id, tokens"
    )
    cursor.execute(transaction_update_query)
    volunteer_id, total_tokens = cursor.fetchone()

    volunteer_token_update_query = (
        f"UPDATE volunteer_details SET tokens = tokens+{total_tokens}, updated_at='{timestamp}' "
        f"WHERE volunteer_id={volunteer_id}"
    )
    cursor.execute(volunteer_token_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route('/assign_request')
def assign_requests():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    request_detail_update_query = (
        "UPDATE request_details "
        f"SET volunteer_id={data['volunteer_id']}, updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']}"
    )
    cursor.execute(request_detail_update_query)

    transaction_update_query = (
        "UPDATE token_transactions"
        f"SET volunteer_id={data['volunteer_id']}, updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']}"
    )
    cursor.execute(transaction_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route('/unassign_request')
def unassign_requests():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    request_detail_update_query = (
        "UPDATE request_details "
        f"SET volunteer_id='NULL', updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']}"
    )
    cursor.execute(request_detail_update_query)

    transaction_update_query = (
        "UPDATE token_transactions"
        f"SET volunteer_id='NULL', updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']}"
    )
    cursor.execute(transaction_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route('/modify_request_details')
def modify_requests():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    request_update_query = (
        "UPDATE request_details "
        f"SET request_information={data['request_information']}, "
        f"request_note='{data.get('request_note', 'NULL')}', "
        f"updated_at='{timestamp}' WHERE request_id = {data['request_id']}"
    )
    cursor.execute(request_update_query)

    if 'tokens' in data:
        token_update_query = (
            "UPDATE token_transactions"
            f"SET tokens={data['tokens']}, updated_at='{timestamp}' "
            f"WHERE request_id= {data['request_id']}"
        )
        cursor.execute(token_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)