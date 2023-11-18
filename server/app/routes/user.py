from flask_restx import Namespace, Resource, fields
from werkzeug.local import LocalProxy

from app.db import get_db

api = Namespace("users", description="Операции с пользователями")

db = LocalProxy(get_db)


@api.route('/')
class UserList(Resource):
    def post(self):
        return "Create"


@api.route('/user/<int:id>')
class User(Resource):
    def get(self, id):
        return f"User: {id}"

    def delete(self, id):
        return f"Delete: {id}"

    def put(self, id):
        return f"Edit: {id}"