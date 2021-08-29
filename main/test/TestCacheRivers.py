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
        dataset.close()
    def test_shape(self):
        dataset = self.build()
        keys = dataset.keys()
        random.shuffle(keys)
        for k in keys[:self.num_random_samples]:
            img = dataset.get(k)
            self.assertEquals(len(img.shape),3)
        dataset.close()
    def test_channel_position(self):
        dataset = self.build()
        keys = dataset.keys()
        random.shuffle(keys)
        for k in keys[:self.num_random_samples]:
            img = dataset.get(k)
            self.assertEquals(img.shape[2],3)
        dataset.close()

    def test_color(self):
        dataset = self.build()
        keys = dataset.keys()
        random.shuffle(keys)
        for k in keys[:self.num_random_samples]:
            img = dataset.get(k)
            for c in range(3):
                uniq = list(np.unique(img[:,:,c]))
                if c == 2:
                    self.assertEquals(uniq,[0.,255.])
                else:
                    self.assertEquals(uniq,[0.])
        dataset.close()


        