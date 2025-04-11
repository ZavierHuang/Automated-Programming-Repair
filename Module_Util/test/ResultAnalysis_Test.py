import os.path
import unittest
from Module_Util.src.ResultAnalysis import ResultAnalysis


class ResultAnalysis_Test(unittest.TestCase):
    def setUp(self):
        self.resultAnalysis = ResultAnalysis()


    def test_old_beam_search_HumanEval_result(self):
        jsonFilePath = 'BeamSearchResult/JsonResult/HumanEval/JSON_CodeLlama/HumanEval_CodeLlama_LORA04_EPOCH_1_PATCH_10.json'
        para = [jsonFilePath, 'CodeLlama', 'Lora04', 'HumanEval', 163]
        self.resultAnalysis.oldResultAnalysis(para)

if __name__ == '__main__':
    unittest.main()
