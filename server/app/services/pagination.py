import json


def format_pagination(args):
    args["start"], args["end"] = int(args["start"]), int(args["end"])
    # Переводим параметры сортировки в нужный формат.
    args["sort"] = json.loads(args["sort"])
    # Переводим параметры фильтрации в нужный формат.
    args["filter"] = json.loads(args["filter"])