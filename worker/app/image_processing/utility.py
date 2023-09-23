import cv2
import numpy as np
from osgeo import gdal


def get_image_RGB(image_name, geotif_bytes):
    '''
    Преобразовывает tif файл в 3-х канальное 8-битное изображение и возвращает его, как массив numpy.

    geotif_bytes - путь до tif файла.
    '''
    gdal.FileFromMemBuffer("/vsimem/" + image_name, geotif_bytes)
    image = gdal.Open("/vsimem/" + image_name)

    # As, there are 3 bands, we will store in 3 different variables
    band_1 = image.GetRasterBand(1)  # red channel
    band_2 = image.GetRasterBand(2)  # green channel
    band_3 = image.GetRasterBand(3)  # blue channel

    b1 = band_1.ReadAsArray()
    b2 = band_2.ReadAsArray()
    b3 = band_3.ReadAsArray()

    # Normalize input image to range [0, 255]
    normalized_b1 = cv2.normalize(b1, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    normalized_b2 = cv2.normalize(b2, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    normalized_b3 = cv2.normalize(b3, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    del image
    gdal.Unlink("/vsimem/" + image_name)

    return np.dstack((normalized_b1, normalized_b2, normalized_b3))


def morph_operations(image_arr, use_gaussian_filter: bool = True):
    if use_gaussian_filter:
        # denoise the image with a Gaussian filter
        image_arr = cv2.GaussianBlur(image_arr, (5, 5), 0)

    # Remove noise and fill holes in the binary image using morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    return cv2.morphologyEx(image_arr, cv2.MORPH_OPEN, kernel)


def connected_components(threshold, connectivity=8):
    # perform connected component analysis
    # apply connected component analysis to the thresholded image
    output = cv2.connectedComponentsWithStats(threshold, connectivity, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    # initialize an output mask to store all forests parsed from
    # the image
    mask = np.zeros(threshold.shape, dtype="uint8")
    # loop over the number of unique connected component labels

    for i in range(1, numLabels):
        # extract the connected component statistics and centroid for the current label
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        # ensure the width, height, and area are all neither too small
        # nor too big
        keepWidth = w > 50
        keepHeight = h > 50
        keepArea = area > 250
        # (cX, cY) = centroids[i]
        # ensure the connected component we are examining passes all
        # three tests
        if all((keepWidth, keepHeight, keepArea)):
            mask[y:y + h, x:x + w, :] = threshold[y:y + h, x:x + w, :]
    return mask


def find_contours(thresh):
     # Find the contours in the input image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    # Аппроксимируем контур, чтобы уменьшить число точек.
    contours_approx = []
    for line in contours:
        # Преобразовываем координаты каждой точки из пикселей в широту и долготу.
        eps = 0.0001 * cv2.arcLength(line, True)
        line_approx = cv2.approxPolyDP(line, eps, True)
        contours_approx.append(line_approx)
    return contours_approx
