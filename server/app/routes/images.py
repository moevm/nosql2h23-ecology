import arrow
from flask import jsonify, request, make_response
from flask_restx import Namespace, Resource
from redis.client import StrictRedis
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId

from app.db import get_db, get_tiles, get_maps, get_redis
from app.tasks import process_image
from app.tasks import slice
from app.services.pagination import format_pagination

db = LocalProxy(get_db)
tiles_fs = LocalProxy(get_tiles)
maps_fs = LocalProxy(get_maps)
redis: StrictRedis = LocalProxy(get_redis)

api = Namespace("images", description="Операции с изображениями")


def get_images_list(find_query={}, skip=0, limit=0):
    maps = []
    for map in db.maps.files.find(find_query).skip(skip).limit(limit):
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

@api.route('/')
class ImagesList(Resource):
    def get(self):
        return get_images_list()

    def post(self):
        new_map = request.files['image']
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
    

@api.route('/table/')
class ImagesForTable(Resource):
    def get(self):
        args = request.args.to_dict()
        format_pagination(args)

        # Переименовываем некоторые поля, которые на сервере называются по-другому.


        # Формируем запрос.
        query = {}

        # Получаем карты, которые подходят под все условия, заданные на клиенте.
        data = get_images_list(query, args["start"], args["end"] - args["start"])
       
        return make_response(jsonify({
            "rowData": data,
            "end": args["start"] + len(data)
        }) , 200)


@api.route('/near/<string:y>/<string:x>/<string:r>')
class ImageFinder(Resource):
    def get(self, y, x, r):
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


@api.route('/image/<string:img_id>')
class Image(Resource):
    def delete(self, img_id):
        map_info = db.maps.files.find_one(ObjectId(img_id))

        if map_info:
            maps_fs.delete(ObjectId(img_id))
            for tile in db.tiles.files.find({"image_id": ObjectId(img_id)}):
                tiles_fs.delete(tile["_id"])

            return jsonify({'message': 'Image deleted successfully'})
        
        return 'OK'

