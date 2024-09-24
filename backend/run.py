from application import create_testing_app

if __name__ == "__main__":
    app = create_testing_app()
    app.run(debug=True)