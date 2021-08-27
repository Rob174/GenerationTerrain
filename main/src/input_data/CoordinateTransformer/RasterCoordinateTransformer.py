from pathlib import Path
from typing import Union, Iterable

import rasterio as rio

class NoneException(Exception):
    def __init__(self,variable_name: str):
        self.message = f"The variable {variable_name} is set to none"
        super(NoneException, self).__init__(self.message)
class RasterCoordinateTransformer:
    def __init__(self):
        self.source_raster = None
    def set_source(self, source_raster):
        self.source_raster = source_raster

    def to_px(self, point_x: Union[Iterable,float], point_y: Union[Iterable,float]):
        if self.source_raster is None:
            raise NoneException("source_raster")
        points_x,points_y = self.source_raster.index(point_x, point_y)
        return [(x,y) for x,y in zip(points_x,points_y)]
        