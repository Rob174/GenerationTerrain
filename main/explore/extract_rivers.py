"""Test rivers extraction from elevation map thanks to the pyshed library
https://github.com/mdbartos/pysheds
"""

from pysheds.grid import Grid

from main.FolderInfos import FolderInfos
import matplotlib.pyplot as plt


if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)
    base_path = FolderInfos.data_raw.joinpath("geotiff").joinpath("1.tiff")
    grid = Grid.from_raster(base_path, data_name='dem')
    grid.read_raster(base_path, data_name='dir')
    r = grid.view('dem')

    # Determine D8 flow directions from DEM
    # ----------------------
    # Fill depressions in DEM
    grid.fill_depressions('dem', out_name='flooded_dem')

    # Resolve flats in DEM
    grid.resolve_flats('flooded_dem', out_name='inflated_dem')

    # Specify directional mapping
    dirmap = {
        "N":64,
        "NE":128,
        "E":1,
        "SE":2,
        "S":4,
        "SW":8,
        "W":16,
        "NW":32
    }
    dirmap = tuple(v for v in dirmap.values())

    # Compute flow directions
    # -------------------------------------
    grid.flowdir(data='inflated_dem', out_name='dir', dirmap=dirmap)
    grid.view('dir')

    # Delineate a catchment
    # ---------------------
    # Specify pour point
    x, y = 834987.5, 6540037.5

    # Delineate the catchment
    xmin, ymin, xmax, ymax = grid.bbox
    xmin, ymin, xmax, ymax = min(xmin,xmax),min(ymin,ymax),max(xmin,xmax),max(ymin,ymax)
    grid.catchment(data='dir', x=x, y=y, dirmap=dirmap, out_name='catch',
                   recursionlimit=15000, xytype='label')


    # Calculate flow accumulation
    # --------------------------
    grid.accumulation(data='catch', dirmap=dirmap, out_name='acc')
    grid.view('acc')
    grid.clip_to('catch')
    r=grid.view('dem')
    branches = grid.extract_river_network(fdir='catch', acc='acc',
                                          threshold=50, dirmap=dirmap)
    plt.matshow(branches)
    plt.show()
    s=0