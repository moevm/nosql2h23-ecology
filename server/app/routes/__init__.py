from flask import Blueprint
from .images_bp import images_bp
from .anomalies_bp import anomalies_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(images_bp, url_prefix="/images")
api_bp.register_blueprint(anomalies_bp, url_prefix="/anomalies")
