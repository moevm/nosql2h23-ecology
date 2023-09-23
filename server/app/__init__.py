from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

from .routes import api_bp

app.config.from_pyfile('config.py')
app.register_blueprint(api_bp, url_prefix="/api")
CORS(app)

from .websocket.queue import send_queue

scheduler = BackgroundScheduler()
scheduler.add_job(send_queue, 'interval', seconds=1)
scheduler.start()
