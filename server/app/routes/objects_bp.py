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

objects_bp = Blueprint('objects_bp', __name__, url_prefix="/objects")


@objects_bp.route('/', methods=['GET'])
def get_objects_info_list():
    objects = []
    for img in db.images.find({}):
        img_objects_types = img["objects"]
        for img_objects in img_objects_types:
            if (img_objects['name'] != 'Forest'):
                for i in range(len(img_objects['area'])):
                    objects.append({
                        "id": str(img["_id"]),
                        "name": img_objects["name"],
                        "objectIndex": i,
                        "area": img_objects['area'][i],
                        "uploadDate": img["upload_date"],
                        "detectDate": img["detect_date"]
                    })
    return objects


@objects_bp.route('/<string:img_id>', methods=['GET'])
def get_objects_of_image(img_id):
    img = db.images.find_one(ObjectId(img_id))
    img_objects_types = img["objects"]

    objects = []
    for img_objects in img_objects_types:
        if (img_objects['name'] != 'Forest'):
            for i in range(len(img_objects['area'])):
                coordinates = [0, 0]
                for polygon_point in img_objects['polygons'][int(i)]:
                    coordinates[0] += polygon_point[0]
                    coordinates[1] += polygon_point[1]
                coordinates[0] /= len(img_objects['polygons'][int(i)])
                coordinates[1] /= len(img_objects['polygons'][int(i)])

                objects.append({
                    "id": str(img_id),
                    "name": img_objects["name"],
                    "objectIndex": i,
                    "area": img_objects["area"][i],
                    "coordinates": coordinates,
                    "uploadDate": img["upload_date"],
                    "detectDate": img["detect_date"] 
                })
    return objects


@objects_bp.route('/<string:img_id>/<string:object_name>/<string:object_index>', methods=['GET'])
def get_object(img_id, object_name, object_index):
    img = db.images.find_one(ObjectId(img_id))
    img_objects_types = img["objects"]

    area = 0
    for img_objects in img_objects_types:
        if (img_objects['name'] == object_name):
            area = img_objects['area'][int(object_index)]
            coordinates = [0, 0]
            for polygon_point in img_objects['polygons'][int(object_index)]:
                coordinates[0] += polygon_point[0]
                coordinates[1] += polygon_point[1]
            coordinates[0] /= len(img_objects['polygons'][int(object_index)])
            coordinates[1] /= len(img_objects['polygons'][int(object_index)])
            break
    
    result = {
        "id": str(img_id),
        "name": object_name,
        "objectIndex": object_index,
        "area": area,
        "coordinates": coordinates,
        "uploadDate": img["upload_date"],
        "detectDate": img["detect_date"] 
    }
    return result
