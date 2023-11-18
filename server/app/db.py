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


def get_maps():
    fs = getattr(g, "maps", None)
    if fs is None:
        fs = g.maps = GridFS(get_db(), 'maps')
    return fs


def get_tiles():
    fs = getattr(g, "tiles", None)
    if fs is None:
        fs = g.tiles = GridFS(get_db(), 'tiles')
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
