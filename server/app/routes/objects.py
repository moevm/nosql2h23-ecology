from flask import request, jsonify, make_response
from flask_login import login_required
from flask_restx import Namespace, Resource
from redis.client import StrictRedis
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId
import json

from app.db import get_db, get_tiles, get_maps, get_redis
from app.utils import parse_json
from app.services.pagination import format_pagination

db = LocalProxy(get_db)
tiles_fs = LocalProxy(get_tiles)
maps_fs = LocalProxy(get_maps)
redis: StrictRedis = LocalProxy(get_redis)

api = Namespace("objects", description="Операции с объедками")


def get_objects_list(find_query={}, skip=0, limit=0):
    objects = []
    for map_object in db.objects.find(find_query).skip(skip).limit(limit):
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


@api.route('/')
class ObjectsList(Resource):
    def get(self):
        return get_objects_list()
    

@api.route('/table/')
class ImagesForTable(Resource):
    def get(self):
        args = request.args.to_dict()
        format_pagination(args)

        # Переименовываем некоторые поля, которые на сервере называются по-другому.
        

        # Формируем запрос.
        query = {}

        # Получаем объекты, которые подходят под все условия, заданные на клиенте.
        data = get_objects_list(query, args["start"], args["end"] - args["start"])
       
        return make_response(jsonify({
            "rowData": data,
            "end": args["start"] + len(data)
        }) , 200)


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


@api.route('/update')
class ObjectsUpdate(Resource):
    def post(self):
        json = request.get_json()
        edited_obj = json['edited']
        created_obj = json['created']
        deleted_obj = json['deleted']

        # Переформируем полученные словари:
        edited_obj_id = []
        deleted_obj_id = []
        for obj_dict in [edited_obj, created_obj, deleted_obj]:
            for obj in obj_dict:
                if obj_dict == edited_obj:
                    edited_obj_id.append(ObjectId(obj["id"]))
                elif obj_dict == deleted_obj:
                    deleted_obj_id.append(ObjectId(obj["id"]))
                # Заменяем id на _id
                if "id" in obj:
                    obj["_id"] = ObjectId(obj["id"])
                    obj.pop("id")
                # updateUserId и updateDatetime на update: {user_id, datetime}
                obj["update"] = {"user_id": obj["updateUserId"], "datetime": obj["updateDatetime"]}
                obj.pop("updateUserId")
                obj.pop("updateDatetime")

        # Добавляем объекты, добавленные пользователем.
        if created_obj:
            db.objects.insert_many(created_obj)

        # Изменяем объекты, измененные пользователем.
        if edited_obj:
            db.objects.delete_many({"_id": {"$in": edited_obj_id}})
            db.objects.insert_many(edited_obj)

        # Удаляем объекты, удаленные пользователем.
        if deleted_obj:
            db.objects.delete_many({"_id": {"$in": deleted_obj_id}})

        return "Ok"


@api.route('/impex')
class ObjectsImpex(Resource):
    def get(self):
        return parse_json(db.objects.find({}))

    @login_required
    def post(self):
        new_objects = json.load(request.files['objects'])
        object_keys = ["_id", "type", "name", "color", "update", "coordinates", "center"]
        for obj in new_objects:
            for k in object_keys:
                if k not in obj:
                    return "Not ok"
            del obj['_id']
        db.objects.insert_many(new_objects)
        return "Ok"
