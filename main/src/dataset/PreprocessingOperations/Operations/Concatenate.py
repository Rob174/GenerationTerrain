import numpy as np
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractPreprocessingOperation


class Concatenate(AbstractPreprocessingOperation):
    def __init__(self, *inputs):
        super(Concatenate, self).__init__(*inputs)
    def execute(self):
        super(Concatenate, self).execute()
        self.outputs = np.concatenate([self.outputs],axis=0)
    def node_text(self):
        return "{Concatenate}"