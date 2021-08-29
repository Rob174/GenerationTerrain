from unittest import TestCase

from main.FolderInfos import FolderInfos
from main.src.dataset.Datasets.HDF5Dataset import HDF5Dataset
from main.src.dataset.Datasets.TwoWayDict import TwoWayDict
import numpy as np
import random

class TestCacheRivers(TestCase):
    def __init__(self,*args,**kwargs):
        super(TestCacheRivers, self).__init__(*args,**kwargs)
        self.num_random_samples = 10

    def build(self):
        FolderInfos.init(test_without_data=True)
        dataset = HDF5Dataset(
            src_hdf5=FolderInfos.data_raw.joinpath("rivers").joinpath("cache_rivers.hdf5"),
            mapping=TwoWayDict({
                "rivers": 0
            })
        )
        return dataset
    def test_open(self):
        dataset = self.build()
        dataset.keys()
    def test_shape(self):
        dataset = self.build()
        keys = dataset.keys()
        random.shuffle(keys)
        for k in keys[:self.num_random_samples]:
            self.assertEquals(len(dataset.get(k).shape),2)
        