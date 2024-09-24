import sys
import os

# Ensure the backend directory is in the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from application import create_testing_app  # Import the app variable
from application.models import *

import pytest
@pytest.fixture
def client():
    app = create_testing_app()
    # Set up the test client and database context
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
        yield client
        with app.app_context():
            db.drop_all()  # Tear down tables after tests
