import shutil
import unittest

from Util_Module.src.FileIO import FileIO
from Util_Module.src.JsonFileIO import JsonFileIO
from Config import *

class JsonFileIO_Test(unittest.TestCase):
    def setUp(self):
        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()

    def test_read_originalData(self):
        HumanEval_CodeLlama_data = os.path.join(ROOT, 'Data_Storage/HumanEval/CodeLlama/Original_Data/HumanEval_CodeLlama_IR4OR2.jsonl')
        data = self.jsonFileIO.readJsonLineData(HumanEval_CodeLlama_data)
        self.assertEqual(len(data), 163)


if __name__ == '__main__':
    unittest.main()
