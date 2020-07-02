from app import utils
import flask
import os

REQUEST_API = flask.Blueprint(f"API_{os.environ.get('VERSION')}_REQUEST_OPS", __name__)


@REQUEST_API.route("/submit_requests", methods=["POST"])
def submit_request():
    """
    Submit requests to get help.

    Request: application/json
        request_type str
            Type of the request. Currently only grocery type is supported.
        request_information string
            Things to be brought at the grocery. This is more like a list or can be
            text. But it is preffered that it is a list to keep it short and concise.
        request_notes string (optional)
            Additional notes pertaining to request.
        request_id int
            Id of the requester sending the request.
        volunteer_id int (optional)
            Volunteer Id picking up the request
        tokens int
            Number of tokens awarded for completing the request
    """
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
        f"'{data.get('is_completed', 'false')}', '{timestamp}', '{timestamp}') RETURNING request_id"
    )
    cursor.execute(request_query)
    request_id = cursor.fetchone()[0]

    transaction_table_update = (
        "UPDATE token_transactions"
        f"SET request_id={request_id} WHERE transaction_id={transaction_id}"
    )
    cursor.execute(transaction_table_update)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route("/get_requests", methods=["POST"])
def get_requests():
    """
    Given voluteer_id fetch list of requests that would be suitable for him to do.
    This is done using special matching algorithm which would use FSA (first 3 digits of Postal Code) of the voluntter and requester to determine their proximity. Currently the algorithm
    would only match the people having same FSA.

    Request: application/json
        volunteer_id int
            Volunteer ID for whom the matching requests are to be found.
    """
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


@REQUEST_API.route("/get_request_content", methods=["POST"])
def get_request_content():
    """
    Fetch content of the request.

    Request: application/json
        request_id int
            Request ID for which the content is to be fetched
    """
    data = flask.request.get_json()
    _, cursor = utils.get_database_connection()
    request_fetch_query = (
        f"SELECT * FROM request_details WHERE request_id={data['request_id']}"
    )

    cursor.execute(request_fetch_query)
    request_data = cursor.fetchall()
    return utils.make_response(request_data, 200)


@REQUEST_API.route('/fetch_all_requests')
def fetch_all_requests():
    """
    Fetch all requests submitted by a requester.

    Request: application/json
        requester_id int
            Requester ID for whom the requests are to be fetched
    """
    data = flask.request.get_json()
    _, cursor = utils.get_database_connection()
    request_fetch_query = (
        f"SELECT * FROM request_details WHERE requester_id={data['requester_id']}"
    )

    cursor.execute(request_fetch_query)
    request_data = cursor.fetchall()
    return utils.make_response(request_data, 200)


@REQUEST_API.route('/fetch_active_requests_requester')
def fetch_active_requests_requester():
    """
    Fetch all active requests of the requester.

    Request: application/json
        requester_id int
            Requester ID for whom the active requests are to be fetched.
    """
    data = flask.request.get_json()
    _, cursor = utils.get_database_connection()
    request_fetch_query = (
        f"SELECT * FROM request_details WHERE requester_id={data['requester_id']} "
        "AND is_completed=false"
    )

    cursor.execute(request_fetch_query)
    request_data = cursor.fetchall()
    return utils.make_response(request_data, 200)


@REQUEST_API.route('/fetch_volunteer_requests')
def fetch_volunteer_requests():
    """
    Fetch all requests taken or completed by a volunteer.

    Request: application/json
        volunteer_id int
            Volunteer ID for whom the requests are to be fetched
    """
    data = flask.request.get_json()
    _, cursor = utils.get_database_connection()
    request_fetch_query = (
        f"SELECT * FROM request_details WHERE volunteer_id={data['volunteer_id']}"
    )

    cursor.execute(request_fetch_query)
    request_data = cursor.fetchall()
    return utils.make_response(request_data, 200)


@REQUEST_API.route('/fetch_active_volunteer_request')
def fetch_active_volunteer_request():
    """
    Fetch all active requests of the voluteer.

    Request: application/json
        volunteer_id int
            Volunteer ID for whom the active requests are to be fetched.
    """
    data = flask.request.get_json()
    _, cursor = utils.get_database_connection()
    request_fetch_query = (
        f"SELECT * FROM request_details WHERE volunteer_id={data['volunteer_id']} "
        "AND is_completed=false"
    )

    cursor.execute(request_fetch_query)
    request_data = cursor.fetchall()
    return utils.make_response(request_data, 200)


@REQUEST_API.route("/cancel_request")
def cancel_requests():
    """
    Cancle the submitted request.

    Request: application/json
        request_id int
            Request ID to be cancelled.
    """
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    transaction_update_query = f"DELETE FROM token_transactions WHERE request_id = {data['request_id']} RETURNING tokens"
    cursor.execute(transaction_update_query)
    tokens = cursor.fetchone()[0]

    request_update_query = (
        "UPDATE request_details "
        f"SET is_cancelled='true', updated_at='{timestamp}'"
        f"WHERE request_id = {data['request_id']} RETURNING requester_id"
    )
    cursor.execute(request_update_query)
    requester_id = cursor.fetchone()[0]

    token_update_query = f"UPDATE requester_details SET tokens=tokens+{tokens} WHERE requester_id = {requester_id}"
    cursor.execute(token_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@REQUEST_API.route("/commenced_request")
def commenced_requests():
    """
    Commence a request. This feature would be used by the volunteer.

    Request: application/json
        request_id int
            Request ID which is to be commenced.
    """
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


@REQUEST_API.route("/completed_request")
def completed_requests():
    """
    Complete a request. This feature would be used by the volunteer.

    Request: application/json
        request_id int
            Request ID which is to be complete.
    """
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


@REQUEST_API.route("/assign_request")
def assign_requests():
    """
    Assign a request. This feature would be used by the volunteer.

    Request: application/json
        request_id int
            Request ID which is to be Assigned.
    """
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


@REQUEST_API.route("/unassign_request")
def unassign_requests():
    """
    Unassign a request. This feature would be used by the volunteer.

    Request: application/json
        request_id int
            Request ID which is to be Unassigned.
    """
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


@REQUEST_API.route("/modify_request_details")
def modify_requests():
    """
    Modify a request. This feature would be used by the requester.

    Request: application/json
        request_id int
            Request ID which is to be Assigned.
        request_information str
            Modified content of the request
        request_note str
            Note associated with a request
        tokens str
            Tokens associated with a request
    """
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

    if "tokens" in data:
        token_update_query = (
            "UPDATE token_transactions"
            f"SET tokens={data['tokens']}, updated_at='{timestamp}' "
            f"WHERE request_id= {data['request_id']}"
        )
        cursor.execute(token_update_query)
    conn.commit()
    return utils.make_response("{error: None}", 200)
