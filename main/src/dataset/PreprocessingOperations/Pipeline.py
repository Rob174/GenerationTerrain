import numpy as np
from pathlib import Path
from typing import List, Iterable, Optional

from main.src.dataset.PreprocessingOperations.AbstractNode import EnumStatus, AbstractNode
from main.src.dataset.PreprocessingOperations.AbstractOperation import AbstractOperation
from main.src.dataset.PreprocessingOperations.Operations.FakeFirstOperation import FakeFirstOperation
from itertools import groupby


class CycleException(Exception):
    def __init__(self, node):
        self.message = f"There is a cycle in the graph including the node {node}"
        super(CycleException, self).__init__(self.message)


class OutputLengthException(Exception):
    def __init__(self, length):
        self.message = f"We must have 2 outputs not {length}"
        super(OutputLengthException, self).__init__(self.message)


class Pipeline:
    def __init__(self, input_operations: List[AbstractOperation], out_path: Path):
        input_operations.sort(key=lambda x: x.attr_id)
        self.attr_input: FakeFirstOperation = FakeFirstOperation(*input_operations)
        for input in input_operations:
            input.set_fake_first_op(self.attr_input)
        self.leveled_operations = []
        self.attr_out_path = out_path

    def build_levels(self):
        """Schedule operations stored in self.queue based on their dependencies and render the resulting network graph
        Concretely we have to decide which operations can be done in parallel first, then which operations can be done...."""
        self.queue = [self.attr_input]
        self.completed = []
        self.search_level_children()
        self.levels = [(level_id, list(group)) for level_id, group in groupby(self.completed, lambda x: x.level)]
        self.leaves = [e for e in self.completed if e.leaf is True]
        length_last = len(self.leaves)
        if length_last != 2:
            raise OutputLengthException(length_last)
        for node in AbstractNode.nodes:
            node.link()
        AbstractNode.render(self.attr_out_path)

    def search_level_children(self):
        """BFS based algorithm to split into levels operations based on their relations."""
        if len(self.queue) == 0:
          return
        op = self.queue.pop(0)
        if op.status != EnumStatus.NOT_VISITED:
            raise CycleException(op)
        op.status = EnumStatus.VISITED
        # Add all children to queue
        if len(op.children) == 0:
            op.leaf = True
        for child in op.children:
            child.level = op.level + 1
            if child in self.queue:
                self.queue.pop(self.queue.index(child))
            self.queue.append(child)
        self.search_level_children()
        op.status = EnumStatus.MARKED
        self.completed.append(op)

    def execute(self, name_id: str) -> List[np.ndarray]:
        """After the graph has been built (and checked at the same time),
        we want to execute the pipeline on a specific input and get the result

        Args:
            name_id: str, id of the sample to produce in the datasets

        Returns:
            List[np.ndarray], list of expected outputs
        """
        self.attr_input.set_name_id(name_id)
        self.levels.sort(key=lambda x:x[0])
        for level_id, level_list in self.levels:
            for op in level_list:
                op.execute()
        return [result.outputs for result in self.leaves]
