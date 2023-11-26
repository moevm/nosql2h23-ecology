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

api = Namespace("images", description="Операции с изображениями")


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


@api.route('/')
class ImagesList(Resource):
    def get(self):
        return get_images_list()

    def post(self):
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


@api.route('/near/<string:y>/<string:x>/<string:r>')
class ImageFinder(Resource):
    def get(self, y, x, r):
        x, y, r = float(x), float(y), float(r)
        # TO DO: после рефакторинга бд должно находится НОРМАЛЬНО, а не в цикле :(
        images = []
        for img in db.images.find({}):
            # Координаты в [y, x], так как leaflet работает в [lat, long].
            if (img["sliced"]):
                y_point_img, x_point_img = img["location"]["coordinates"][0]
                if (x_point_img - x) ** 2 + (y_point_img - y) ** 2 <= r ** 2:
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


@api.route('/tile_map_resource/<string:img_id>')
class TileResources(Resource):
    def get(self, img_id):
        tile_map_resource = db.images.find_one(ObjectId(img_id))["tile_map_resource"]
        if tile_map_resource is None:
            abort(404)
        else:
            return db.images.find_one(ObjectId(img_id))["tile_map_resource"]


@api.route('/image/<string:img_id>')
class Image(Resource):
    def delete(self, img_id):
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
@api.route("/tile/<string:img_id>/<int:z>/<int:x>/<int:y>")
class Tile(Resource):
    def get(self, img_id, z, x, y):
        tile = tiles_fs.find_one({'image_id': ObjectId(img_id), 'z': z, 'x': x, 'y': y})
        if tile:
            return send_file(io.BytesIO(tile.read()), mimetype='image/png')
        else:
            return 'OK'


@api.route('/objects/<string:img_id>')
class ObjectsFinder(Resource):
    def get(self, img_id):
        return db.images.find_one(ObjectId(img_id))["objects"]
