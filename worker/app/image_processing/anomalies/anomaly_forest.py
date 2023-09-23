import cv2
from bson import ObjectId

from app import app
from app.db import local
from app.image_processing.anomalies.anomaly_base import AnomalyBase
from app.image_processing.utility import morph_operations, find_contours, get_image_RGB


class AnomalyForest(AnomalyBase):
    '''
    Класс для нахождения леса на изображении.
    '''
    def __init__(self, img_id, image_bytes):
        super().__init__(img_id, image_bytes)
        
        self.name = 'Forest'
        self.color = 'green'
    
    def find_contours_of_anomaly(self):
        '''
        Метод Otsu выделения выделяющихся объектов на изображении. Возвращает контуры найденных объектов.
        '''
        image_RGB = get_image_RGB(self.img_id, self.image_bytes)

        gray = cv2.cvtColor(image_RGB, cv2.COLOR_BGR2GRAY)

        # denoise the image with a Gaussian filter
        blurred_image = cv2.GaussianBlur(gray,(5,5),0)
        self.update(10)

        _, image_result = cv2.threshold(
            blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
        )
        self.update(20)

        # Remove noise and fill holes in the binary image using morphological operations
        closed = morph_operations(image_result, use_gaussian_filter=False)
        self.update(10)

        # Find the contours in the input image
        contours = find_contours(closed)
        self.update(10)

        return contours
    
    @staticmethod
    @app.task(name='forest_find', queue="image_process")
    def create_and_process(img_id):
        db = local.db
        map_fs = local.map_fs
        image_info = db.images.find_one(ObjectId(img_id))

        # Получаем саму картинку из GridFS.
        image_bytes = map_fs.get(ObjectId(image_info['fs_id'])).read()

        forest_anomaly = AnomalyForest(img_id, image_bytes)
        AnomalyBase.process_anomaly(forest_anomaly)
        forest_anomaly.filter_polygons_by_area(10)
        forest_anomaly.after_end_of_process()
        return "Processing completed"
