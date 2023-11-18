from flask_restx import Namespace, Resource, fields
from werkzeug.local import LocalProxy

from app.db import get_db

api = Namespace("users", description="Операции с пользователями")

db = LocalProxy(get_db)

# Тело для добавления пользователя
user_post_parser = api.parser(
).add_argument(
    "login", type=str, required=True
).add_argument(
    "password", type=str, required=True
).add_argument(
    "name", type=str, required=True
).add_argument(
    "role", type=str, required=True
)


@api.route('/')
class UserList(Resource):
    @api.doc(parser=user_post_parser)
    def post(self):
        args = user_post_parser.parse_args()
        if db.users.find_one({"login": args.login}):
            return f"User with login {args.login} already exists", 400
        result = db.users.insert_one(args)
        return str(result.inserted_id)

    def get(self):
        return 'Get Self'


@api.route('/user/<int:id>')
class User(Resource):
    def get(self, id):
        return f"User: {id}"

    def delete(self, id):
        return f"Delete: {id}"

    def put(self, id):
        return f"Edit: {id}"
