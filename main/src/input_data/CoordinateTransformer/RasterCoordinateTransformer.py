from pathlib import Path
import rasterio as rio


class RasterCoordinateTransformer:
    def __init__(self, source_raster: Path):
        self.source_raster = rio.open(source_raster)

    def to_px(self, point_x, point_y):
        return self.source_raster.index(point_x, point_y)
        