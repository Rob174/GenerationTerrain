from dataclasses import dataclass
from typing import get_type_hints

import numpy as np
import re

from osgeo import gdal,osr

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

    def to_geotiff(self,output_file:str):
        driver = gdal.GetDriverByName("GTiff")
        dst_ds = driver.Create(output_file, self.header.ncols, self.header.nrows, 1, gdal.GDT_Byte)
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