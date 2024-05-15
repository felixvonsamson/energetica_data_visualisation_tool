"""
This code is run once at the start of the game
"""

import socket
from flask import Flask  # noqa: E402

from website.gameEngine import gameEngine  # noqa: E402


def create_app():
    # gets lock to avoid multiple instances
    lock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    lock.bind("\0energetica")

    # creates the app :
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ksdfzrtbftufdun unfdnzuidnihsf98ERf"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    # creates the engine (ad loading the sava if it exists)
    engine = gameEngine()
    app.config["engine"] = engine

    # add blueprints (website repositories) :
    from .views import views, overviews
    from .api.http import http

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(overviews, url_prefix="/production_overview")
    app.register_blueprint(http, url_prefix="/")

    return app
