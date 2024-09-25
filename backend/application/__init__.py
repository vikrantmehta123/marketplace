from flask import Flask
from .models import db, User, Role
from .dal import UserDAL
from flask_cors import CORS

def setup_initial_data():
    roles = {1: 'admin', 2: 'editor', 3: 'viewer'}
    for role_id, role_name in roles.items():
        existing_role = db.session.query(Role).filter_by(role_id=role_id).first()
        if existing_role is None:
            new_role = Role(role_id=role_id, role_name=role_name)
            db.session.add(new_role)
        else:
            print(f"Role '{role_name}' already exists.")
    db.session.commit()
    admin = db.session.query(User).filter_by(username='admin').first()
    if admin is None:
        admin = UserDAL.create(username='admin', email='admin@example.com',
                     password='adminpassword', contact="1234567890", address="10 Dummy Street", roles=[1])

        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

def create_testing_app():
    app = Flask(__name__)

    app.config['TESTING'] = True
    # In-memory DB for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with the db instance
    db.init_app(app)
    from .api import api
    
    app.register_blueprint(api)

    return app

def create_development_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    
    db.init_app(app)
    from .api import api
    from .cache import cache

    app.register_blueprint(api)
    cache.init_app(app=app)
    with app.app_context():
        db.create_all()  # Create tables
        setup_initial_data()
    return app
