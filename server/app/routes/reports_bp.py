from flask import Blueprint
from redis.client import StrictRedis
from werkzeug.local import LocalProxy
from bson.objectid import ObjectId

from app.db import get_db, get_tile_fs, get_map_fs, get_redis


db = LocalProxy(get_db)
tile_fs = LocalProxy(get_tile_fs)
map_fs = LocalProxy(get_map_fs)
redis: StrictRedis = LocalProxy(get_redis)

reports_bp = Blueprint('reports_bp', __name__, url_prefix="/reports")


@reports_bp.route('/', methods=['GET'])
def get_reports_list():
    reports = []
    for img in db.images.find({}):
        img_anomalies_types = img["anomalies"]
        count = sum([len(anomalies['polygons']) for anomalies in filter(lambda x: x['name'] != 'Forest', img_anomalies_types)])
        if count > 0:
            reports.append({
                "id": str(img["_id"]),
                "date": img["detect_date"],
                "anomalies": count,
                "name": str(img["name"]) 
            })
    return reports


@reports_bp.route('/<string:img_id>', methods=['GET'])
def get_report(img_id):
    anomalies = []
    img = db.images.find_one(ObjectId(img_id))
    img_anomalies_types = img["anomalies"]
    for img_anomalies in img_anomalies_types:
        if (img_anomalies['name'] != 'Forest'):
            for i in range(len(img_anomalies['area'])):
                anomalies.append({
                    "id": str(img["_id"]),
                    "anomalyIndex": i,
                    "name": img_anomalies["name"],
                    "area": img_anomalies['area'][i]
                })
    return anomalies

