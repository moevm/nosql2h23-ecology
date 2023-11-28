from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config.from_pyfile('config.py')

from .auth.login_manager import login_manager

login_manager.init_app(app)

from .routes import api

api.init_app(app)

CORS(app, supports_credentials=True)

from .websocket.queue import send_queue

scheduler = BackgroundScheduler()
scheduler.add_job(send_queue, 'interval', seconds=1)
scheduler.start()

from .dev import get_admin, get_test_user


def add_init_users():
    get_admin()
    get_test_user()


with app.app_context():
    add_init_users()
