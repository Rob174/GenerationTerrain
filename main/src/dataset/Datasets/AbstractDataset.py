"""Base class to build your own dataset"""
from abc import ABC,abstractmethod
from typing import Any

from main.src.data.TwoWayDict import TwoWayDict

from main.src.dataset.PreprocessingOperations.Operations.InputOperation import InputOperation


class ElementNotFound(Exception):
    def __init__(self,element,dataset):
        self.message = f"The element {element} has not been found in the dataset {dataset}"

class AbstractDataset(ABC,InputOperation):
    """Base class to build your own dataset"""

    def __init__(self, mapping: TwoWayDict, *args, **kwargs):
        self.attr_mapping = mapping

    @property
    def dataset(self):
        """property to map to the dataset object mappping to the file (hdf5 object, ...)"""
        raise NotImplementedError
    @abstractmethod
    def get(self, id: str) -> Any:
        """Get the object representing the array of id name

        Args:
            id: id of the sample in the dataset

        Returns:
            Any, object representing the sample extracted from the dataset

        """

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def values(self):
        pass
    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def __iter__(self):
        """Allow to use for loop on this object"""
        pass

        