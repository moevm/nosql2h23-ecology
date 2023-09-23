import pymongo
import redis
from flask import g
from gridfs import GridFS
from flask import current_app as app


def get_db():
    db = getattr(g, "database", None)
    if db is None:
        client = pymongo.MongoClient(app.config.get('MONGO_URI'))  # config['PROD']['DB_URI']
        # Если есть база данных ecologyDB
        db = g.database = client.get_database('ecologyDB')
    return db


def close_db(error=None):
    db = g.pop('database', None)
    if db is not None:
        db.close()


def get_map_fs():
    fs = getattr(g, "map_fs", None)
    if fs is None:
        fs = g.map_fs = GridFS(get_db(), 'map_fs')
    return fs


def get_tile_fs():
    fs = getattr(g, "tile_fs", None)
    if fs is None:
        fs = g.tile_fs = GridFS(get_db(), 'tile_fs')
    return fs


def get_redis():
    r = getattr(g, "redis", None)
    if r is None:
        r = g.redis = redis.StrictRedis.from_url(app.config.get('REDIS_URI'), decode_responses=True)
    return r


def close_redis(error=None):
    r = g.pop('redis', None)
    if r is not None:
        r.close()
