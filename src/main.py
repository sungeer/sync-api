from flask import Flask

from src.core.logger import setup_logger
from src.core.db import db
from src.core.http_client import http
from src.utils.serial import JSONExtendProvider
from src.routes import register_routes


def create_app():
    app = Flask('hostess')

    app.json = JSONExtendProvider(app)

    app.json.ensure_ascii = False

    setup_logger()
    register_routes(app)

    db.init()
    http.init()

    return app
