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
    for one_object in db.objects.find({}):
        one_object.append({
            "id": str(one_object._id),
            "type": one_object["type"],
            "name": one_object["name"],
            "color": one_object["color"],
            "update": one_object["update"], #join?
            "location": one_object["location"] #join?
        })
    return objects


@objects_bp.route('/<string:obj_id>', methods=['GET'])
def index(obj_id):
    obj = db.objects.find_one(ObjectId(obj_id))
    if obj is None:
        abort(404)
    else:
        return obj
