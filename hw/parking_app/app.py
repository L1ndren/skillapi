from flask import Flask
from .extensions import db


def create_app(config=None):
    app = Flask(__name__)

    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///parking.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    if config:
        app.config.update(config)

    db.init_app(app)

    from .routes import init_routes
    init_routes(app)

    return app