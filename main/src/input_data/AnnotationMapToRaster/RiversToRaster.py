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


class RiversToRaster:
    def __init__(self,cache_path: Optional[Union[str,Path]] = None):
        self.dico_lines_per_tiff = {}
        self.cache_path = cache_path
    def generate(self,start:int,stop:int):
        FolderInfos.init(test_without_data=True)
        geotiff_opener = GeotiffOpener()
        shapefile_reader = RiversShpFileReader(FolderInfos.data_raw.joinpath("rivers").joinpath("COURS_D_EAU.shp"))
        dico_lines_per_tiff = {}
        size = stop-start+1
        list_points = list(shapefile_reader.get_points())
        size *= len(list_points)
        progress = ProgressBar0(IterationManager(total=size))
        with progress:
            for tiff in geotiff_opener.iter_geotiff(start=start,stop=stop):
                dico_lines_per_tiff[tiff.current_path] = []
                for points in list_points:
                    points_transformed = []
                    for point in points:
                        points_transformed.append(tiff.loc_to_px(point))
                    if 0 in np.max(points,axis=0):
                        continue
                    dico_lines_per_tiff[tiff.current_path].append(points_transformed)
                    progress.on_end()
        with open(FolderInfos.data_raw.joinpath("rivers").joinpath(f"from_{start}_to_{stop}.json")) as fp:
            json.dump(dico_lines_per_tiff,fp)
        return None
    def len_geotiff(self):
        return len(GeotiffOpener())
    def save(self):
        if self.cache_path is None:
            return
        with open(self.cache_path,"w") as fp:
            json.dump(self.dico_lines_per_tiff,fp)

import multiprocessing as mp
if __name__ == '__main__':
    num_cpu = mp.cpu_count()//2
    pool = mp.Pool(num_cpu)
    FolderInfos.init(test_without_data=True)
    r = RiversToRaster()
    nb_elem = r.len_geotiff()
    split_ids = [int(v) for v in np.linspace(0,nb_elem,num_cpu*16)]

    results = [pool.apply(RiversToRaster().generate, args=(start,stop)) for start,stop in zip(split_ids[:-1],split_ids[1:])]
    pool.close()
    s=0

