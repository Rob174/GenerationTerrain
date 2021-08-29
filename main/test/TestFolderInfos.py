from unittest import TestCase

from main.FolderInfos import FolderInfos, NotInitializedException


class TestFolderInfos(TestCase):
    def test_proper_initialization(self):
        FolderInfos.init(test_without_data=True)
        v = FolderInfos.get_class().data_in
        v = FolderInfos.get_class().data_out
        v = FolderInfos.get_class().data_raw
        v = FolderInfos.get_class().data_test
        v = FolderInfos.get_class().base_folder
        v = FolderInfos.get_class().base_filename
        v = FolderInfos.get_class().root_folder
        v = FolderInfos.get_class().id
    def test_missed_initialization(self):
        with self.assertRaises(NotInitializedException):
            v = FolderInfos.get_class().data_in

        