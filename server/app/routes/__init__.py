from flask_restx import Api

from .images_bp import api as images_api
from .user import api as user_api

api = Api(
    title="Ecology API",
    version="1.0",
    prefix='/api',
    doc='/api/docs'
)

api.add_namespace(images_api)
api.add_namespace(user_api)
