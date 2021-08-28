"""Represents an abstract operation"""

from abc import ABC, abstractmethod
from typing import List, Any

from main.src.dataset.PreprocessingOperations.AbstractNode import AbstractNode


class AbstractOperation(ABC,AbstractNode):
    def __init__(self, *inputs: List[Any]):
        AbstractNode.__init__(self,*inputs)
        ABC.__init__(self)
        self.outputs = None
    @abstractmethod
    def execute(self):
        self.outputs = [o.outputs for o in self.attr_inputs]



        