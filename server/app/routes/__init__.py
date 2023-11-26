from flask_restx import Api

from .images import api as images_api
from .user import api as user_api
from .auth import api as auth_api
from .objects import api as objects_api

api = Api(
    title="Ecology API",
    version="1.0",
    prefix='/api',
    doc='/api/docs'
)

api.add_namespace(user_api)
api.add_namespace(auth_api)
api.add_namespace(images_api)
api.add_namespace(objects_api)
