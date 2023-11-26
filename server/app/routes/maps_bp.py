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
    for map in db.maps.files.find({}):
        maps.append({
            "id": str(map["_id"]),
            "name": map["name"],
            "updateUserId": map["update"]["user_id"],
            "updateDatetime": map["update"]["datetime"],
            "coordinates": map["coordinates"],
            # Переворачиваем, чтобы получить [lat, lng] для leaflet
            "center": [map["center"][1], map["center"][0]],
            "ready": map["ready"],
            "sliced": map["sliced"]
        })
    return maps


@maps_bp.route('/upload_map', methods=['POST'])
def add_map():
    new_map = request.files['map']
    img_name = request.form.get('name')
    file_id = maps_fs.put(
        new_map, filename=request.form.get('name'),  chunk_size= 256 * 1024,
        name = img_name,
        center = [0.5, 0.5],
        coordinates = [[0, 1], [1, 1], [1, 0], [0, 0]],
        # TO DO: normal user_id.
        update = {"user_id": 0, "datetime": str(arrow.now().to('UTC'))},
        ready = False,
        sliced = False
    )

    slice.delay(str(file_id))
    process_image.delay(str(file_id))

    return jsonify({'message': 'Image added successfully'})


@maps_bp.route('/delete_map/<string:map_id>', methods=['DELETE'])
def delete_map(map_id):
    map_info = db.maps.files.find_one(ObjectId(map_id))

    if map_info:
        maps_fs.delete(ObjectId(map_id))
        for tile in db.tiles.files.find({"image_id": ObjectId(map_id)}):
            tiles_fs.delete(tile["_id"])

        socketio.emit("images", get_images_list()) #update sockets
        return jsonify({'message': 'Image deleted successfully'})
    
    return 'OK'


@maps_bp.route('/<string:map_id>', methods=['GET'])
def get_image(map_id):
    maps_file = maps_fs.files.find_one(ObjectId(map_id)) #choose file?
    return send_file(io.BytesIO(maps_file), mimetype='image/tiff')


@maps_bp.route('/near/<string:y>/<string:x>/<string:r>', methods=['GET'])
def images_near(y, x, r):
    x, y, r = float(x), float(y), float(r)

    maps_info = db.maps.files.find({
        "center": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [x, y]
                },
                "$maxDistance": r,
            }
        }, 
        "sliced": True
    })

    maps = []
    for map in maps_info:
        maps.append({
            "id": str(map["_id"]),
            "name": map["name"],
            "updateUserId": map["update"]["user_id"],
            "updateDatetime": map["update"]["datetime"],
            "coordinates": map["coordinates"],
            # Переворачиваем, чтобы получить [lat, lng] для leaflet
            "center": [map["center"][1], map["center"][0]],
            "ready": map["ready"],
            "sliced": map["sliced"]
        })
    return maps
