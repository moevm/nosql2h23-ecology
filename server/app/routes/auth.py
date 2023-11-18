from flask_restx import Namespace, Resource, fields
from werkzeug.local import LocalProxy

from app.db import get_db

api = Namespace("auth", description="Аутентификация")

db = LocalProxy(get_db)


@api.route('/login')
class Login(Resource):
    def post(self):
        return "Log In"

    def get(self):
        return 'get logging'


@api.route('/login/dev')
class Login(Resource):
    def post(self):
        return "Admin Login"