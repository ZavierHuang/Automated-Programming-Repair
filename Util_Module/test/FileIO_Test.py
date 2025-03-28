import os
import unittest

from Util_Module.src.FileIO import FileIO

class FileIO_Test(unittest.TestCase):
    def setUp(self):
        self.fileIO = FileIO('F:/GITHUB/Automated-Programming-Repair/')

    def test_fileExists(self):
        GOOGLE_JAVA_FORMAT = self.fileIO.Root + 'Tool/google-java-format-1.18.1-all-deps.jar'
        self.assertTrue(self.fileIO.isFileExist(GOOGLE_JAVA_FORMAT))

    def test_read_originalData(self):
        HumanEval_CodeLlama_data = self.fileIO.Root + 'Data_Storage/Original_Data/HumanEval/HumanEval_CodeLlama_IR4OR2.jsonl'
        data = self.fileIO.readJsonLineData(HumanEval_CodeLlama_data)
        self.assertEqual(len(data), 163)

    def test_write_data(self):
        writeFileName = 'test1.java'

        writeFileFolder = self.fileIO.Root + 'Util_Module/test/tempFile/'
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
