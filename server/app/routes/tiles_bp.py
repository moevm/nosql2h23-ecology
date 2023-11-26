import io
from flask import Blueprint, send_file
from redis.client import StrictRedis
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId

from app.db import get_db, get_tiles, get_maps, get_redis


db = LocalProxy(get_db)
tiles_fs = LocalProxy(get_tiles)
maps_fs = LocalProxy(get_maps)
redis: StrictRedis = LocalProxy(get_redis)

tiles_bp = Blueprint('tiles_bp', __name__, url_prefix="/tiles")


@tiles_bp.route("/<string:map_id>/<int:z>/<int:x>/<int:y>", methods=['GET'])
def get_tile(map_id, z, x, y):
    tile = tiles_fs.find_one({'image_id': ObjectId(map_id), 'z': z, 'x': x, 'y': y})
    if tile:
        return send_file(io.BytesIO(tile.read()), mimetype='image/png')
    else:
        return 'OK'

