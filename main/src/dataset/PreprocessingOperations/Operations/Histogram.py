from typing import Tuple, List

from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation
import numpy as np

class Histogram(AbstractOperation):
    def __init__(self, bin_size: float,*inputs):
        super(Histogram, self).__init__(*inputs)
        self.bin_size = bin_size
    def execute(self):
        super(Histogram, self).execute()
        self.outputs:List[Tuple[np.ndarray,np.ndarray]] = \
            [np.histogram(self.outputs,bins=np.arange(np.min(o),np.max(o)+self.bin_size,self.bin_size)) for o in self.outputs]
    def node_text(self):
        super(Histogram, self).node_text()
        return "{Histogram}"
    def __repr__(self):
        return f"Histogram {self.attr_id} of level {self.level}"

        