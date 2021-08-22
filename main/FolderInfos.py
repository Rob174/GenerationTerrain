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
        >>> FolderInfos.root_folder
        C:\\....\\detection_nappe_hydrocarbures_IMT_cefrem\\
    """
    data_in: Path = None
    """Path, data_in folder path"""
    data_out: Path = None
    """Path,  data_out folder path"""
    data_raw: Path = None
    """Path, data_raw folder path"""
    base_folder: Path = None
    """Path, path to the newly created folder for the run"""
    base_filename: Path = None
    """Path, incomplete path to any new file in this new folder"""
    data_test: Path = None
    """Path, data_test folder path"""
    root_folder: Path = None
    """Path, path to the GenerationTerrain folder"""
    id: str = None
    """str, uniq id generated with the datetime of the run"""
    initialized = False
    """bool, True if initialized"""

    @staticmethod
    def init(custom_name="",subdir="",test_without_data=False,with_id=None):
        """Initialize some interesting pathes as static attributes.

        Args:
            custom_name: str, custom name to add in the folder of the current run
            subdir: str, subdir for datafolder
            test_without_data: bool, if False, the object automatically creates a folder for each run. If True this folder is not created.
        """
        while True:
            FolderInfos.id = strftime("%Y-%m-%d_%Hh%Mmin%Ss", localtime())
            if with_id is not None:
                FolderInfos.id = with_id
            FolderInfos.root_folder = Path(__file__).parent.parent
            FolderInfos.input_data_folder = FolderInfos.root_folder.joinpath("data_in")
            FolderInfos.data_out = FolderInfos.root_folder.joinpath("data_out")
            if subdir != "":
                FolderInfos.data_out = FolderInfos.data_out.joinpath(subdir)
            FolderInfos.base_folder = FolderInfos.data_out.joinpath(FolderInfos.id + "_"+custom_name)
            FolderInfos.base_filename = FolderInfos.base_folder.joinpath(FolderInfos.id+"_"+custom_name)
            FolderInfos.data_test = FolderInfos.root_folder.joinpath("data_test")
            FolderInfos.data_raw = FolderInfos.root_folder.joinpath("data_raw")
            try:
                if test_without_data is False and with_id is None:
                    os.mkdir(FolderInfos.base_folder)
                break
            except FileExistsError as e:
                print(e)
                print("waiting..... folder name already taken")
                time.sleep(4)
        FolderInfos.initialized = True
    @staticmethod
    def is_initialized():
        if not FolderInfos.initialized:
            raise NotInitializedException()
    @staticmethod
    def open_mode_suggestion(path):
        if os.path.exists(path) is True:
            return "r+"
        return "w"

