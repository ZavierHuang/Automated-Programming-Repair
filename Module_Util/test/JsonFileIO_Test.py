import shutil
import unittest

from Module_Util.src.FileIO import FileIO
from Module_Util.src.JsonFileIO import JsonFileIO
from Config import *

class JsonFileIO_Test(unittest.TestCase):
    def setUp(self):
        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()

    def test_read_originalData(self):
        HumanEval_CodeLlama_data = os.path.join(ROOT, 'Data_Storage/HumanEval/CodeLlama/Original_Data/HumanEval_CodeLlama_IR4OR2.jsonl')
        data = self.jsonFileIO.readJsonLineData(HumanEval_CodeLlama_data)
        self.assertEqual(len(data), 163)

    def test_create_patch_result_json(self):
        dictionary = []

        for i in range(5):
            sub_dictionary = {
                'ID': 'buggyId',
                'Repair': True,
                'Type': 'Single',
                'Solution': 'return x+y;',
                'ExactlyMatch': True,
                'output': {}
            }
            for j in range(5):
                sub_dictionary['output'][str(j)] = {
                    'patch' : 'None',
                    'formatCheck':{
                        'formatResult':True,
                        'formatLog': '............'
                    },
                    'compileCheck':{
                        'compileResult':True,
                        'compileLog': '............'
                    },
                    'ExactlyMatch':True
                }
            dictionary.append(sub_dictionary)

        self.jsonFileIO.writeJsonFile(dictionary, os.path.join(ROOT, 'Module_Util/test/json/test.json'))
        self.assertTrue(os.path.exists(os.path.join(ROOT, 'Module_Util/test/json/test.json')))
        shutil.rmtree(os.path.join(ROOT, 'Module_Util/test/json/test.json'))

    def test_read_jsonLine_data(self):
        jsonFile = os.path.join(ROOT, 'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/patch/HumanEval_CodeLlama_Lora_Demo_Patch05_TEST.jsonl')

        data = self.jsonFileIO.readJsonLineData(jsonFile)

        for item in data:
            print(item['buggy_code'])
            # output = item['output']
            # for i in range(len(output)):
            #     print(output[str(i)]['output_patch'])
            print("=====================")

if __name__ == '__main__':
    unittest.main()
