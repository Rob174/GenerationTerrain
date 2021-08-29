import numpy as np
from pathlib import Path

import rasterio

class GeoTiffReader:
    def __init__(self,path: Path):
        self.path = path
        self.file = rasterio.open(self.path)
    def get_array(self):
        return np.array(self.file.read(1),dtype=np.float32)
    def get_tranformation_matrix(self):
        return np.array(self.file.transform,dtype=np.float32)



        