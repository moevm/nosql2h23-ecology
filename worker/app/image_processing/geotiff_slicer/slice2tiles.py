import gdal2tiles
from osgeo import gdal


# -b это слой, который берем, порядок слоев 1, 2, 3 так как sample.tif в формате rgb.
def sliceToTiles(
        geotiffName,
        geotiffBytes,
        slicesOutputPath,
        optionsTranslate=['-if GTiff', '-ot Byte', '-b 1', '-b 2', '-b 3', '-of vrt', '-scale'],
        optionsSliceToTiles={"nb_processes": 1}
):
    """
    Function that prepares and cuts a geotiff file into fragments that are available for display in leaflet.js.
    - geotiffName - name of geotiff file for preparing and slicing.
    - geotiffBytes - byte array of geotiff file for preparing and slicing.
    - optionsTranslate - list of options for gdal_translate (Translate options to convert 16 bit images to 8 bit).
    - optionsSliceToTiles - dict of options for slicing (for gdal2tiles).
    """
    gdal.FileFromMemBuffer(f"/vsimem/{geotiffName}.tiff", geotiffBytes)
    image = gdal.Open(f"/vsimem/{geotiffName}.tiff")

    gdal.Translate(f'/vsimem/{geotiffName}.vrt', image, options=" ".join(optionsTranslate))
    gdal2tiles.generate_tiles(f'/vsimem/{geotiffName}.vrt', slicesOutputPath, **optionsSliceToTiles)

    gdal.Unlink(f'/vsimem/{geotiffName}.vrt')
    gdal.Unlink(f"/vsimem/{geotiffName}.tiff")
