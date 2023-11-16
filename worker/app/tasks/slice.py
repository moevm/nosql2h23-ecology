import multiprocessing
import os
from bson.objectid import ObjectId
from app import app
from app.image_processing.geotiff_slicer.slice2tiles import sliceToTiles
from celery.utils.log import get_task_logger
from app.db import local

logger = get_task_logger(__name__)


@app.task(name='slice', queue="slice")
def slice(map_id: str):
    """
    Нарезать geotiff в базе данных с индексом id на кусочки и положить их в gridfs с именем
    <image_name>_<z>_<x>_<y>.png
    """
    db = local.db
    maps_fs = local.maps_fs
    tiles_fs = local.tiles_fs
    redis = local.redis

    # Получаем запись из бд с информацией по изображению.
    map_file = maps_fs.files.find_one(ObjectId(map_id))

    # Получаем саму картинку из GridFS.
    #image_bytes = maps_fs.get(map_file['fs_id']).read()

    slicers = len(redis.keys('slice_queue:*'))

    # Нарезаем на фрагменты.
    sliceToTiles(
        map_id, map_file.read(), f'./{map_id}',
        optionsSliceToTiles={"nb_processes": max(1, multiprocessing.cpu_count() // (1 + slicers))}
    )

    # Удаляем фрагменты, если они уже были в GridFS.
    cursor = tiles_fs.find({"image_id": map_id})
    for document in cursor:
        tiles_fs.delete(document["_id"])

    # Добавляем все фрагменты в GridFS.
    for root, _, files in os.walk(map_id):
        path = root.split(os.sep)
        for file in files:
            # Сами фрагменты лежат по пути /{z}/{x}/{y}.png, но нужно отсечь доп. файлы
            # с информацией о геолокации в корне папки.
            if len(path) >= 2:
                with open(root + "/" + file, "rb") as f:
                    file_content = f.read()
                    tiles_fs.put(
                        file_content,
                        metadata={
                            "image_id": ObjectId(map_id),
                            "z": int(path[1]),
                            "x": int(path[2]),
                            "y": int(file.split('.')[0])
                        }
                    )

    # Добавляем данные для отображения изображения.
    with open(f'{map_id}/tilemapresource.xml', "r") as f:
        xml_content = f.read()
        maps_fs.files.update_one({"_id": map_file["_id"]}, {"$set": {"tile_map_resource": xml_content}})

    # Удаляем временную папку с слайсами.
    for root, dirs, files in os.walk(map_id, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(map_id)

    redis.delete(f'slice_queue:{map_id}')
    maps_fs.files.update_one({"_id": map_file["_id"]}, {"$set": {"sliced": True}})

    return "Done"
