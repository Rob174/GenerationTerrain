import json
from enum import Enum

from h5py import File

from main.FolderInfos import FolderInfos
from main.src.input_data.Readers.GeoTiffReader import GeoTiffReader
from rich.progress import track

class EnumDicoInfosElevation(str,Enum):
    transformation_matrix = "transformation_matrix"

if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)
    elevation_path = FolderInfos.get_class().data_raw.joinpath("elevation")
    data_folder = elevation_path.joinpath("geotiff")
    with File(elevation_path.joinpath("elevation.hdf5"),"w") as cache_elevation:
        dico_infos = {}
        for tiff in track(list(data_folder.iterdir())):
            geotiff = GeoTiffReader(tiff)
            array = geotiff.get_array()
            dico_infos[tiff.stem] = {
                EnumDicoInfosElevation.transformation_matrix:geotiff.get_tranformation_matrix().tolist()
            }
            cache_elevation.create_dataset(
                name=tiff.stem,
                shape=array.shape,
                dtype='f',
                data=array
            )
    with open(elevation_path.joinpath("elevation_infos.json"),"w") as fp:
        json.dump(dico_infos,fp)