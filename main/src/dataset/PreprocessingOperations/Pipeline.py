from typing import List, Iterable, Optional

from main.src.dataset.PreprocessingOperations.AbstractNode import EnumStatus
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
    def __init__(self, input_operations: List[AbstractOperation]):
        input_operations.sort(key=lambda x: x.id)
        self.attr_input: FakeFirstOperation = FakeFirstOperation(input_operations)
        self.leveled_operations = []

    def build_levels(self):
        self.queue = [self.attr_input]
        self.completed = []
        self.search_level_children()
        self.levels = [(level_id, list(group)) for level_id, group in groupby(self.completed, lambda x: x.level)]
        length_last = len(self.levels[-1][1])
        if length_last != 2:
            raise OutputLengthException(length_last)

    def search_level_children(self):
        op = self.queue.pop(0)
        if op.status != EnumStatus.NOT_VISITED:
            raise CycleException(op)
        op.status = EnumStatus.VISITED
        # Add all children to queue
        for child in op.children:
            child.level = op.level + 1
            self.queue.append(child)
        self.search_level_children()
        op.status = EnumStatus.MARKED
        self.completed.append(op)

    def execute(self, name_id: str):
        self.attr_input.set_name_id(name_id)
        last_level: Optional[Iterable] = None
        for level_id, level_list in self.levels:
            for op in level_list:
                op.execute()
            last_level = level_list
        return [result.output for result in last_level]