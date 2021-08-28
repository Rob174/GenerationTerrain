"""A dataset to manage hdf5 files for 2d np.ndarrays"""
from pathlib import Path

import numpy as np
from h5py import File

from main.src.data.Datasets.AbstractDataset import AbstractDataset
from main.src.data.TwoWayDict import TwoWayDict
from main.src.param_savers.BaseClass import BaseClass

from main.src.dataset.Datasets.AbstractDataset import ElementNotFound


class HDF5Dataset(BaseClass, AbstractDataset):
    """A dataset to manage hdf5 files for 2d np.ndarrays"""

    def __init__(self, src_hdf5: Path, mapping: TwoWayDict):
        super().__init__(mapping)
        self.attr_path = src_hdf5
        self.file = File(self.attr_path, "r")

    def get(self, id: str):
        """Get the object representing the array of id name

        Args:
            id: id of the sample in the dataset

        Returns:
            np.ndarray, representing the sample extracted from the dataset

        """
        try:
            elem = np.array(self.file[id], dtype=np.float32)
        except Exception as e:
            print(e)
            raise ElementNotFound(id,f"{self.__class__.__name__} of file {self.attr_path}")
        return elem

    def __iter__(self):
        """Allow to use for loop on this object"""
        return (k for k in self.keys())

    def keys(self):
        # with File(self.attr_path, "r") as file:
        return list(self.file.keys())

    def values(self):
        # with File(self.attr_path, "r") as file:
        return list(self.file.values())

    def __len__(self):
        # with File(self.attr_path, "r") as file:
        return len(self.file)
    def close(self):
        self.file.close()
