import json
from flask import request, jsonify, make_response
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource
from werkzeug.local import LocalProxy
from copy import deepcopy

from app.auth.authorization import role_require
from app.db import get_db
from app.services.user import get_user_by_id, find_user, update_user, delete_user, bulk_upload_users
from app.utils import parse_json
from app.services.pagination import format_pagination, create_sort_params, create_filter_params


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
    

@api.route('/table/')
class ImagesForTable(Resource):
    def get(self):
        args = request.args.to_dict()
        format_pagination(args)

        # Переименовываем некоторые поля, которые на сервере называются по-другому.
        for sort_opt in args["sort"]:
            if sort_opt["colId"] == "_id.$oid":
                sort_opt["colId"] = "_id"

        filter_args = deepcopy(args["filter"])
        for filter_key, filter_value in filter_args.items():
            new_key = filter_key
            if filter_key == "_id.$oid":
                new_key = "_id"
            args["filter"].pop(filter_key)
            args["filter"][new_key] = filter_value

        # Формируем запрос.
        query = create_filter_params(args["filter"])
        sort = create_sort_params(args["sort"])

        # Получаем юзеров, которые подходят под все условия, заданные на клиенте.
        if sort: data = parse_json(db.users.find(query)
            .skip(args["start"])
            .limit(args["end"] - args["start"])
            .sort(sort)
        )
        else: data = parse_json(db.users.find(query)
            .skip(args["start"])
            .limit(args["end"] - args["start"])
        )
       
        return make_response(jsonify({
            "rowData": data,
            "end": args["start"] + len(data)
        }) , 200)


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
        bulk_upload_users(new_users)
        return "OK"
