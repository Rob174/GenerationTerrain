from abc import ABC,abstractmethod
from enum import Enum
from pathlib import Path
from typing import List
from graphviz import Digraph



class EnumStatus(str,Enum):
    VISITED = "visited"
    MARKED = "marked"
    NOT_VISITED = "not_visited"
class AbstractNode(ABC):
    id = 0
    graph: Digraph = Digraph(format="png")
    nodes = []
    @staticmethod
    def render(path: Path):
        AbstractNode.graph.render(path)
    @staticmethod
    def reset():
        AbstractNode.id = 0
        AbstractNode.nodes = []
    def __init__(self,*inputs):
        self.attr_inputs: List = inputs
        self.attr_id =  int(AbstractNode.id)
        self.leaf = False
        AbstractNode.id = AbstractNode.id+1
        self.node()
        self.children = []
        for input in self.attr_inputs:
            input.children.append(self)
        for input in self.attr_inputs:
            input.children.sort(key=lambda x:x.attr_id)

        self.status = EnumStatus.NOT_VISITED
        self.level = float('inf')
        AbstractNode.nodes.append(self)

    def link(self):
        for input in self.attr_inputs:
            link_str = f"\t{input.attr_id} -> {self.attr_id}"
            if link_str not in AbstractNode.graph.body:
                AbstractNode.graph.edge(str(input.attr_id),str(self.attr_id))
    def node(self):
        text = self.node_text()
        AbstractNode.graph.node(str(self.attr_id),label=text,shape="record")
    @abstractmethod
    def node_text(self):
        pass


        