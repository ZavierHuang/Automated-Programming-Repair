import shutil
import unittest

from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs
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

    def test_multiple_fill_json_create(self):
        self.verification_QuixBugs = Verification_QuixBugs()
        self.verification_QuixBugs.setLLMModel(LLM_Qwen())
        jsonFilePaths = os.path.join(ROOT, 'Module_Src/test/tempJsonData/Qwen_Patch05_first.jsonl')
        outputJsonFilePaths = os.path.join(ROOT, 'Module_Src/test/tempJsonData/Qwen_test_Multiple_Src.jsonl')
        data = self.jsonFileIO.readJsonLineData(jsonFilePaths)

        outputJsonFileList = []
        for item in data:
            if item['bug_id'] not in ['BREADTH_FIRST_SEARCH','FLATTEN','LCS_LENGTH']:
                continue

            buggyCode = item['buggy_code']
            print(buggyCode)
            print("======================================")
            output = item['output']
            for i in range(len(output)):
                patchCode = output[str(i)]['output_patch']
                newBuggyCode = self.verification_QuixBugs.getLLMModel().patchReplaceByModel(buggyCode, patchCode)
                newBuggyCode = self.verification_QuixBugs.getLLMModel().remarkErrorPosition(newBuggyCode)

                dictionary = {
                    'bug_id': item['bug_id'] + '_' + str(i),
                    'buggyCode': newBuggyCode,
                    'fixed_chunk': item['gold_patch'],
                }
                outputJsonFileList.append(dictionary)

        self.jsonFileIO.writeJsonLineFile(outputJsonFileList, outputJsonFilePaths)
        self.assertTrue(self.jsonFileIO.isPathExist(outputJsonFilePaths))

        data = self.jsonFileIO.readJsonLineData(outputJsonFilePaths)
        self.assertEqual(len(data), 15)

        for item in data:
            buggyCode = item['buggyCode']
            if self.verification_QuixBugs.getLLMModel().getLLMName() == 'CodeLlama':
                self.assertEqual(buggyCode.count('buggy code'), 1)
                self.assertEqual(buggyCode.count('<FILL_ME>'), 1)
            elif self.verification_QuixBugs.getLLMModel().getLLMName() == 'Qwen':
                PREFIX = '<|fim_prefix|>'
                MIDDLE = '<|fim_middle|>'
                SUFFIX = '<|fim_suffix|>'
                self.assertEqual(buggyCode.count('buggy code'), 1)
                self.assertEqual(buggyCode.count(PREFIX), 1)
                self.assertEqual(buggyCode.count(MIDDLE), 1)
                self.assertEqual(buggyCode.count(SUFFIX), 1)
            else:
                print("ERROR")

    def test_read_jsonFIle(self):
        data = self.jsonFileIO.readJsonLineData(os.path.join(ROOT, 'Data_Storage/HumanEval/CodeLlama/Original_Data/HumanEval_CodeLlama_IR4OR2.jsonl'))

        for item in data:
            print(item['bug_id'])
            print(item['buggy_code'])
            print("============================================")

    def test_read_quixBugs_solution(self):
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, 'Data_Storage/QuixBugs/Solution/QuixBugsSolution.json'))
        for item in data:
            print(data[item])

if __name__ == '__main__':
    unittest.main()
