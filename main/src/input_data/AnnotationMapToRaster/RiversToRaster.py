import PIL
import numpy as np
import json
from pathlib import Path
from typing import Optional, Union

from rich.progress import TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn

from main.FolderInfos import FolderInfos
from main.src.ProgressBar.IterationManager import IterationManager
from main.src.ProgressBar.ProgressBar0 import ProgressBar0
from main.src.input_data.BoundingBox.BoundingBox import BoundingBox
from main.src.input_data.ColorManager.Color import Color
from main.src.input_data.CoordinateTransformer.RasterCoordinateTransformer import RasterCoordinateTransformer
from main.src.input_data.GeotiffOpener import GeotiffOpener
from main.src.input_data.LineDrawer.LineDrawer import LineDrawer
from main.src.input_data.ShapefileReaders.RiversShpFileReader import RiversShpFileReader
from h5py import File
class FactoryRiversExtractor:
    def create(self):
        FolderInfos.init(test_without_data=True)
        geotiff_opener = GeotiffOpener()
        shapefile_reader = RiversShpFileReader(FolderInfos.data_raw.joinpath("rivers").joinpath("COURS_D_EAU.shp"))
        line_drawer = LineDrawer(transformer=RasterCoordinateTransformer(), thickness=10, color=Color(r=0, g=0, b=255))
        return line_drawer,shapefile_reader,geotiff_opener,

class RiversToRaster:
    def __init__(self, line_drawer: LineDrawer,shapefile_reader:RiversShpFileReader, geotiff_opener: GeotiffOpener,cache_path: Optional[Union[str,Path]] = None):
        self.cache_path = cache_path
        self.line_drawer = line_drawer
        self.shapefile_reader = shapefile_reader
        self.geotiff_opener = geotiff_opener
    def generate(self,start:int,stop:int,path_hdf5: Path):
        size = stop-start+1
        list_points = list(self.shapefile_reader.get_points())
        size *= len(list_points)
        progress = ProgressBar0(IterationManager(total=size))
        with progress:
            with File(path_hdf5,"w") as cache:
                for tiff in self.geotiff_opener.iter_geotiff(start=start,stop=stop):
                    self.line_drawer.transformer.set_source(tiff.current_rio_object)
                    layer: Optional[PIL.Image] = None
                    draw: Optional[PIL.ImageDraw.ImageDraw] = None
                    for points in list_points:
                        points_transformed = []
                        for point in points:
                            points_transformed.append(tiff.loc_to_px(point))
                        if 0 in np.max(points,axis=0):
                            continue
                        progress.on_end()
                        layer,draw = self.line_drawer.draw(
                            points,
                            bounding_box=BoundingBox(
                                upper_left=tiff.upper_left(),
                                lower_right=tiff.lower_right(),
                                coordinate_transformer=self.line_drawer.transformer
                            ),
                            layer=layer,draw=draw
                        )
                layer = np.array(layer,dtype=np.uint8)
                cache.create_dataset(name=tiff.current_path.stem,shape=layer.shape,dtype='f',data=layer)
        return None
    def len_geotiff(self):
        return len(self.geotiff_opener)
    def save(self):
        if self.cache_path is None:
            return
        pass

if __name__ == '__main__':
    num_cpu = 8
    FolderInfos.init(test_without_data=True)
    r = RiversToRaster(*FactoryRiversExtractor().create())
    nb_elem = r.len_geotiff()
    split_ids = [int(v) for v in np.linspace(0,nb_elem,num_cpu*16*8)]
    RiversToRaster(*FactoryRiversExtractor().create()).generate(
        split_ids[0],
        split_ids[1],
        path_hdf5=FolderInfos.data_raw.joinpath("rivers").joinpath(f"cache_{split_ids[0]}_{split_ids[1]}.hdf5")
    )
    s=0

