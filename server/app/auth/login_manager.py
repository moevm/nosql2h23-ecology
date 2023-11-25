from bson import ObjectId
from flask_login import LoginManager

from app.auth.User import User
from app.db import get_db

login_manager = LoginManager()

from app import app

with app.app_context():
    db = get_db()


@login_manager.user_loader
def load_user(user_id):
    user = db.users.find_one(ObjectId(user_id))
    if user:
        return User(user)
    else:
        return None
