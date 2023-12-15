from flask import request
from flask_login import login_required
from flask_restx import Namespace, Resource
from werkzeug.local import LocalProxy
import json

from app.db import get_db
from app.services.objects import bulk_upload_objects
from app.services.user import bulk_upload_users
from app.utils import parse_json

db = LocalProxy(get_db)

api = Namespace("dumps", description="Дампы")


@api.route('/')
class DumpResource(Resource):
    def get(self):
        return parse_json({
            'objects': db.objects.find({}),
            'users': db.users.find({})
        })

    @login_required
    def post(self):
        dump = json.load(request.files['dump'])
        bulk_upload_objects(dump['objects'])
        bulk_upload_users(dump['users'])
        return "Ok"
