from os import environ

FLASK_PORT = environ.get('FLASK_PORT', 5000)
MONGO_URI = environ.get('MONGO_URI', "mongodb://localhost:27017/db")
REDIS_URI = environ.get('REDIS_URI', "redis://localhost:6379/0")

PRUNE_DB = environ.get('PRUNE_DB', 'False') == 'True'
TEST_DATA = environ.get('TEST_DATA', 'False') == 'True'
DEBUG = environ.get('DEBUG', 'True') == 'True'
SECRET_KEY = environ.get('SESSION_KEY', '$Default_Secret_Key$')

INIT_ADMIN_LOGIN = environ.get('INIT_ADMIN_LOGIN', 'admin')
INIT_ADMIN_PASSWORD = environ.get('INIT_ADMIN_PASSWORD', 'admin')
