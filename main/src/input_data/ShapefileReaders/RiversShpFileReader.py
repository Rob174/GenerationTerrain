from pathlib import Path
import geopandas as gpd

class RiversShpFileReader:
    def __init__(self, source_file: Path):
        self.source_file = source_file

    def get_points(self):
        shapefile = gpd.read_file(self.source_file)
        for shape in shapefile.geometry:
            if shape.type == "LineString":
                yield list(zip(*shape.xy))
            elif shape.type == 'MultiLineString':
                accumulator =  []
                for subline in shape:
                    accumulator.extend(list(zip(*subline.xy)))
                yield accumulator