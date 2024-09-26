from application import create_testing_app, create_development_app
import sys
from database_setup import *
import signal 

def handle_exit_signal(signum, frame):
    """Handle server shutdown and drop the database."""
    print("\nShutting down the server...")
    with app.app_context():
        db.drop_all()  # Drop all tables from the database
        print("Database dropped successfully.")
    sys.exit(0)  # Exit the program after cleanup


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "TEST":
        app = create_testing_app()
    elif mode == "DEV":
        signal.signal(signal.SIGINT, handle_exit_signal)       
        app = create_development_app()
        with app.app_context():
            db.drop_all()
        initialize_database(app=app)
    else:
        sys.exit()
    app.run(debug=True)