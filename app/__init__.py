from dotenv import load_dotenv
from flask import Flask
import flask_login
import os


def config(app):
    load_dotenv()
    app.config["DEBUG"] = False
    app.config["TESTING"] = False
    app.config[
        "secret_key"
    ] = "u055scvqlehhy39ysioieyd8tq868e3kwadkr1ugkro16izchioqg867vn94n682"


app = Flask(__name__)
login_manager = flask_login.LoginManager()
config(app)
