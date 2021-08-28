from main.FolderInfos import FolderInfos
from main.src.dataset.PreprocessingOperations.Operations.Concatenate import ConcatDataset
from main.src.dataset.Datasets.HDF5Dataset import HDF5Dataset

from main.src.dataset.Datasets.TwoWayDict import TwoWayDict


class RiversDatasetFactory:
    def __call__(self, *args, **kwargs):
        elevation_dataset = HDF5Dataset(FolderInfos.data_in.joinpath("elevations.hdf5"),mapping=TwoWayDict({}))
        rivers_dataset = HDF5Dataset(FolderInfos.data_in.joinpath("rivers.hdf5"),mapping=TwoWayDict({"river":"0x0000ff"}))
        concatenated_dataset = ConcatDataset(elevation_dataset,rivers_dataset)
        return concatenated_dataset
        