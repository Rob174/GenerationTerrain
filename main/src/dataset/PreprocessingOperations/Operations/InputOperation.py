from abc import abstractmethod

from main.src.dataset.PreprocessingOperations.AbstractNode import EnumStatus
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation
from main.src.dataset.PreprocessingOperations.Operations.FakeFirstOperation import FakeFirstOperation


class InputOperation(AbstractOperation):
    def __init__(self):
        super(InputOperation, self).__init__()
        self.status = EnumStatus.NOT_VISITED
    def set_fake_first_op(self,input:FakeFirstOperation):
        self.attr_inputs = [input]
    @abstractmethod
    def get(self, id:str):
        pass
    def execute(self):
        self.outputs = self.get(self.attr_inputs[0].outputs)
    def __repr__(self):
        return f"InputOperation {self.attr_id} of level {self.level}"
    def node_text(self):
        super(InputOperation, self).node_text()
