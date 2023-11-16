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

maps_bp = Blueprint('maps_bp', __name__, url_prefix="/maps")


@maps_bp.route('/', methods=['GET'])
# delete excess
def get_images_list():
    maps = []
    for one_map in maps_fs.files.find({}):
        maps.append({
            "id": str(one_map["_id"]),
            "name": one_map["name"],
            "update": one_map["update"],
            "location": one_map["location"],
            "tile_map_resource": one_map["tile_map_resource"],
            "size": one_map["size"],
            "ready": one_map["ready"],
            "sliced": one_map["sliced"]
        })

    return maps


@maps_bp.route('/tile_map_resource/<string:img_id>', methods=['GET'])
def index(img_id):
    tile_map_resource = maps_fs.files.find_one(ObjectId(img_id))["tile_map_resource"]
    if tile_map_resource is None:
        abort(404)
    else:
        return maps_fs.files.find_one(ObjectId(img_id))["tile_map_resource"]


@maps_bp.route('/upload_map', methods=['POST'])
def add_map():
    new_map = request.files['map']
    file_id = maps_fs.put(new_map, filename=request.form.get('name'),  chunk_size=256 * 1024,
                          metadata={"location": "something",
                                    "tile_map_resource": "something too",
                                    "size": "new_map.size() ?",
                                    "ready": False,
                                    "sliced": False})

    slice.delay(str(file_id))
    process_image.delay(str(file_id))

    return jsonify({'message': 'Image added successfully'})


@maps_bp.route('/delete_map/<string:map_id>', methods=['DELETE'])
def delete_map(map_id):
    map_info = maps_fs.files.find_one(ObjectId(map_id))
    if map_info:
        maps_fs.delete(ObjectId(map_id))
        for tile in tiles_fs.files.find({"image_id": ObjectId(map_id)}):
            tiles_fs.delete(tile._id)

        socketio.emit("images", get_images_list()) #update sockets
        return jsonify({'message': 'Image deleted successfully'})
    return 'OK'


# Маршрут для leaflet-а, возвращает кусочки для отображения.

@maps_bp.route('/<string:map_id>', methods=['GET'])
def get_image(map_id):
    maps_file = maps_fs.files.find_one(ObjectId(map_id)) #choose file?
    return send_file(io.BytesIO(maps_file), mimetype='image/tiff')

