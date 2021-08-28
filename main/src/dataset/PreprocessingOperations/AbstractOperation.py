"""Represents an abstract operation"""

from abc import ABC, abstractmethod
from typing import List, Any

from main.src.dataset.PreprocessingOperations.AbstractNode import AbstractNode

class WrongInput(Exception):
    def __init__(self,object):
        self.message = f"Object of type {type(object)} is not suited to be an input"
        super(WrongInput, self).__init__(self.message)



class AbstractOperation(AbstractNode):
    def __init__(self, *inputs: List[Any]):
        super(AbstractOperation, self).__init__(*inputs)
        self.outputs = None
    @abstractmethod
    def execute(self):
        self.outputs = [o.outputs for o in self.attr_inputs]
    def set_fake_first_op(self,input):
        raise WrongInput(self)



        