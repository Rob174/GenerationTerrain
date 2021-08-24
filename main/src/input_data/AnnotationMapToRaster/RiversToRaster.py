import numpy as np
import json
from pathlib import Path
from typing import Optional, Union

from rich.progress import TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn

from main.FolderInfos import FolderInfos
from main.src.ProgressBar.IterationManager import IterationManager
from main.src.ProgressBar.ProgressBar0 import ProgressBar0
from main.src.input_data.GeotiffOpener import GeotiffOpener
from main.src.input_data.ShapefileReaders.RiversShpFileReader import RiversShpFileReader
from rich import Progress


class RiversToRaster:
    def __init__(self,cache_path: Optional[Union[str,Path]] = None):
        self.dico_lines_per_tiff = {}
        self.cache_path = cache_path
        self.generate()
        self.save()
    def generate(self):
        geotiff_opener = GeotiffOpener()
        shapefile_reader = RiversShpFileReader(FolderInfos.data_raw.joinpath("rivers").joinpath("COURS_D_EAU.shp"))
        self.dico_lines_per_tiff = {}
        progress = ProgressBar0(IterationManager(total=len(geotiff_opener.iter_geotiff())*len(shapefile_reader.get_points())))
        with progress:
            for tiff in geotiff_opener.iter_geotiff():
                self.dico_lines_per_tiff[tiff.current_path] = []
                for points in shapefile_reader.get_points():
                    points_transformed = []
                    for point in points:
                        points_transformed.append(tiff.loc_to_px(point))
                    if 0 in np.max(points,axis=0):
                        continue
                    self.dico_lines_per_tiff[tiff.current_path].append(points_transformed)
                    progress.on_end()
            return self.dico_lines_per_tiff
    def save(self):
        if self.cache_path is None:
            return
        with open(self.cache_path,"w") as fp:
            json.dump(self.dico_lines_per_tiff,fp)

if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)
    r = RiversToRaster(cache_path=FolderInfos.data_raw.joinpath("rivers").joinpath("cache_rivers.json"))
