import io
import arrow
from flask import jsonify, request, send_file, abort
from flask_restx import Namespace, Resource
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

api = Namespace("tiles", description="Операции с тайлами изображений")


# Маршрут для leaflet-а, возвращает кусочки для отображения.
@api.route("/tile/<string:img_id>/<int:z>/<int:x>/<int:y>")
class Tile(Resource):
    def get(self, img_id, z, x, y):
        tile = tiles_fs.find_one({'image_id': ObjectId(img_id), 'z': z, 'x': x, 'y': y})
        if tile:
            return send_file(io.BytesIO(tile.read()), mimetype='image/png')
        else:
            return 'OK'
