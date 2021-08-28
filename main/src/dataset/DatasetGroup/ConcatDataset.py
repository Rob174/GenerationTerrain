from typing import Optional

import numpy as np
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractMerger
from main.src.dataset.Datasets.AbstractDataset import ElementNotFound


class WrongShapeException(Exception):
    def __init__(self,shape_ref: Optional[tuple],shape_targ:tuple):
        self.message = f"Two elements have different shapes with {shape_ref} and {shape_targ}"
        super(WrongShapeException, self).__init__(self.message)

class DatasetGroup(AbstractMerger):
    def __init__(self,*datasets):
        self.attr_datasets = datasets
        super(DatasetGroup, self).__init__(*datasets)
    def get(self, id: str):
        """Get the object representing the array of id name

        Args:
            id: id of the sample in the dataset

        Returns:
            np.ndarray, representing the sample extracted from the dataset

        """
        elems = []
        shape = None
        for dataset in self.attr_datasets:
            try:
                elem = dataset.get(id)
                if shape is not  None and elem.shape != shape:
                    raise WrongShapeException(shape,elem.shape)
                elems.append()
            except ElementNotFound as e:
                print(e)
                raise ElementNotFound(f"Element {id} not found in dataset {dataset.__class__.__name__}")
        return elems
    def keys(self):
        sets = [set(d) for d in self.attr_datasets]
        return sets[0].intersection(*sets[1:])

    def values(self):
        return (self.get(k) for k in self.keys())
    def items(self):
        return ((k,self.get(k)) for k in self.keys())

    def __iter__(self):
        """Allow to use for loop on this object"""
        return self.values()

        