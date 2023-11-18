import cv2
import arrow
from typing import List, Any
from bson import ObjectId

from app.image_processing.coordinates_transform.transform_coordinates import CoordintesTransformer
from app.db import local


class ObjectBase:
    '''
    Базовый класс для нахождения объектов одного типа.
    '''
    def __init__(self, img_id, image_bytes):
        self.img_id = img_id
        self.image_bytes = image_bytes
        self.polygons = []
        self.area = []
        
        self.name = "Base Object"
        self.color = "black"

        redis = local.redis
        queue_item = f'queue:{img_id}'
        num_objects = int(redis.hget(queue_item, 'processing_functions_immut'))
        self.update = lambda x: redis.hset(queue_item, 
            'progress', float(redis.hget(queue_item, 'progress')) + (x/num_objects)
        )

    def find_contours_of_object(self) -> List[List[Any]]:
        '''
        Метод, который находит контуры объектов на изображении и возвращает список списков точек.
        '''
        pass

    def find_geo_polygons(self, contours_of_object):
        '''
        Метод, который преобразовывает контуры объекты в геопривязанные контуры и 
        сохраняет их в поле polygons класса.
        '''
        coord_transformer = CoordintesTransformer(self.image_bytes)

        step_progress = 35 / (len(contours_of_object) + 1)

        self.polygons = []
        for line in contours_of_object:
            # Преобразовываем координаты каждой точки из пикселей в широту и долготу.
            line_arr = []

            for point in line:
                x_pix, y_pix = point[0]
                line_arr.append(coord_transformer.pixel_xy_to_lat_long(x_pix, y_pix))
            self.polygons.append(line_arr)
            self.update(step_progress)

        coord_transformer.close()

    def __find_spatial_resolution(self):
        '''
        Метод, который находит разрешение изображения в метрах 
        (сколько метров в одном пикселе).
        '''
        coord_transf = CoordintesTransformer(self.image_bytes)

        width = coord_transf.width
        height = coord_transf.height

        left_up = coord_transf.pixel_xy_to_meters(0, 0)
        right_down = coord_transf.pixel_xy_to_meters(width - 1, height - 1)

        coord_transf.close()

        return abs(right_down[0] - left_up[0]) / width, abs(right_down[1] - left_up[1]) / height

    def find_area(self, contours):
        '''
        Метод, который находит площадь каждой объекты заданного типа.
        '''
        sptial_res = self.__find_spatial_resolution()

        step_progress = 15 / (len(contours) + 1)

        self.area = []
        for polygon in contours:
            # Находим площадь в пикселях и умножаем на разрешение каждого пикселя.
            area = cv2.contourArea(polygon) * sptial_res[0] * sptial_res[1]
            self.area.append(area)
            self.update(step_progress)

    def filter_polygons_by_area(self, min_area):
        '''
        Метод, который фильтрует найденные объекты и удаляет те, 
        площадь которых меньше, чем минимальная площадь (min_area).
        '''
        i = 0
        while i < len(self.area):
            if (self.area[i] < min_area):
                self.area.pop(i)
                self.polygons.pop(i)
            else:
                i += 1

    @staticmethod
    def create_and_process(img_id):
        '''
        Метод, который создает объект необходимого класса объекты, выполняет её поиск (process_object) 
        и сохранение в базе данных (after_end_of_process)
        '''
        pass

    @staticmethod
    def process_object(object):
        '''
        Полный поиск объекты и сохранение в базе данных.

        object - один из наследников класса ObjectBase.
        '''
        contours = object.find_contours_of_object()
        object.find_geo_polygons(contours)
        object.find_area(contours)
    
    def after_end_of_process(self):
        '''
        Метод, который сохраняет объект найденные объекты одного типа в базу данных.
        '''
        db = local.db
        redis = local.redis
        image_info = db.images.find_one(ObjectId(self.img_id))
        queue_item = f'queue:{self.img_id}'
        
        if (len(self.polygons) > 0):
            # Формируем словарь найденных объектов.
            object_dict = {
                'name': self.name,
                'color': self.color,
                'polygons': self.polygons,
                'area': self.area
            }

            # Добавляем словарь найденных объектов в базу данных.
            objects_list = image_info['objects']
            objects_list.append(object_dict)
            db.images.update_one({"_id": image_info['_id']}, {"$set": {"objects": objects_list}})
            db.images.update_one({"_id": image_info['_id']}, {"$set": {"detect_date": str(arrow.now().to('UTC'))}})

        # Удаляем запись в redis-е, если обработки всех объектов завершились.
        redis.hset(queue_item, 'processing_functions', int(redis.hget(queue_item, 'processing_functions')) - 1)
        if int(redis.hget(queue_item, 'processing_functions')) == 0:
            redis.delete(queue_item)
            db.images.update_one({"_id": image_info['_id']}, {"$set": {"ready": True}})

    def get_object_by_index(self, index):
        '''
        Метод, который возвращает одну объект из найденных на изображении.
        '''
        return {
            'index': index,
            'polygon': self.polygons[index],
            'area': self.area[index]
        }
