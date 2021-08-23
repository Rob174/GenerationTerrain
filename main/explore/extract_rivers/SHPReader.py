from pathlib import Path
from typing import Tuple, List, Optional

import geopandas as gpd
import numpy as np
import rasterio as rio


class CoordinateTransformer:
    def __init__(self, source_raster: Path):
        self.source_raster = rio.open(source_raster)

    def to_px(self, point_x, point_y):
        return self.source_raster.index(point_x, point_y)


class BoundingBox:
    """Bounding box"""

    def __init__(self, upper_left: Tuple[int, int], lower_right: Tuple[int, int],
                 coordinate_transformer: CoordinateTransformer):
        self.upper_left_coord = upper_left
        self.lower_right_coord = lower_right
        self.coordinate_transformer = coordinate_transformer
        transformed_coordinates = np.stack((self.coordinate_transformer.to_px(*upper_left),
                                            self.coordinate_transformer.to_px(*lower_right)))
        self.upper_left_px = np.min(transformed_coordinates, axis=0)
        self.lower_right_px = np.max(transformed_coordinates, axis=0)
        self.shape = self.lower_right_px - self.upper_left_px


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def to_hex(self):
        s = ""
        for c in (self.r, self.g, self.b):
            s += str(hex(c))[2:]
        return s


from PIL import Image, ImageDraw


class LineDrawer:
    def __init__(self, transformer: CoordinateTransformer, thickness: int, color: Color):
        self.thickness = thickness
        self.transformer = transformer
        self.color = color

    def draw(self, points: List[Tuple[int, int]], bounding_box: BoundingBox, layer: Optional[np.ndarray]):
        assert layer is None or (
                    type(layer) is np.ndarray and len(layer.shape) == 3 and layer.shape[-1] == 3), "Wrong type of layer"
        if layer is None:
            layer = np.zeros((*bounding_box.shape, 3), dtype=np.uint8)
        for i in range(len(points)):
            points[i] = self.transformer.to_px(*points[i])
        img = Image.fromarray(layer)
        draw = ImageDraw.ImageDraw(img)  # draw the base i
        draw.line(points, fill=self.color.to_hex(), width=self.thickness)
        return img


class ShpFileReader:
    def __init__(self, source_file: Path):
        self.source_file = source_file

    def get_points(self):
        shapefile = gpd.read_file(self.source_file)
        for shape in shapefile.geometry:
            yield list(zip(*shape.xy))
