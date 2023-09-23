import rasterio.warp
from rasterio.crs import CRS
from rasterio.io import MemoryFile


class CoordintesTransformer:
    '''
    Класс для преобразования координат tif изображения. В конеце использования должен быть вызван метод close.

    geotif_bytes - байтовый массив tif файла.
    '''
    def __init__(self, geotif_bytes: bytes):
        self.image_file = rasterio.MemoryFile(geotif_bytes)
        self.image = self.image_file.open()
        self.lat_long_crs = CRS.from_epsg(4326)
        self.meters_crs = CRS.from_epsg(32724)
        self.image_crs = self.image.crs

        self.width = self.image.width
        self.height = self.image.height

    def pixel_xy_to_lat_long(self, x, y):
        xy_in_image_crs = self.image.xy(y, x)
        if (self.image_crs != self.lat_long_crs):
            long_lat = rasterio.warp.transform(
                self.image_crs,
                self.lat_long_crs,
                [xy_in_image_crs[0]],
                [xy_in_image_crs[1]]
            )
            # return [lattitude, longitude]
            return long_lat[1][0], long_lat[0][0]
        else:
            # return [lattitude, longitude]
            return xy_in_image_crs[1], xy_in_image_crs[0]
        
    def pixel_xy_to_meters(self, x, y):
        xy_in_image_crs = self.image.xy(y, x)
        if (self.image_crs != self.meters_crs):
            meters_x_y = rasterio.warp.transform(
                self.image_crs,
                self.meters_crs,
                [xy_in_image_crs[0]],
                [xy_in_image_crs[1]]
            )
            # return [x, y]
            return meters_x_y[0][0], meters_x_y[1][0]
        else:
            # return [x, y]
            return xy_in_image_crs[0], xy_in_image_crs[1]
    
    def close(self):
        self.image.close()
        self.image_file.close()