import os
import shutil
import unittest

from Util_Module.src.FileIO import FileIO
from Config import *

class FileIO_Test(unittest.TestCase):
    def setUp(self):
        self.fileIO = FileIO()

    def test_file_exists(self):
        self.assertTrue(self.fileIO.isPathExist(JAVA_FORMAT_PATH))

    def test_folder_exists(self):
        self.assertTrue(self.fileIO.isPathExist(os.path.join(ROOT,'Data_Storage')))

    def test_read_originalData(self):
        HumanEval_CodeLlama_data = os.path.join(ROOT, 'Data_Storage/HumanEval/CodeLlama/Original_Data/HumanEval_CodeLlama_IR4OR2.jsonl')
        data = self.fileIO.readJsonLineData(HumanEval_CodeLlama_data)
        print(data)
        self.assertEqual(len(data), 163)

    def test_write_data(self):
        writeFileName = 'test1.java'

        writeFileFolder = os.path.join(ROOT,  'Util_Module/test/javaFormatTestFile/')
        self.assertTrue(os.path.isdir(writeFileFolder))

        writeFilePath = writeFileFolder + writeFileName
        writeContent = 'Hello'
        self.fileIO.writeFileData(writeFilePath, writeContent)
        self.assertTrue(self.fileIO.isPathExist(writeFilePath))

        readDataContent = self.fileIO.readFileData(writeFilePath)
        self.assertEqual(writeContent, readDataContent)

        self.fileIO.deleteFileData(writeFilePath)
        self.assertFalse(self.fileIO.isPathExist(writeFilePath))

    def test_get_all_subfolder(self):
        tempFolderPath = os.path.join(ROOT, 'Util_Module/test/tempFolder')

        if self.fileIO.isPathExist(tempFolderPath):
            shutil.rmtree(tempFolderPath)

        os.makedirs(tempFolderPath)
        os.makedirs(os.path.join(tempFolderPath, 'subFolder1'))
        os.makedirs(os.path.join(tempFolderPath, 'subFolder2'))
        os.makedirs(os.path.join(tempFolderPath, 'subFolder3'))

        tempFilePath1 = os.path.join(tempFolderPath, 'subFolder1/test1-1.txt')
        tempFilePath2 = os.path.join(tempFolderPath, 'subFolder1/test1-2.txt')
        tempFilePath3 = os.path.join(tempFolderPath, 'subFolder2/test2.txt')
        tempFilePath4 = os.path.join(tempFolderPath, 'subFolder3/test3-1.txt')
        tempFilePath5 = os.path.join(tempFolderPath, 'subFolder3/test3-2.txt')

        self.fileIO.writeFileData(tempFilePath1, "Hello1")
        self.fileIO.writeFileData(tempFilePath2, "Hello2")
        self.fileIO.writeFileData(tempFilePath3, "Hello3")
        self.fileIO.writeFileData(tempFilePath4, "Hello4")
        self.fileIO.writeFileData(tempFilePath5, "Hello5")

        subFolderList = self.fileIO.getSubFolderList(tempFolderPath)
        allFileList = self.fileIO.getFileListUnderFolder(tempFolderPath)

        self.assertEqual(len(subFolderList), 3)
        self.assertEqual(len(allFileList), 5)

    def test_clear_all_file_under_subfolder(self):
        tempFolderPath = os.path.join(ROOT,  'Util_Module/test/tempFolder')
        subFolderList = self.fileIO.getSubFolderList(tempFolderPath)
        result = self.fileIO.deleteSubFolderAndCreate(tempFolderPath, subFolderList)
        self.assertTrue(result)

    def test_shutil_move_file(self):
        fileName = 'test.txt'

        # source
        srcFolder = os.path.join(ROOT, 'Util_Module/test/tempFolder2')
        self.assertFalse(self.fileIO.isPathExist(srcFolder))

        os.mkdir(srcFolder)
        self.assertTrue(self.fileIO.isPathExist(srcFolder))

        srcFilePath = os.path.join(srcFolder, fileName)
        self.fileIO.writeFileData(srcFilePath, "Hello")
        self.assertTrue(self.fileIO.isPathExist(srcFilePath))

        # destination
        desFolder = os.path.join(ROOT, 'Util_Module/test/tempFolder3')
        self.assertFalse(self.fileIO.isPathExist(desFolder))

        os.mkdir(desFolder)
        self.assertTrue(self.fileIO.isPathExist(desFolder))

        desFilePath = os.path.join(desFolder, fileName)
        shutil.move(srcFilePath, desFilePath)
        self.assertTrue(self.fileIO.isPathExist(desFilePath))

        shutil.rmtree(srcFolder)
        shutil.rmtree(desFolder)









if __name__ == '__main__':
    unittest.main()
