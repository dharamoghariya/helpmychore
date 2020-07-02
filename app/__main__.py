import os
import sys

sys.path.append(os.getcwd())

from app import app
from app import user_transactions
from app import request_transactions
from app import health_transactions
from app import token_transactions
from app.views.base import main_page

from app import login_manager

# @app.route('/')
# def index() -> str:
#     return "Welcome to COVID-19 Personal API Service!"

if __name__ == "__main__":
    app.register_blueprint(health_transactions.HEALTH_API)
    app.register_blueprint(request_transactions.REQUEST_API)
    app.register_blueprint(token_transactions.TOKEN_API)
    app.register_blueprint(user_transactions.AUTH)
    app.register_blueprint(main_page)
    login_manager.init_app(app)
    app.run(host="0.0.0.0", debug=True)
