import os
import unittest

from Util_Module.src.FileIO import FileIO
from Config import *

class FileIO_Test(unittest.TestCase):
    def setUp(self):
        self.fileIO = FileIO()

    def test_fileExists(self):
        self.assertTrue(self.fileIO.isFileExist(JAVA_FORMAT_PATH))

    def test_read_originalData(self):
        HumanEval_CodeLlama_data = ROOT + 'Data_Storage/HumanEval/CodeLlama/Original_Data/HumanEval_CodeLlama_IR4OR2.jsonl'
        data = self.fileIO.readJsonLineData(HumanEval_CodeLlama_data)
        self.assertEqual(len(data), 163)

    def test_write_data(self):
        writeFileName = 'test1.java'

        writeFileFolder = ROOT + 'Util_Module/test/tempFile/'
        self.assertTrue(os.path.isdir(writeFileFolder))

        writeFilePath = writeFileFolder + writeFileName
        writeContent = 'Hello'
        self.fileIO.writeFileData(writeFilePath, writeContent)
        self.assertTrue(self.fileIO.isFileExist(writeFilePath))

        readDataContent = self.fileIO.readFileData(writeFilePath)
        self.assertEqual(writeContent, readDataContent)

        self.fileIO.deleteFileData(writeFilePath)
        self.assertFalse(self.fileIO.isFileExist(writeFilePath))




if __name__ == '__main__':
    unittest.main()
