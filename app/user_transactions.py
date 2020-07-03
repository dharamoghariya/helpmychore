from app import utils
from app import login_manager
from flask import request, redirect, url_for, Blueprint
import flask_login
import os
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

AUTH = Blueprint(f"API_{os.environ.get('VERSION')}_USER_OPS", __name__)


class User:
    pass


@login_manager.user_loader
def user_loader(username):
    """
    Userloader function for flask_login

    Arugments:
        username str
            Username of the user
    """
    user = User()
    user.id = username
    return user


# @login_manager.request_loader
# def request_loader(request):
#     """
#     Request loader function to help flask_login
#
#     request: application/json
#         username str
#             Username of the string
#         password str
#             Password of the user
#     """
#     data = request.get_json()
#     username = data['username']
#
#     _, cursor = utils.get_database_connection()
#     query = (
#         f"SELECT username, password FROM login_details WHERE username={data['username']}"
#     )
#     cursor.execute(query)
#     username, password = cursor.fetchone()
#
#     user = User()
#     user.id = username
#     user.is_authenticated = (generate_password_hash(data['password']) == password)
#     return user


@AUTH.route("/login_user", methods=["POST"])
def login():
    """
    Login the user

    Request: application/json
        username str
            Username of the user
        password str
            Password of the user
    """
    data = request.get_json()

    _, cursor = utils.get_database_connection()
    query = f"SELECT username, password FROM login_details WHERE username='{data['username']}'"
    cursor.execute(query)
    username, password = cursor.fetchone()
    if username == None:
        return utils.make_response("{error: User does not exist}", 404)

    if generate_password_hash(data["password"]) == password:
        user = User()
        user.id = username
        flask_login.login_user(user)
    return utils.make_response("{error: None}", 200)


@AUTH.route("/logout")
def logout():
    """
    Logout the user.
    """
    flask_login.logout_user()
    return redirect(url_for("pages.login_page"))


@AUTH.route("/signup_user", methods=["POST"])
def signup():
    """
    Sign up the user.

    Request: application/json
        username str
            Username of the user signing up. It has to be unique.
        password str
            Password of the user
        unitNo int
            Unit number of the user's address
        streetNo int
            Street number of the user's address
        streetName str
            Street name of the user's address
        additional str
            Additional infomration about user's address
        city str
            City of the user's address
        postalCode str
            Postal code of the user's address
        name str
            Name of the user
        email str
            Email of the user
        phone str
            Phone number of the user
        age int
            Age of the user
        medicalCondition boolean
            If the user has any medical condition.
    """
    data = request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    is_active = "true"

    password = generate_password_hash(data["password"])

    try:
        login_query = (
            "INSERT INTO login_details (username, password, is_active, created_at, updated_at)"
            f"VALUES ('{data['username']}', '{password}', {is_active}, '{timestamp}', "
            f"'{timestamp}') RETURNING login_id"
        )
        cursor.execute(login_query)
        login_id = cursor.fetchone()[0]

    except psycopg2.IntegrityError:
        message = f"{{error: Username {data['username']} is taken}}"
        return utils.make_response(message, 409)

    address_query = (
        "INSERT INTO address_dir (unit_no, street_number, street_name, additional_info, "
        "city, province, postal_code, login_id, created_at, updated_at) VALUES ("
        f"'{data.get('unitNo', 'NULL')}', '{data.get('streetNo', 'NULL')}',"
        f"'{data['streetName']}', '{data.get('additional', 'NULL')}', '{data['city']}', "
        f"'{data['province']}', '{data['postalCode']}', {login_id}, '{timestamp}', '{timestamp}')"
    )

    cursor.execute(address_query)

    if data["category"] == "Volunteer":
        query = (
            "INSERT INTO volunteer_details (volunteer_name, volunteer_email, volunteer_phone,"
            f"volunteer_age, login_id, created_at, updated_at) VALUES ('{data['name']}',"
            f"'{data['email']}', {data['phone']}, {data['age']}, {login_id}, "
            f"'{timestamp}', '{timestamp}')"
        )

        try:
            cursor.execute(query)
        except psycopg2.IntegrityError:
            message = f"{{error: Email {data['email']} is already in the system}}"
            return utils.make_response(message, 409)
    else:
        medical_condition = True if data["medicalCondition"] == "Yes" else False
        query = (
            "INSERT INTO requester_details (requester_name, requester_email, requester_phone, requester_age,"
            f"has_medical_condition, login_id, created_at, updated_at) VALUES ('{data['name']}', "
            f"'{data['email']}', '{data['phone']}', {data['age']}, {medical_condition}, "
            f"{login_id}, '{timestamp}', '{timestamp}')"
        )
        try:
            cursor.execute(query)
        except psycopg2.IntegrityError:
            message = f"{{error: Email {data['email']} is already in the system}}"
            return utils.make_response(message, 409)

    conn.commit()
    return utils.make_response("{error: None}", 200)
