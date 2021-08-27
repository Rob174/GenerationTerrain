from typing import Tuple

from main.src.input_data.CoordinateTransformer.RasterCoordinateTransformer import RasterCoordinateTransformer
import numpy as np

class BoundingBox:
    """Bounding box"""

    def __init__(self, upper_left: Tuple[int, int], lower_right: Tuple[int, int],
                 coordinate_transformer: RasterCoordinateTransformer):
        self.upper_left_coord = upper_left
        self.lower_right_coord = lower_right
        self.coordinate_transformer = coordinate_transformer
        transformed_coordinates = np.stack((self.coordinate_transformer.to_px(*upper_left),
                                            self.coordinate_transformer.to_px(*lower_right)))
        self.upper_left_px = np.min(transformed_coordinates, axis=0)
        self.lower_right_px = np.max(transformed_coordinates, axis=0)
        self.shape = self.lower_right_px - self.upper_left_px