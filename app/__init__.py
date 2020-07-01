from dotenv import load_dotenv
from flask import Flask
import os

def config(app):
    load_dotenv()
    app.config['DEBUG']=False
    app.config['TESTING']=False

app = Flask(__name__)
config(app)