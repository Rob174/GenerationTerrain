import numpy as np
from unittest import TestCase

from main.src.dataset.PreprocessingOperations.Operations.Concatenate import Concatenate
from main.src.dataset.PreprocessingOperations.Operations.InputOperation import InputOperation
from main.src.dataset.PreprocessingOperations.Pipeline import Pipeline


class FakeInputOperationMonoColor(InputOperation):
    def __init__(self):
        super(FakeInputOperationMonoColor, self).__init__()

    def get(self,id):
        super(FakeInputOperationMonoColor, self).get(id)
        return np.random.rand(100,100)
    def node_text(self):
        return "input"
    def __repr__(self):
        return f"FakeInputOperation {self.attr_id} of level {self.level}"

class TestPipeline(TestCase):
    def build_graph1(self):
        dataset_in1 = FakeInputOperationMonoColor()
        dataset_in2 = FakeInputOperationMonoColor()
        merged = Concatenate(dataset_in1,dataset_in2)
        dataset_in3 = FakeInputOperationMonoColor()
        pipeline = Pipeline([dataset_in1,dataset_in2,dataset_in3])
        return pipeline,dataset_in1,dataset_in2,merged,dataset_in3
    def test_ids(self):
        pipeline,*nodes = self.build_graph1()
        for i,n in enumerate(nodes):
            self.assertEqual(n.attr_id, i)

    def test_build_levels(self):
        pipeline,*_ = self.build_graph1()
        pipeline.build_levels()
    def test_execute(self):
        pipeline,*_ = self.build_graph1()
        pipeline.build_levels()
        result = pipeline.execute("test")
        self.assertEqual(len(result),2)

