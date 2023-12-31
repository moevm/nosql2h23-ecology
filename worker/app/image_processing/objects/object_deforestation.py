import cv2
import numpy as np
from bson import ObjectId

from app import app
from app.db import local
from app.image_processing.objects.object_base import ObjectBase
from app.image_processing.utility import connected_components, find_contours, get_image_RGB


class ObjectDeforestation(ObjectBase):
    '''
    Класс для нахождения вырубок на изображении.
    '''
    def __init__(self, img_id, image_bytes):
        super().__init__(img_id, image_bytes)
        
        self.name = 'Вырубка'
        self.color = 'red'
    
    def find_contours_of_object(self):
        '''
        Использование нейросети для нахождения областей вырубок.
        '''
        image_RGB = get_image_RGB(self.img_id, self.image_bytes)
        shape_image = image_RGB.shape

        resized_image = cv2.resize(image_RGB, (512, 512))
        self.update(10)

        image_norm = resized_image / 255
        prediction = local.deforestation_model.predict(image_norm.reshape(1, 512, 512, 3))
        self.update(20)

        mask = (prediction[0] == 1).astype(np.uint8)

        # Remove white pixels from image (resize to perserve resize errors)
        white_mask = cv2.inRange(resized_image, (255, 255, 255), (255, 255, 255))
        white_mask[white_mask > 0] = 1
        cv2.multiply(mask, 1 - white_mask, mask)
        self.update(5)

        filtered_mask = connected_components(mask)
        image = cv2.resize(filtered_mask, (shape_image[1], shape_image[0]))
        self.update(5)

        contours = find_contours(image)
        self.update(10)
        
        return contours
    
    @staticmethod
    @app.task(name='deforestation_find', queue="image_process")
    def create_and_process(img_id):
        maps_fs = local.maps_fs
        
        # Получаем саму картинку из GridFS.
        image_bytes = maps_fs.find_one(ObjectId(img_id)).read()

        deforestation_object = ObjectDeforestation(img_id, image_bytes)
        ObjectBase.process_object(deforestation_object)
        deforestation_object.filter_polygons_by_area(deforestation_object.max_area / 4)
        deforestation_object.after_end_of_process()
        return "Processing completed"
