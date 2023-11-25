from functools import wraps

from flask_login import current_user


def role_require(role):
    def decorator(f):
        @wraps(f)
        def _decorator(*args, **kwargs):
            if current_user and current_user.role == role:
                return f(*args, **kwargs)
            else:
                return 'Unauthorized', 401

        return _decorator

    return decorator
