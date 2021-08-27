from pathlib import Path
import rasterio as rio

class NoneException(Exception):
    def __init__(self,variable_name: str):
        self.message = f"The variable {str} is set to none"
        super(NoneException, self).__init__(self.message)
class RasterCoordinateTransformer:
    def __init__(self):
        self.source_raster = None
    def set_source(self, source_raster):
        self.source_raster = source_raster

    def to_px(self, point_x, point_y):
        if self.source_raster is None:
            raise NoneException("source_raster")
        return self.source_raster.index(point_x, point_y)
        