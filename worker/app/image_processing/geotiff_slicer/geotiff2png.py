from osgeo import gdal


def geotiffToPng(
        geotiffBytes,
        pngName, 
        optionsList = ['if GTiff', '-ot Byte', '-of PNG', '-b 1', '-b 2', '-b 3', '-scale']
    ):
    """
    Function to convert geotiff file to png.
    - geotiffBytes - byte array of geotiff file for converting.
    - pngName - path to store output png.
    - options - list of options to gdal.Translate.
    """
    gdal.Translate(
        pngName,
        geotiffBytes,
        options=" ".join(optionsList)
    )