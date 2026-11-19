from flask import Flask

from src.core.logger import setup_logger
from src.core.db import db
from src.core.http_client import http
from src.core.errors import register_errors
from src.utils.serial import JSONExtendProvider
from src.routes import register_routes


def create_app():
    app = Flask(
        __name__,
        static_folder=None,
        template_folder=None
    )

    app.json = JSONExtendProvider(app)

    app.json.ensure_ascii = False
    app.json.sort_keys = False  # key 不按字母序重排

    setup_logger()
    register_errors(app)
    register_routes(app)

    db.init()
    http.init()

    return app
