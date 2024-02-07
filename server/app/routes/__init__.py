from flask_restx import Api
from flask_restx.apidoc import apidoc

from .images import api as images_api
from .user import api as user_api
from .auth import api as auth_api
from .objects import api as objects_api
from .tiles import api as tiles_api
from .dump import api as dump_api

api = Api(
    title="Ecology API",
    version="1.0",
    prefix='/api',
    doc='/api/docs'
)

apidoc.static_url_path = "/api/docs/swaggerui"

api.add_namespace(user_api)
api.add_namespace(auth_api)
api.add_namespace(images_api)
api.add_namespace(tiles_api)
api.add_namespace(objects_api)
api.add_namespace(dump_api)
