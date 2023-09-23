from pymongo import MongoClient
from redis import Redis

from pprint import pprint


def connect_to_mongo(url, port):
    # Подключение к базе данных монго.
    client = MongoClient(url, port)

    db = client.get_database("test")

    print("-"*100)
    print("Mongo. Подключение к базе данных успешно.")
    return db.hello_world


def insert_document_mongo(collection):
    # Вставка документа в коллекцию hello_world базы данных test.
    doc = {"text": "hello world!", "project": "ecology"}
    doc_id = collection.insert_one(doc).inserted_id

    # Вывод элемента с id doc_id в коллекции hello_world.
    print("-"*100)
    print("Mongo. Вставленный в коллекцию hello_world документ:")
    pprint(collection.find_one(doc_id))


def drop_collection_mongo(collection):
    # Удаляем коллекцию hell_world.
    collection.drop()

    # Проверяем, что она пустая, после удаления всех элементов.
    print("-"*100)
    print("Mongo. Количество документов в коллекции hello_world после удаления:", end=" ")
    pprint(collection.count_documents({}))


def connect_to_redis(url, port):
    redis = Redis(host=url, port=port)
    print("-"*100)
    print("Redis. Подключение к базе данных успешно.")
    return redis


def set_and_get_element_redis(redis):
    # set элемент в виде словаря.
    redis.hset('map:1234', mapping={
        'anomalies': 300,
        "size": 12400
    })

    # get получить все поля положенного словаря по ключу.
    print("-"*100)
    print("Redis. get положенного ранее элемента")
    pprint(redis.hgetall('map:1234'))


if __name__ == "__main__":
    url = "localhost"
    mongo_port = 27017
    redid_port = 6379

    hello_world_collection = connect_to_mongo(url, mongo_port)
    insert_document_mongo(hello_world_collection)
    drop_collection_mongo(hello_world_collection)

    redis = connect_to_redis(url, redid_port)
    set_and_get_element_redis(redis)
