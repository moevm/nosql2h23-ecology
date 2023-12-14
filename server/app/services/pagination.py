import re
import json
import arrow
from bson.objectid import ObjectId
from bson.errors import InvalidId


def format_pagination(args):
    args["start"], args["end"] = int(args["start"]), int(args["end"])
    # Переводим параметры сортировки в нужный формат.
    args["sort"] = json.loads(args["sort"])
    # Переводим параметры фильтрации в нужный формат.
    args["filter"] = json.loads(args["filter"])


def create_sort_params(sort_args):
    sort_params = []
    for sort_arg in sort_args:
        sort_params.append((sort_arg["colId"], 1 if sort_arg["sort"] == "asc" else -1))
    return sort_params


def create_filter_params(filter_args):
    filter_params = {}
    for filter_field, filter_args in filter_args.items():
        if filter_args["filterType"] == "date":
            filter_args["dateFrom"] = filter_args["dateFrom"].split(" ")[0]
            if filter_args["type"] == "equal":
                filter_params[filter_field] = {"$regex": re.escape(filter_args["dateFrom"])}
            elif filter_args["type"] == "lessThan":
                filter_params[filter_field] = {"$lt": filter_args["dateFrom"]}
            elif filter_args["type"] == "greaterThan":
                filter_params[filter_field] = {"$gt": filter_args["dateFrom"]}

        elif filter_args["filterType"] == "text":
            if filter_args["type"] == "contains":
                filter_params[filter_field] = {"$regex": re.escape(filter_args["filter"])}
            elif filter_args["type"] == "notContains":
                filter_params[filter_field] = {"$not": {"$regex": re.escape(filter_args["filter"])}}
            elif filter_args["type"] == "equal":
                try:
                    filter_args["filter"] = ObjectId(filter_args["filter"])
                except InvalidId:
                    pass
                filter_params[filter_field] = filter_args["filter"]

    return filter_params