from werkzeug.local import LocalProxy

from app.db import get_db

db = LocalProxy(get_db)


def bulk_upload_objects(new_objects):
    object_keys = ["_id", "type", "name", "color", "update", "coordinates", "center"]
    for obj in new_objects:
        for k in object_keys:
            if k not in obj:
                return "Not ok"
        del obj['_id']
    db.objects.insert_many(new_objects)
