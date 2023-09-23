from app.image_processing.find_forest.helpers import find_contours, connected_components
import numpy as np
import cv2
from app.db import local


def find_deforestation(image_RGP, update):
    shape_image = image_RGP.shape
    resized_image = cv2.resize(image_RGP, (512, 512))
    update(1)
    image_norm = resized_image / 255
    prediction = local.deforestation_model.predict(image_norm.reshape(1, 512, 512, 3))
    update(1)
    mask = (prediction[0] == 1).astype(np.uint8)
    # denoised_img = morph_operations(mask)
    filtered_mask = connected_components(mask)
    image = cv2.resize(filtered_mask, (shape_image[1], shape_image[0]))
    update(1)
    contour_img = find_contours(image)
    update(1)

    return contour_img
