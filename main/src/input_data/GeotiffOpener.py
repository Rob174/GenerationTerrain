from typing import Tuple

from main.FolderInfos import FolderInfos
import rasterio as rio


class GeotiffOpener:
    def __init__(self):
        self.base_path = FolderInfos.data_raw.joinpath("elevation").joinpath("geotiff")
        self.current_rio_object = None
        self.current_path = None

    def iter_geotiff(self):
        for path in self.base_path.iterdir():
            self.current_rio_object = rio.open(path)
            self.current_path = path
            yield self

    def loc_to_px(self, point: Tuple[float, float]):
        return self.current_rio_object.index(*point)
