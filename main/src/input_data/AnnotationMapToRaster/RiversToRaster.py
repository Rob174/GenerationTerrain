import PIL
import numpy as np
from pathlib import Path
from typing import Optional, Union


from main.FolderInfos import FolderInfos
from main.src.ProgressBar.IterationManager import IterationManager
from main.src.ProgressBar.ProgressBar0 import ProgressBar0
from main.src.input_data.BoundingBox.BoundingBox import BoundingBox
from main.src.input_data.ColorManager.Color import Color
from main.src.input_data.CoordinateTransformer.RasterCoordinateTransformer import RasterCoordinateTransformer
from main.src.input_data.GeotiffOpener import GeotiffOpener
from main.src.input_data.LineDrawer.LineDrawer import LineDrawer
from main.src.input_data.Readers.RiversShpFileReader import RiversShpFileReader
from h5py import File
class FactoryRiversExtractor:
    def create(self):
        FolderInfos.init(test_without_data=True)
        geotiff_opener = GeotiffOpener()
        shapefile_reader = RiversShpFileReader(FolderInfos.get_class().data_raw.joinpath("rivers").joinpath("COURS_D_EAU.shp"))
        line_drawer = LineDrawer(transformer=RasterCoordinateTransformer(), thickness=10, color=Color(r=0, g=0, b=255))
        return line_drawer,shapefile_reader,geotiff_opener

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
        with File(path_hdf5,"w") as cache:
            for tiff in self.geotiff_opener.iter_geotiff(start=start,stop=stop):
                print(tiff.current_path)
                self.line_drawer.transformer.set_source(tiff.current_rio_object)
                layer: Optional[PIL.Image.Image] = None
                draw: Optional[PIL.ImageDraw.ImageDraw] = None
                for points in list_points:
                    layer,draw = self.line_drawer.draw(
                        [point[0] for point in points],[point[1] for point in points],
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
from ray.util.multiprocessing import Pool
import ray
def execute(arg):
    start, stop = arg
    RiversToRaster(*FactoryRiversExtractor().create()).generate(
        start,
        stop,
        path_hdf5=FolderInfos.get_class().data_raw.joinpath("rivers").joinpath(
            f"cache_{start}_{stop}.hdf5")
    )
    return f"End {start} -> {stop}"
def to_hdf5():
    num_cpu = 11

    FolderInfos.init(test_without_data=True)
    r = RiversToRaster(*FactoryRiversExtractor().create())
    nb_elem = r.len_geotiff()
    split_ids = [int(v) for v in np.linspace(0, nb_elem, num_cpu * 4)]
    ray.init()
    pool = Pool(processes=num_cpu)
    stop_index = len(split_ids)
    start_index = 0
    for result in pool.map(execute, list(zip(split_ids[:stop_index - 1], split_ids[1:stop_index]))):
        print(result)
if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)
    rivers_folder: Path = FolderInfos.get_class().data_raw.joinpath("rivers")
    with File(rivers_folder.joinpath("cache_rivers.hdf5"),"w") as cache:
        cache: File
        for cache_file in list(rivers_folder.iterdir())[0:2]:
            if cache_file.suffix == ".hdf5":
                with File(cache_file,"r") as cache_src:
                    for img_name,img in cache_src.items():
                        cache.create_dataset(name=img_name,shape=img.shape,dtype='i',data=np.array(img,dtype=np.uint8))
                print(f"{cache_file} done")

    s=0