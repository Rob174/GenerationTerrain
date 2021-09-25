from abc import abstractmethod
from typing import List

import numpy as np
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation


class AbstractFilter(AbstractOperation):
    def __init__(self, *inputs):
        super(AbstractFilter, self).__init__(*inputs)
    def execute(self):
        super(AbstractFilter, self).execute()
        if self.condition(self.outputs) is False:
            self.outputs = [None for _ in range(len(self.outputs))]
    @abstractmethod
    def condition(self,inputs: List[np.ndarray]):
        pass
    def node_text(self):
        super(AbstractFilter, self).node_text()
        return "{AbstractFilter}"
    def __repr__(self):
        return f"AbstractFilter {self.attr_id} of level {self.level}"
        