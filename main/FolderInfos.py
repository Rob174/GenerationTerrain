"""Static class containing interesting folder of the project with a separator adapted for the operating system (windows or linux)"""
import time
from time import strftime, gmtime, localtime
import os
from platform import system
from pathlib import Path


class NotInitializedException(Exception):
    def __str__(self):
        return "FolderInfos has not been initialized"

class FolderInfos:
    """Static class containing interesting folder of the project with a separator adapted for the operating system (windows or linux)
    We have to first initialize the class by calling the init method and then we can directly call the desired attribute



    Example of usage:

        >>> FolderInfos.init(test_without_data=False)
        >>> FolderInfos.get_class().root_folder
        C:\\....\\detection_nappe_hydrocarbures_IMT_cefrem\\
    """
    custom_name: str = ""
    subdir: str = ""
    @property
    def data_in(self) -> Path:
        """Path, data_in folder path"""
        return self.root_folder.joinpath("data_in")
    @property
    def data_out(self) -> Path:
        """Path,  data_out folder path"""
        path = self.root_folder.joinpath("data_out")
        if FolderInfos.subdir != "":
            self._data_out = path.joinpath(FolderInfos.subdir)
        return path
    @property
    def data_raw(self) -> Path:
        """Path, data_raw folder path"""
        return self.root_folder.joinpath("data_raw")
    @property
    def base_folder(self) -> Path:
        """Path, path to the newly created folder for the run"""
        return self.data_out.joinpath(self.id + "_"+FolderInfos.custom_name)
    @property
    def base_filename(self) -> Path:
        """Path, incomplete path to any new file in this new folder"""
        return self.base_folder.joinpath(self.id+"_"+FolderInfos.custom_name)
    @property
    def data_test(self) -> Path:
        """Path, data_test folder path"""
        return self.root_folder.joinpath("data_test")
    @property
    def root_folder(self) -> Path:
        """Path, path to the GenerationTerrain folder"""
        return Path(__file__).parent.parent
    @property
    def id(self) -> str:
        """str, uniq id generated with the datetime of the run"""
        if self._id is None:
            self._id = strftime("%Y-%m-%d_%Hh%Mmin%Ss", localtime())
        return self._id
    instance = None
    @staticmethod
    def get_class() -> 'FolderInfos':
        if FolderInfos.instance is None:
            raise NotInitializedException()
        return FolderInfos.instance
    @staticmethod
    def init(custom_name="",subdir="",test_without_data=False,with_id=None):
        FolderInfos.instance = FolderInfos(custom_name,subdir,test_without_data,with_id)
    def __init__(self,custom_name="",subdir="",test_without_data=False,with_id=None):
        """Initialize some interesting pathes as static attributes.

        Args:
            custom_name: str, custom name to add in the folder of the current run
            subdir: str, subdir for datafolder
            test_without_data: bool, if False, the object automatically creates a folder for each run. If True this folder is not created.
        """
        FolderInfos.subdir = subdir
        FolderInfos.custom_name = custom_name
        while True:
            if with_id is not None:
                self._id = with_id
            else:
                self._id = None
            try:
                if test_without_data is False and with_id is None:
                    os.mkdir(self.base_folder)
                break
            except FileExistsError as e:
                print(e)
                print("waiting..... folder name already taken")
                time.sleep(4)

