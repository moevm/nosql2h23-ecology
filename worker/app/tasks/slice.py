import multiprocessing
import os
from bson.objectid import ObjectId

from app import app
from app.image_processing.geotiff_slicer.slice2tiles import sliceToTiles
from app.image_processing.utility import parse_xml_slice
from celery.utils.log import get_task_logger
from app.db import local
from app import config


logger = get_task_logger(__name__)

@app.task(name='slice', queue="slice")
def slice(image_id: str):
    """
    Нарезать geotiff в базе данных с индексом id на кусочки и положить их в gridfs с именем
    <image_name>_<z>_<x>_<y>.png
    """
    db = local.db
    maps_fs = local.maps_fs
    tiles_fs = local.tiles_fs
    redis = local.redis

    # Получаем саму картинку из GridFS.
    image_bytes = maps_fs.get(ObjectId(image_id)).read()

    slicers = len(redis.keys('slice_queue:*'))

    # Нарезаем на фрагменты.
    sliceToTiles(
        image_id, image_bytes, f'./{image_id}',
        optionsSliceToTiles= {
            "nb_processes": max(1, multiprocessing.cpu_count() // (1 + slicers)),
            "zoom": [config.MIN_ZOOM, config.MAX_ZOOM]
        }
    )

    # Удаляем фрагменты, если они уже были в GridFS.
    for document in tiles_fs.find({"image_id": image_id}):
        tiles_fs.delete(document["_id"])

    # Добавляем все фрагменты в GridFS.
    for root, _, files in os.walk(image_id):
        path = root.split(os.sep)
        for file in files:
            # Сами фрагменты лежат по пути /{z}/{x}/{y}.png, но нужно отсечь доп. файлы
            # с информацией о геолокации в корне папки.
            if len(path) >= 2:
                with open(root + "/" + file, "rb") as f:
                    file_content = f.read()
                    tiles_fs.put(
                        file_content,
                        image_id = ObjectId(image_id),
                        z = int(path[1]),
                        x = int(path[2]),
                        y = int(file.split('.')[0])
                    )

    # Добавляем данные для отображения изображения.
    coordinates = parse_xml_slice(f'{image_id}/tilemapresource.xml')
    center = [0, 0]
    for i in range(len(coordinates)):
        center[0] += coordinates[i][0]
        center[1] += coordinates[i][1]
    # Переворачиваем координаты из [lat, lng] получаем [lng, lat]
    center[1], center[0] = center[0] / 4, center[1] / 4
    # coordinates в порядке [lat, lng]
    db.maps.files.update_one({"_id": ObjectId(image_id)}, {"$set": {"coordinates": coordinates, "center": center}})

    # Удаляем временную папку со слайсами.
    for root, dirs, files in os.walk(image_id, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(image_id)

    redis.delete(f'slice_queue:{image_id}')
    db.maps.files.update_one({"_id": ObjectId(image_id)}, {"$set": {"sliced": True}})

    return "Done"
