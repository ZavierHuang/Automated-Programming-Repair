import re
import unittest
from Module_Analysis.src.new_ResultAnalysis import NewResultAnalysis


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
        jsonFile = f'Result_Output/HumanEval/Native/CodeLlama/Json/CodeLlama_HumanEval_Base10.json'
        self.newResultAnalysis.passCaseGrowthTendency(jsonFile)


    def test_pass_but_not_exactly_match(self):
        jsonFile = f'Result_Output/HumanEval/Qwen/OriginalResult/BeamSearch/Lora08/Json/Lora08_E2_BS.json'
        self.newResultAnalysis.passButNotExactlyMatch(jsonFile)

    def test_prompt_reapir_add_success_case(self):
        LLM = 'Qwen'
        DataSet = 'HumanEval'
        for Lora in ['04', '08', '16']:
            print("LORA:", Lora)
            promptJsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/BeamSearch/Lora{Lora}/PromptRepairFolder/Json/BS_Lora{Lora}_{LLM}_PRE_RES.json'
            originalJsonFile = f'Result_Output/{DataSet}/{LLM}/OriginalResult/BeamSearch/Lora{Lora}/Json/Lora{Lora}_E2_BS.json'

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

if __name__ == '__main__':
    unittest.main()
