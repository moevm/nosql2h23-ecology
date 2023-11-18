from flask_login import login_user, login_required, current_user, logout_user
from flask_restx import Namespace, Resource
from werkzeug.local import LocalProxy

from app.auth.User import User
from app.db import get_db

api = Namespace("auth", description="Аутентификация")

db = LocalProxy(get_db)

auth_parser = api.parser(
).add_argument(
    "login", type=str, required=True
).add_argument(
    "password", type=str, required=True
)


# TODO заменить password на хэш
@api.route('/login')
class Login(Resource):
    @api.doc(parser=auth_parser)
    def post(self):
        args = auth_parser.parse_args()
        user = db.users.find_one({"login": args.login})
        if not user:
            return f'No user with login {args.login}', 404
        elif args.password != user['password']:
            return 'Incorrect password', 400
        else:
            login_user(User(user), remember=True)
            return 'Ok', 200

    @login_required
    def get(self):
        print(current_user)
        return f'Logged in'

    def delete(self):
        logout_user()
        return 'Logged out'


@api.route('/login/dev')
class Login(Resource):
    def post(self):
        return "Admin Login"
