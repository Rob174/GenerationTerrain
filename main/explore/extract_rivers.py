"""Test rivers extraction from elevation map thanks to the pyshed library
https://github.com/mdbartos/pysheds
"""

from pysheds.grid import Grid

from main.FolderInfos import FolderInfos

if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)
    base_path = FolderInfos.data_raw.joinpath("BDALTIV2_2-0_25M_ASC_LAMB93-IGN69_D001_2021-01-13")\
        .joinpath("BDALTIV2")\
        .joinpath("1_DONNEES_LIVRAISON_2021-02-00157").joinpath("BDALTIV2_MNT_25M_ASC_LAMB93_IGN69_D001")
    base_out_name = pathlib.Path(FolderInfos.data_raw)
    # for i,path in enumerate(base_path.iterdir()):
    #     s=0
    grid = Grid.from_raster(r"C:\Users\robin\Documents\projets\GenerationTerrain\data_raw\test.tif", data_name='dem')