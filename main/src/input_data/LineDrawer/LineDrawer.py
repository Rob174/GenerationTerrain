from typing import List, Tuple, Optional

from PIL import Image, ImageDraw

from main.src.input_data.CoordinateTransformer.RasterCoordinateTransformer import RasterCoordinateTransformer
from main.src.input_data.BoundingBox.BoundingBox import BoundingBox
from main.src.input_data.ColorManager.Color import Color
import numpy as np

from main.FolderInfos import FolderInfos
from main.src.input_data.GeotiffOpener import GeotiffOpener
from main.src.input_data.ShapefileReaders.RiversShpFileReader import RiversShpFileReader


class LineDrawer:
    def __init__(self, transformer: RasterCoordinateTransformer, thickness: int, color: Color):
        self.thickness = thickness
        self.transformer = transformer
        self.color = color

    def draw(self, points: List[Tuple[int, int]], bounding_box: BoundingBox, layer: Optional[Image.Image],draw: Optional[ImageDraw.ImageDraw]):
        if layer is None:
            layer = np.zeros((*bounding_box.shape, 3), dtype=np.uint8)
            layer = Image.fromarray(layer)
            draw = ImageDraw.ImageDraw(layer)
        for i in range(len(points)):
            points[i] = self.transformer.to_px(*points[i])
        draw.line(points, fill=self.color.to_hex(), width=self.thickness)
        return layer,draw
if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)



