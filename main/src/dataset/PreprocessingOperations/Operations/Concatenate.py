import numpy as np
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation


class Concatenate(AbstractOperation):
    def __init__(self, *inputs):
        super(Concatenate, self).__init__(*inputs)
    def execute(self):
        super(Concatenate, self).execute()
        self.outputs = np.concatenate([self.outputs],axis=0)
    def node_text(self):
        return "{Concatenate}"
    def __repr__(self):
        return f"Concatenate {self.attr_id} of level {self.level}"