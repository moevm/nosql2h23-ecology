from werkzeug.local import LocalProxy
from flask import current_app as app
from app.db import get_db

db = LocalProxy(get_db)


def get_admin():
    admin = db.users.find_one({"login": app.config.get('INIT_ADMIN_LOGIN')})
    if not admin:
        result = db.users.insert_one({
            'login': app.config.get('INIT_ADMIN_LOGIN'),
            'password': app.config.get('INIT_ADMIN_PASSWORD'),
            'name': 'root',
            'role': 'admin'
        })
        admin = db.users.find_one(result.inserted_id)
    return admin


def get_test_user():
    user = db.users.find_one({"login": 'user'})
    if not user:
        result = db.users.insert_one({
            'login': 'user',
            'password': '1234',
            'name': 'Ivan',
            'role': 'user'
        })
        user = db.users.find_one(result.inserted_id)
    return user
