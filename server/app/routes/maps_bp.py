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
def get_images_list():
    maps = []
    for img in db.maps.find({}):
        maps.append({
            "id": str(img["_id"]),
            "name": img["name"],
            'uploadDate': img["upload_date"],
            'size': maps_fs.find_one({'_id': img["fs_id"]}).length,
            "ready": img["ready"],
            "sliced": img["sliced"]
        })

    return maps

''' УБРАТЬ '''
@maps_bp.route('/tile_map_resource/<string:img_id>', methods=['GET'])
def index(img_id):
    tile_map_resource = db.images.find_one(ObjectId(img_id))["tile_map_resource"]
    if tile_map_resource is None:
        abort(404)
    else:
        return db.images.find_one(ObjectId(img_id))["tile_map_resource"]


@maps_bp.route('/upload_map', methods=['POST'])
def add_map():
    new_map = request.files['map']
    file_id = maps_fs.put(new_map, filename=new_map.filename, chunk_size=256 * 1024)
    img_name = request.form.get('name')
    item = {
        "tile_map_resource": None,
        "fs_id": file_id,
        "objects": [],
        "upload_date": str(arrow.now().to('UTC')),
        "detect_date": "",
        "name": img_name,
        'ready': False,
        'sliced': False
    }
    
    result = db.images.insert_one(item)
    img_id = result.inserted_id

    slice.delay(str(img_id))
    process_image.delay(str(img_id))

    return jsonify({'message': 'Image added successfully'})


@maps_bp.route('/delete_image/<string:img_id>', methods=['DELETE'])
def delete_image(img_id):
    image_info = db.images.find_one(ObjectId(img_id))
    if (image_info):
        fs_id = image_info["fs_id"]

        db.images.delete_one({"_id": ObjectId(img_id)})

        maps_fs.delete(fs_id)
        for tile in tiles_fs.find({"image_id": ObjectId(img_id)}):
            tiles_fs.delete(tile._id)

        socketio.emit("images", get_images_list())
        return jsonify({'message': 'Image deleted successfully'})
    return 'OK'


# Маршрут для leaflet-а, возвращает кусочки для отображения.
@maps_bp.route("/tile/<string:img_id>/<int:z>/<int:x>/<int:y>", methods=['GET'])
def get_tile(img_id, z, x, y):
    tile = tiles_fs.find_one({'image_id': ObjectId(img_id), 'z': z, 'x': x, 'y': y})
    if tile:
        return send_file(io.BytesIO(tile.read()), mimetype='image/png')
    else:
        return 'OK'


@maps_bp.route('/<string:img_id>', methods=['GET'])
def get_image(img_id):
    image_info = db.images.find_one(ObjectId(img_id))
    image_file = tiles_fs.get(image_info["fs_id"])
    return send_file(io.BytesIO(image_file), mimetype='image/tiff')


@maps_bp.route('/objects/<string:img_id>', methods=['GET'])
def get_all_objects(img_id):
    return db.images.find_one(ObjectId(img_id))["objects"] 
