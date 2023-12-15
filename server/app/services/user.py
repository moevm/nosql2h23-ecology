from bson import ObjectId

from app import app
from app.db import get_db

with app.app_context():
    db = get_db()


def get_user_by_id(id: str):
    return db.users.find_one(ObjectId(id))


def find_user(login: str):
    return db.users.find_one({"login": login})


def update_user(id: str, data):
    return db.users.update_one({"_id": ObjectId(id)}, {"$set": data})


def delete_user(id: str):
    db.users.delete_one({"_id": ObjectId(id)})


def bulk_upload_users(new_users):
    users_keys = ["_id", "login", "password", "name", "role"]
    for user in new_users:
        for k in users_keys:
            if k not in user:
                return "Not ok"
        del user['_id']

    # Пропускаем уже существующих пользователей
    new_users = list(filter(
        lambda user: not db.users.find_one({"login": user["login"]}),
        new_users
    ))

    if len(new_users):
        db.users.insert_many(new_users)
