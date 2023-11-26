import io
import arrow
from flask import Blueprint, jsonify
from redis.client import StrictRedis
from werkzeug.local import LocalProxy

from app.db import get_db, get_tiles, get_maps, get_redis


db = LocalProxy(get_db)
tiles_fs = LocalProxy(get_tiles)
maps_fs = LocalProxy(get_maps)
redis: StrictRedis = LocalProxy(get_redis)

users_bp = Blueprint('users_bp', __name__, url_prefix="/users")

@users_bp.route('/add_user', methods=['POST'])
def add_user():
    db.users.insert({"login": "LOGIN",
                     "password": "PASSWORD",
                     "name": "Dmitriy",
                     "status": "offline",
                     "role": "admin"})

    return jsonify({'message': 'User added successfully'})
