from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation


class FakeFirstOperation(AbstractOperation):
    def __init__(self, *inputs):
        super().__init__()
        self.level = 0
        self.attr_inputs = []
        self.children = inputs
    def set_name_id(self,name_id:str):
        self.outputs = name_id
    def node_text(self):
        return "{FakeNode}"
    def __repr__(self):
        return f"FakeFirstOperation {self.attr_id} of level {self.level}"
    def execute(self):
        pass