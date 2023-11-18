from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, mongo_data):
        for key, value in mongo_data.items():
            setattr(self, key, value)

    def get_id(self):
        return str(self._id)
