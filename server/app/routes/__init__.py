from flask import Blueprint
from .maps_bp import maps_bp
from .objects_bp import objects_bp
from .tiles_bp import tiles_bp
from .users_bp import users_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(users_bp, url_prefix="/users")
api_bp.register_blueprint(maps_bp, url_prefix="/maps")
api_bp.register_blueprint(tiles_bp, url_prefix="/tiles")
api_bp.register_blueprint(objects_bp, url_prefix="/objects")
