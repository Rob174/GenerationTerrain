from abc import abstractmethod

from main.src.dataset.PreprocessingOperations.AbstractNode import EnumStatus
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation
from main.src.dataset.PreprocessingOperations.Operations.FakeFirstOperation import FakeFirstOperation


class InputOperation(AbstractOperation):
    def __init__(self,input:FakeFirstOperation):
        super(InputOperation, self).__init__([input])
        self.status = EnumStatus.NOT_VISITED
    @abstractmethod
    def get(self, id:str):
        pass
    def execute(self):
        self.outputs = self.get(self.attr_inputs[0].outputs)
