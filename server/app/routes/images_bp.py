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

images_bp = Blueprint('images_bp', __name__, url_prefix="/images")


@images_bp.route('/', methods=['GET'])
def get_images_list():
    images = []
    for img in db.images.find({}):
        images.append({
            "id": str(img["_id"]),
            "name": img["name"],
            'uploadDate': img["upload_date"],
            'size': maps_fs.find_one({'_id': img["fs_id"]}).length,
            "location": img["location"],
            "ready": img["ready"],
            "sliced": img["sliced"]
        })

    return images


@images_bp.route('/near/<string:y>/<string:x>/<string:r>', methods=['GET'])
def images_near(y, x, r):
    x, y, r = float(x), float(y), float(r)
    # TO DO: после рефакторинга бд должно находится НОРМАЛЬНО, а не в цикле :(
    images = []
    for img in db.images.find({}):
        # Координаты в [y, x], так как leaflet работает в [lat, long].
        if (img["sliced"]):
            y_point_img, x_point_img = img["location"]["coordinates"][0]
            if (x_point_img - x)**2 + (y_point_img - y)**2 <= r**2:
                images.append({
                    "id": str(img["_id"]),
                    "name": img["name"],
                    'uploadDate': img["upload_date"],
                    'size': maps_fs.find_one({'_id': img["fs_id"]}).length,
                    "location": img["location"],
                    "ready": img["ready"],
                    "sliced": img["sliced"]
                })
    return images


@images_bp.route('/tile_map_resource/<string:img_id>', methods=['GET'])
def index(img_id):
    tile_map_resource = db.images.find_one(ObjectId(img_id))["tile_map_resource"]
    if tile_map_resource is None:
        abort(404)
    else:
        return db.images.find_one(ObjectId(img_id))["tile_map_resource"]


@images_bp.route('/upload_image', methods=['POST'])
def add_image():
    image = request.files['image']
    file_id = maps_fs.put(image, filename=image.filename, chunk_size=256 * 1024)
    img_name = request.form.get('name')
    item = {
        "location": {"type": "Polygon", "coordinates": []},
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


@images_bp.route('/delete_image/<string:img_id>', methods=['DELETE'])
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
@images_bp.route("/tile/<string:img_id>/<int:z>/<int:x>/<int:y>", methods=['GET'])
def get_tile(img_id, z, x, y):
    tile = tiles_fs.find_one({'image_id': ObjectId(img_id), 'z': z, 'x': x, 'y': y})
    if tile:
        return send_file(io.BytesIO(tile.read()), mimetype='image/png')
    else:
        return 'OK'


@images_bp.route('/objects/<string:img_id>', methods=['GET'])
def get_all_objects(img_id):
    return db.images.find_one(ObjectId(img_id))["objects"] 
