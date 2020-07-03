from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

main_page = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


@main_page.route("/")
def main():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        abort(404)


@main_page.route("/signup")
def signup_page():
    try:
        return render_template("signup.html")
    except TemplateNotFound:
        abort(404)


@main_page.route("/login")
def login_page():
    try:
        return render_template("login.html")
    except TemplateNotFound:
        abort(404)


@main_page.route("/requests")
def requests_page():
    try:
        return render_template("requests.html")
    except TemplateNotFound:
        abort(404)


@main_page.route("/request-volunteer")
def request_volunteer_page():
    try:
        return render_template("create_request.html")
    except TemplateNotFound:
        abort(404)
