from flask import Flask
from .api import api
from .models import db


def create_testing_app():
    app = Flask(__name__)
    
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with the db instance
    db.init_app(app)
    app.register_blueprint(api)

    # Register your blueprints, etc.

    return app
