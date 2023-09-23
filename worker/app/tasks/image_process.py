from bson import ObjectId

from app import app
from app.db import local
from app.image_processing.anomalies.anomaly_forest import AnomalyForest
from app.image_processing.anomalies.anomaly_deforestation import AnomalyDeforestation


@app.task(name='image_process', queue="image_process")
def process_image(img_id: str):
    db = local.db
    redis = local.redis
    image_info = db.images.find_one(ObjectId(img_id))
    
    # 
    ## Список аномалий для поиска
    anomalies = [AnomalyForest, AnomalyDeforestation]
    ## 
    # 

    # Создаем запись в redis-е для отображения очереди на клиенте.
    queue_item = f'queue:{img_id}'
    redis.hset(queue_item, mapping={
        'id': str(img_id),
        'progress': 0,
        'name': image_info['name'],
        'uploadDate': image_info['upload_date'],
        'status': 'enqueued',
        'processing_functions_immut': len(anomalies),
        'processing_functions': len(anomalies)
    })
    redis.hset(queue_item, 'status', 'processing')

    # Запуск обработчиков аномалий.
    for anomaly_class in anomalies:
        anomaly_class.create_and_process.delay(img_id)

    return "Done"