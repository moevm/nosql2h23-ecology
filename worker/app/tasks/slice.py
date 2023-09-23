import multiprocessing
import os
from bson.objectid import ObjectId
from app import app
from app.image_processing.geotiff_slicer.slice2tiles import sliceToTiles
from celery.utils.log import get_task_logger
from app.db import local

logger = get_task_logger(__name__)


@app.task(name='slice', queue="slice")
def slice(img_id: str):
    """
    Нарезать geotiff в базе данных с индексом id на кусочки и положить их в gridfs с именем
    <image_name>_<z>_<x>_<y>.png
    """
    db = local.db
    map_fs = local.map_fs
    tile_fs = local.tile_fs
    redis = local.redis

    # Получаем запись из бд с информацией по изображению.
    image_info = db.images.find_one(ObjectId(img_id))

    # Получаем саму картинку из GridFS.
    image_bytes = map_fs.get(image_info['fs_id']).read()

    slicers = len(redis.keys('slice_queue:*'))

    # Нарезаем на фрагменты.
    sliceToTiles(
        img_id, image_bytes, f'./{img_id}',
        optionsSliceToTiles={"nb_processes": max(1, multiprocessing.cpu_count() // (1 + slicers))}
    )

    # Удаляем фрагменты, если они уже были в GridFS.
    cursor = tile_fs.find({"image_id": img_id})
    for document in cursor:
        tile_fs.delete(document["_id"])

    # Добавляем все фрагменты в GridFS.
    for root, _, files in os.walk(img_id):
        path = root.split(os.sep)
        for file in files:
            # Сами фрагменты лежат по пути /{z}/{x}/{y}.png, но нужно отсечь доп. файлы
            # с информацией о геолокации в корне папки.
            if len(path) >= 2:
                with open(root + "/" + file, "rb") as f:
                    file_content = f.read()
                    tile_fs.put(
                        file_content,
                        image_id=ObjectId(img_id),
                        z=int(path[1]),
                        x=int(path[2]),
                        y=int(file.split('.')[0])
                    )

    # Добавляем данные для отображения изображения.
    with open(f'{img_id}/tilemapresource.xml', "r") as f:
        xml_content = f.read()
        db.images.update_one({"_id": image_info["_id"]}, {"$set": {"tile_map_resource": xml_content}})

    # Удаляем временную папку с слайсами.
    for root, dirs, files in os.walk(img_id, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(img_id)

    redis.delete(f'slice_queue:{img_id}')
    db.images.update_one({"_id": image_info["_id"]}, {"$set": {"sliced": True}})

    return "Done"
