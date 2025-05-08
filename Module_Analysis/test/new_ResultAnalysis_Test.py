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
        promptJsonFile = 'Result_Output/QuixBugs/CodeLlama/diversityBeamSearch100/Lora04/PromptRepairFolder/Json/DBS_Lora04_100_CodeLlama_PRE_RES.json'
        originalJsonFile = 'Result_Output/QuixBugs/CodeLlama/diversityBeamSearch100/Lora04/Json/CodeLlama_Lora04_DBS_100.json'

        self.newResultAnalysis.promptRepairAddSuccessCase(promptJsonFile, originalJsonFile)


if __name__ == '__main__':
    unittest.main()
