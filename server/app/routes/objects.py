from flask_restx import Namespace, Resource
from redis.client import StrictRedis
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId

from app.db import get_db, get_tiles, get_maps, get_redis

db = LocalProxy(get_db)
tiles_fs = LocalProxy(get_tiles)
maps_fs = LocalProxy(get_maps)
redis: StrictRedis = LocalProxy(get_redis)

api = Namespace("objects", description="Операции с объедками")


@api.route('/')
class ObjectsList(Resource):
    def get(self):
        objects = []
        for map_object in db.objects.find({}):
            objects.append({
                "id": str(map_object["_id"]),
                "type": map_object["type"],
                "name": map_object["name"],
                "color": map_object["color"],
                "updateUserId": map_object["update"]["user_id"],
                "updateDatetime": map_object["update"]["datetime"],
                "coordinates": map_object["coordinates"],
                # Переворачиваем, чтобы получить [lat, lng] для leaflet
                "center": [map_object["center"][1], map_object["center"][0]],
            })
        return objects


@api.route('/object/<string:obj_id>')
class ImageObjects(Resource):
    def get(self, obj_id):
        map_object = db.objects.find_one(ObjectId(obj_id))
        return {
            "id": str(map_object["_id"]),
            "type": map_object["type"],
            "name": map_object["name"],
            "color": map_object["color"],
            "updateUserId": map_object["update"]["user_id"],
            "updateDatetime": map_object["update"]["datetime"],
            "coordinates": map_object["coordinates"],
            # Переворачиваем, чтобы получить [lat, lng] для leaflet
            "center": [map_object["center"][1], map_object["center"][0]],
        }


@api.route('/near/<string:y>/<string:x>/<string:r>')
class ObjectsNear(Resource):
    def get(self, y, x, r):
        x, y, r = float(x), float(y), float(r)

        objects_info = db.objects.find({
            "center": {
                "$nearSphere": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [x, y]
                    },
                    "$maxDistance": r,
                }
            }
        })

        objects = []
        for map_object in objects_info:
            objects.append({
                "id": str(map_object["_id"]),
                "type": map_object["type"],
                "name": map_object["name"],
                "color": map_object["color"],
                "updateUserId": map_object["update"]["user_id"],
                "updateDatetime": map_object["update"]["datetime"],
                "coordinates": map_object["coordinates"],
                # Переворачиваем, чтобы получить [lat, lng] для leaflet
                "center": [map_object["center"][1], map_object["center"][0]],
            })
        return objects
