from pathlib import Path
from typing import List, Tuple

from main.src.dataset.PreprocessingOperations.Operations.Filters.AbstractFilter import AbstractFilter
import numpy as np
import json

class HistogramOutlier(AbstractFilter):
    def __init__(self,path_ref_val:Path):
        with open(path_ref_val,"r") as fp:
            self.reference_values = json.load(fp)
    def same_histograms(self,hist1:Tuple[np.ndarray,np.ndarray],hist2:Tuple[np.ndarray,np.ndarray]) -> bool:
        bins1,eff1 = hist1
        bins2,eff2 = hist2

        for bin in bins1:
            try:
                index = bins2.index(bin)
                if eff2[index] != eff1[index]:
                    return False
            except ValueError:
                return False
        return True

    def condition(self,inputs: List[Tuple[np.ndarray]]) -> None:
        reference_hist,*hist_to_compare = inputs
        self.outputs = []
        for histogram in hist_to_compare:
            self.outputs.append(not self.same_histograms(histogram,reference_hist))


        