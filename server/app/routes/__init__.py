from flask_restx import Api

# from .images_bp import images_bp
# from .anomalies_bp import anomalies_bp
# from .reports_bp import reports_bp
#
# images_api = Api(images_bp)
# anomalies_api = Api(anomalies_bp)
# reports_api = Api(reports_bp)

from .user import api as user_api

api = Api(
    title="Ecology API",
    version="1.0",
    prefix='/api',
    doc='/api/docs'
)

# api.add_namespace(images_api.namespace)
# api.add_namespace(anomalies_api.namespaces)
# api.add_namespace(reports_api.namespaces)
api.add_namespace(user_api)
