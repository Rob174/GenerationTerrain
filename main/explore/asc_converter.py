from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import get_type_hints, Union, Optional

import numpy as np
import re

from osgeo import gdal,osr

from main.FolderInfos import FolderInfos


@dataclass
class ASCIIHeader:
    ncols: int
    nrows: int
    xllcorner: float
    yllcorner: float
    cellsize: float
    NODATA_value: float
    def __post_init__(self):
        for attr, type in get_type_hints(ASCIIHeader).items():
            setattr(self, attr, type(getattr(self, attr)))
class ASCFile:
    def __init__(self,path: str):
        self.path = path
        self.np_data = np.loadtxt(path, skiprows=6)
        with open(self.path,"r") as fp:
            infos = {}
            for _ in range(6):
                infos.update([[s.strip() for s in re.split(" +", fp.readline())]])
        self.header = ASCIIHeader(**infos)

    def to_geotiff(self,output_file:Union[str,Path]):
        """
        Convert ASC file to Geotiff
        Taken from https://qastack.fr/gis/62343/how-can-i-convert-a-ascii-file-to-geotiff-using-python

        Args:
            output_file: str, path to the geotiff output path

        Returns:

        """
        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(str(output_file), self.header.ncols, self.header.nrows, 1, gdal.GDT_Byte)
        dst_ds.SetGeoTransform( [ self.header.xllcorner, # top left x
                                  self.header.cellsize, # w-e pixel resolution
                                  0, # rotation
                                  self.header.yllcorner, # top left y
                                  0, # rotation
                                  self.header.cellsize # n-s pixel resolution
                                  ] )
        # set the reference info
        srs = osr.SpatialReference()
        srs.SetWellKnownGeogCS("WGS84")
        dst_ds.SetProjection(srs.ExportToWkt())

        # write the band
        dst_ds.GetRasterBand(1).WriteArray(self.np_data)

class AbstractFolderManager(ABC):
    @abstractmethod
    def last_index(self):
        pass

    def next_index(self):
        return self.last_index()+1
    @abstractmethod
    def next_name(self):
        pass
class GeoTiffFolderManager(AbstractFolderManager):
    instance: Optional = None
    def create(self,base_path: Path):
        if not GeoTiffFolderManager.instance:
            GeoTiffFolderManager.instance = GeoTiffFolderManager(base_path)
        return GeoTiffFolderManager.instance

    def __init__(self, base_path : Path):
        self.base_path = base_path

    def last_index(self):
        return len(list(self.base_path.glob("*")))-1
    def next_name(self):
        return self.base_path.joinpath(str(self.next_index())+".tiff")
class BDAltivFolderConverter:
    def __init__(self, base_path: Path, out_folder_manager: AbstractFolderManager):
        self.base_path = base_path
        self.out_folder_manager = out_folder_manager
    def convert(self):
        [folder] = list(self.base_path.joinpath("BDALTIV2").glob("1_*"))
        for asc_file in list(folder.iterdir())[0].iterdir():
            file =  ASCFile(asc_file)
            file.to_geotiff(self.out_folder_manager.next_name())



if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)
    for folder in FolderInfos.data_raw.joinpath("asc").iterdir():
        converter = BDAltivFolderConverter(
            folder,
            GeoTiffFolderManager(FolderInfos.data_raw.joinpath("geotiff"))
        )
        converter.convert()