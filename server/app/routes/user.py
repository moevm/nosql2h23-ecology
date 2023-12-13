from flask_login import login_required, current_user
from flask_restx import Namespace, Resource, fields
from werkzeug.local import LocalProxy

from app.auth.authorization import role_require
from app.db import get_db
from app.services.user import get_user_by_id, find_user, update_user, delete_user
from app.utils import parse_json

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

# Тело для обновления пользователя
user_put_parser = api.parser(
).add_argument(
    "login", type=str, required=False
).add_argument(
    "password", type=str, required=False
).add_argument(
    "name", type=str, required=False
).add_argument(
    "role", type=str, required=False
)


@api.route('/')
class UserList(Resource):
    @login_required
    @role_require('admin')
    @api.doc(parser=user_post_parser)
    def post(self):
        args = user_post_parser.parse_args()
        if db.users.find_one({"login": args.login}):
            return f"User with login {args.login} already exists", 400
        result = db.users.insert_one(args)
        return str(result.inserted_id)

    @login_required
    @role_require('admin')
    def get(self):
        return parse_json(db.users.find())


@api.route('/user/<string:id>')
class UserResource(Resource):
    @login_required
    @role_require('admin')
    def get(self, id):
        return parse_json(get_user_by_id(id))

    @login_required
    @role_require('admin')
    def delete(self, id):
        delete_user(id)
        return "Deleted"

    @login_required
    @role_require('admin')
    @api.doc(parser=user_put_parser)
    def put(self, id):
        args = user_put_parser.parse_args()
        args = dict((k, v) for k, v in args.items() if v is not None)
        update_user(id, args)
        return 'Updated'


@api.route('/user/login/<string:login>')
class UserResource(Resource):
    @login_required
    def get(self, login):
        return parse_json(find_user(login))


# Тело для обновления пользователя самим собой
self_put_parser = api.parser(
).add_argument(
    "login", type=str, required=False
).add_argument(
    "password", type=str, required=False
).add_argument(
    "name", type=str, required=False
)


@api.route('/user/self')
class UserResource(Resource):
    @login_required
    @api.doc(parser=self_put_parser)
    def put(self):
        args = user_put_parser.parse_args()
        args = dict((k, v) for k, v in args.items() if v is not None)
        update_user(current_user.get_id(), args)
        return 'Updated'

@api.route('/impex')
class UserResource(Resource):
    def get(self):
        return parse_json(db.users.find({}))

    @login_required
    def post(self):
        new_users = json.load(request.files['users'])
        users_keys = ["_id", "login", "passwod", "name", "state"] # Has user got property "role" ?
        for user in new_users:
            if db.users.find_one({"login": user["login"]}):
                return f"User with login {user["login"]} already exists"
            for k in users_keys:
                if k not in user:
                    return "Not ok"
            del user['_id']
        db.users.insert_many(new_users)
        return "OK"
