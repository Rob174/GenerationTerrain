from main.src.dataset.PreprocessingOperations.AbstractNode import AbstractNode
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation


class FakeFirstOperation(AbstractOperation):
    def __init__(self, *inputs):
        super().__init__(*inputs)
        self.attr_inputs = []
        self.children = inputs
    def set_name_id(self,name_id:str):
        self.outputs = name_id
    def node_text(self):
        return "{FakeNode}"

    def execute(self):
        pass