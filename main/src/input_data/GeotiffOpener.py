from typing import Tuple

from main.FolderInfos import FolderInfos
import rasterio as rio


class GeotiffOpener:
    def __init__(self):
        self.base_path = FolderInfos.data_raw.joinpath("elevation").joinpath("geotiff")
        self.current_rio_object = None
        self.current_path = None

    def iter_geotiff(self,start:int,stop:int):
        assert type(start) is int, f"start is not int but {type(start)}"
        assert type(stop) is int, f"stop is not int but {type(stop)}"
        pathes = list(self.base_path.iterdir())
        for path in pathes[start:stop]:
            self.current_rio_object = rio.open(path)
            self.current_path = path
            yield self
    def __len__(self):
        return len(list(self.base_path.iterdir()))
    def loc_to_px(self, point: Tuple[float, float]):
        return self.current_rio_object.index(*point)
