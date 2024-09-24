from application import create_testing_app, create_development_app
import sys

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "TEST":
        app = create_testing_app()
    elif mode == "DEV":
        app = create_development_app()
    else:
        sys.exit()
    app.run(debug=True)