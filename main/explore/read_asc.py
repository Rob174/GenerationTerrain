"""Test on how to read an asc file"""
from main.FolderInfos import FolderInfos
import numpy as np
import matplotlib.pyplot as plt






if __name__ == '__main__':
    FolderInfos.init(test_without_data=True)
    base_path = FolderInfos.get_class().data_raw.joinpath("BDALTIV2_2-0_25M_ASC_LAMB93-IGN69_D001_2021-01-13")\
        .joinpath("BDALTIV2")\
        .joinpath("1_DONNEES_LIVRAISON_2021-02-00157").joinpath("BDALTIV2_MNT_25M_ASC_LAMB93_IGN69_D001")
    for file_obj in base_path.iterdir():
        array = np.loadtxt(file_obj, skiprows=6)
        plt.figure(1)
        plt.title(f"Source")
        plt.imshow(array,cmap="gray")
        plt.show()
        s=0