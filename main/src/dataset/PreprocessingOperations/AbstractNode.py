from abc import ABC,abstractmethod
from enum import Enum
from typing import List


class EnumStatus(str,Enum):
    VISITED = "visited"
    MARKED = "marked"
    NOT_VISITED = "not_visited"
class AbstractNode(ABC):
    id = 0
    def __init__(self,*inputs):
        self.attr_inputs: List[AbstractNode] = inputs
        AbstractNode.id += 1
        self.attr_id =  AbstractNode.id
        self.children = []
        for input in self.attr_inputs:
            input.children.append(self)
        for input in self.attr_inputs:
            input.children.sort(key=lambda x:x.id)

        self.status = EnumStatus.NOT_VISITED
        self.level = float('inf')

    def link(self,graph):
        for input in self.attr_inputs:
            graph.edge(input.attr_id,self.attr_id)
    def node(self,graph):
        graph.node(self.attr_id,label=self.node_text(),shape="record")
    @abstractmethod
    def node_text(self):
        pass
    def __str__(self):
        return  f"Node {self.id} with text {self.node_text()}"


        