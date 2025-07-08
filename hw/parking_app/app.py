from flask import Flask
from .extensions import db
from .routes import init_routes


def create_app(config=None):
    app = Flask(__name__)

    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///parking.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TESTING': config.get('TESTING', False) if config else False
    })

    if config:
        app.config.update(config)

    db.init_app(app)
    init_routes(app)

    return app
