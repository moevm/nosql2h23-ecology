from werkzeug.local import LocalProxy
from flask import current_app as app
import arrow
import os
import sys
from app.db import get_db, get_maps
from app.tasks import process_image, slice


db = LocalProxy(get_db)
maps_fs = LocalProxy(get_maps)

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


def add_test_data():
    test_file_path = "/map_samples/2.tif"
    if os.path.isfile(test_file_path) and not db.maps.files.count_documents({}):
        file_id = maps_fs.put(
            open(test_file_path, "rb"), filename="2.tif",  chunk_size= 256 * 1024,
            name = "test_sample",
            center = [0.5, 0.5],
            coordinates = [[0, 1], [1, 1], [1, 0], [0, 0]],
            update = {"user_id": "test_data", "datetime": str(arrow.now().to('UTC'))},
            ready = False,
            sliced = False
        )

        slice.delay(str(file_id))
        process_image.delay(str(file_id))
