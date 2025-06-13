import os
import re
import unittest

from Config import ROOT
from Module_Analysis.src.new_ResultAnalysis import NewResultAnalysis
from Module_Util.src.JsonFileIO import JsonFileIO


class oldResultAnalysis_Test(unittest.TestCase):
    def setUp(self):
        self.newResultAnalysis = NewResultAnalysis()


    def test_result_analysis(self):
        # diversityList = ['20','40','60','80','100']
        # LoraList = ['04','08','16']
        #
        # for lora in LoraList:
        #     for diversity in diversityList:
        #         print("lora:",lora,"diversity:",diversity)
        #         jsonFile = f'Result_Output/QuixBugs/CodeLlama/diversityBeamSearch{diversity}/Lora{lora}_Multiple/Json/CodeLlama_Lora{lora}_DBS_{diversity}_Multiple.json'
        #         self.newResultAnalysis.resultAnalysis(jsonFile)
        #         print("\n")

        jsonFile = f'Result_Output/HumanEval/Native/Qwen/Json/Qwen_HumanEval_Base10.json'
        self.newResultAnalysis.resultAnalysis(jsonFile)

    def test_pass_Case_Growth_Tendency(self):
        jsonFile = f'Result_Output/QuixBugs/Qwen/BeamSearch/Lora04/Json/Qwen_Lora04_BS.json'
        self.newResultAnalysis.passCaseGrowthTendency(jsonFile)


    def test_pass_but_not_exactly_match(self):
        jsonFile = f'Result_Output/HumanEval/Qwen/OriginalResult/BeamSearch/Lora08/Json/Lora08_E2_BS.json'
        self.newResultAnalysis.passButNotExactlyMatch(jsonFile)

    def test_prompt_repair_add_success_case(self):
        promptJsonFile = f'Result_Output/HumanEval/Qwen/OriginalResult/BeamSearch/Lora08/PromptRepairFolder/Json/BS_Lora08_Qwen_PRE_RES.json'
        originalJsonFile = f'Result_Output/HumanEval/Qwen/OriginalResult/BeamSearch/Lora08/Json/Lora08_E2_BS.json'

        self.newResultAnalysis.promptRepairAddSuccessCase(promptJsonFile, originalJsonFile)

    def test_prompt_compileAndFormatError_repair_case(self):
        LLM = 'Qwen'
        DataSet = 'HumanEval'
        Lora = '08'
        promptJsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/BeamSearch/Lora{Lora}/PromptRepairFolder/Json/BS_Lora{Lora}_{LLM}_PRE_FEM.json'
        originalJsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/BeamSearch/Lora{Lora}/Json/Lora{Lora}_E2_BS.json'
        self.newResultAnalysis.promptRepairErrorCase(promptJsonFile, originalJsonFile)

    def test_get_format_error_case(self):
        LLM = 'Qwen'
        DataSet = 'HumanEval'
        Lora = '08'
        originalJsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/BeamSearch/Lora{Lora}/Json/Lora{Lora}_E2_BS.json'
        self.newResultAnalysis.promptRepairFormatErrorCase(originalJsonFile)

    def test_get_format_error_case_repair_tendency(self):
        LLM = 'Qwen'
        DataSet = 'HumanEval'
        Lora = '08'
        promptJsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/BeamSearch/Lora{Lora}/PromptRepairFolder/Json/BS_Lora{Lora}_{LLM}_PRE_FEM.json'
        self.newResultAnalysis.promptRepairFormatErrorCase_Repair_Tendency(promptJsonFile)

    def test_get_emtpy_patch_result(self):
        # LLM = 'Qwen'
        # DataSet = 'HumanEval'
        # LoraList = ['04', '08', '16']
        #
        # for Lora in LoraList:
        #     print("Lora:",Lora)
        #     jsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/BeamSearch/Lora{Lora}/Json/Lora{Lora}_E2_BS.json'
        #     self.newResultAnalysis.getEmptyPatchCode(jsonFile)

        LLM = 'Qwen'
        DataSet = 'HumanEval'
        LoraList = ['04','08','16']
        diversityList = ['20','40','60','80']

        for diversity in diversityList:
            for Lora in LoraList:
                print("Lora:",Lora,"Diversity:",diversity)
                jsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/DiverseBeamSearch{diversity}/Lora{Lora}/Json/Lora{Lora}_E2_DBS_{diversity}.json'
                self.newResultAnalysis.getEmptyPatchCode(jsonFile)
                print()


    def test_get_buggy_code(self):
        jsonFile = os.path.join(ROOT, 'Data_Storage/HumanEval/CodeLlama/Original_Data/HumanEval_CodeLlama_IR4OR2.jsonl')
        self.jsonFileIO = JsonFileIO()

        data = self.jsonFileIO.readJsonLineData(jsonFile)

        for item in data:
            if item['bug_id'] == 'UNIQUE':
                print(item['buggy_code'])

    def test_error_case(self):
        jsonFile = os.path.join(ROOT, 'Result_Output/QuixBugs/CodeLlama/BeamSearch/Lora04/Json/CodeLlama_Lora04_BS.json')
        self.jsonFileIO = JsonFileIO()
        self.newResultAnalysis.getErrorCase(jsonFile)


    def test_DBS_BS_RepairPart(self):
        DBSJsonFile = os.path.join(ROOT, 'Result_Output/HumanEval/Qwen/OriginalResult/DiverseBeamSearch60/Lora08/Json/Lora08_E2_DBS_60.json')
        BSJsonFile = os.path.join(ROOT, 'Result_Output/HumanEval/Qwen/OriginalResult/BeamSearch/Lora08/Json/Lora08_E2_BS.json')
        self.jsonFileIO = JsonFileIO()
        self.newResultAnalysis.DBS_BS_RepairPart(BSJsonFile, DBSJsonFile)

    def test_repair_failure_because_of_compile_problem(self):
        jsonFile = os.path.join(ROOT, 'Result_Output/HumanEval/Qwen/OriginalResult/BeamSearch/Lora08/Json/Lora08_E2_BS.json')
        self.jsonFileIO = JsonFileIO()
        self.newResultAnalysis.failure_reason(jsonFile)

if __name__ == '__main__':
    unittest.main()
