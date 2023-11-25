import io
import arrow
from flask import Blueprint, jsonify, request, send_file, abort
from redis.client import StrictRedis
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId

from app import socketio
from app.db import get_db, get_tiles, get_maps, get_redis
from app.tasks import process_image
from app.tasks import slice


db = LocalProxy(get_db)
tiles_fs = LocalProxy(get_tiles)
maps_fs = LocalProxy(get_maps)
redis: StrictRedis = LocalProxy(get_redis)

users_bp = Blueprint('users_bp', __name__, url_prefix="/users")

@users_bp.route('/add_user', methods=['POST'])
def add_map():
    db.users.insert({"login": "LOGIN",
                     "password": "PASSWORD",
                     "name": "Dmitriy",
                     "status": "offline",
                     "role": "admin"})

    return jsonify({'message': 'User added successfully'})
