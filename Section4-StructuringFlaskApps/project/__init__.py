from flask import Flask

from .extensions import db
from .routes import main

# application factory pattern
def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()# use the from_prefixed_env method to load configuration values from environment variables that start with a specific prefix, this is a convenient way to manage configuration values in different environments (development, testing, production) without having to hardcode them in the codebase

    db.init_app(app)

    app.register_blueprint(main)

    return app