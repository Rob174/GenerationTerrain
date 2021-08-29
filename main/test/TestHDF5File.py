from unittest import TestCase

from main.FolderInfos import FolderInfos
from main.src.dataset.Datasets.AbstractDataset import ElementNotFound
from main.src.dataset.Datasets.HDF5Dataset import HDF5Dataset
from main.src.dataset.Datasets.TwoWayDict import TwoWayDict


class TestHDF5Dataset(TestCase):
    def __init__(self,*args,**kwargs):
        super(TestHDF5Dataset, self).__init__(*args,**kwargs)
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
    def test_missing_key(self):
        dataset = self.build()
        with self.assertRaises(ElementNotFound):
            dataset.get("test_key")
        dataset.close()
    def test_keys(self):
        dataset = self.build()
        keys = dataset.keys()
        self.assertEquals(type(keys),list)
        dataset.close()


    def test_values(self):
        dataset = self.build()
        values = dataset.values()
        self.assertEquals(type(values),list)
        self.assertEquals(len(values),len(dataset.keys()))
        dataset.close()

    def test_length(self):
        dataset = self.build()
        length = len(dataset)
        self.assertEquals(type(length),int)
        self.assertEquals(length,len(dataset.keys()))
        dataset.close()
    def test_node_text(self):
        dataset = self.build()
        self.assertEquals(type(dataset.node_text()),str)


        