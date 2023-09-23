import numpy as np
import cv2 as cv

def findContoursInFile(hsv_min, hsv_max, fn):
    img = cv.imread(fn)

    hsv = cv.cvtColor( img, cv.COLOR_BGR2HSV ) #BGR на HSV
    thresh = cv.inRange( hsv, hsv_min, hsv_max ) # применяем цветовой фильтр
    contours, hierarchy = cv.findContours( thresh.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # отображаем контуры поверх изображения
    cv.drawContours( img, contours, -1, (255,0,0), 1, cv.LINE_AA, hierarchy, 1 )
    cv.imwrite(fn[:len(fn)-4] + '_1.jpg', img)

    #cv.imshow('contours', img) # выводим итоговое изображение в окно
    #cv.waitKey()
    #cv.destroyAllWindows()

# параметры цветового фильтра для поиска просек
hsv_min = np.array((0, 0, 0), np.uint8)
hsv_max = np.array((70, 255, 255), np.uint8)
filename = 'forest2.jpg'
findContoursInFile(hsv_min, hsv_max, filename)

