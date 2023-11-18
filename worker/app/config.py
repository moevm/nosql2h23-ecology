from os import environ

MONGO_URI = environ.get('MONGO_URI', "mongodb://localhost:27017/db")
REDIS_URI = environ.get('REDIS_URI', "redis://localhost:6379/0")

MIN_ZOOM = int(environ.get('MIN_ZOOM', 1))
MAX_ZOOM = int(environ.get('MAX_ZOOM', 15))
