from typing import List, Tuple, Optional

from PIL import Image, ImageDraw

from main.explore.input_data_processors import CoordinateTransformer
from main.explore.input_data_processors.BoundingBox.BoundingBox import BoundingBox
from main.explore.input_data_processors.ColorManager.Color import Color
import numpy as np

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
        draw = ImageDraw.ImageDraw(img)
        draw.line(points, fill=self.color.to_hex(), width=self.thickness)
        return img
        