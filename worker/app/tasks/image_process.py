from bson import ObjectId

from app import app
from app.db import local
from app.image_processing.objects.object_forest import ObjectForest
from app.image_processing.objects.object_deforestation import ObjectDeforestation


@app.task(name='image_process', queue="image_process")
def process_image(map_id: str):
    db = local.db
    redis = local.redis
    
    map_info = db.maps.files.find_one(ObjectId(map_id))
    
    # 
    ## Список объектов для поиска
    objects = [ObjectForest, ObjectDeforestation]
    ## 
    # 

    # Создаем запись в redis-е для отображения очереди на клиенте.
    queue_item = f'queue:{map_id}'
    redis.hset(queue_item, mapping={
        'id': map_id,
        'progress': 0,
        'name': map_info['name'],
        'uploadDate': map_info['update']["datetime"],
        'status': 'enqueued',
        'processing_functions_immut': len(objects),
        'processing_functions': len(objects)
    })
    redis.hset(queue_item, 'status', 'processing')

    # Запуск обработчиков объектов.
    for object_class in objects:
        object_class.create_and_process.delay(map_id)

    return "Done"