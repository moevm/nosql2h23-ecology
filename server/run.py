from app import app


if __name__ == "__main__":
    port = app.config.get('FLASK_PORT')

    if app.config.get('DEBUG'):
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()
