from os import environ

MONGO_URI = environ.get('MONGO_URI', "mongodb://localhost:27017/db")
REDIS_URI = environ.get('REDIS_URI', "redis://localhost:6379/0")
