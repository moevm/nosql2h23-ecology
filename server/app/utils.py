import json

from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))
