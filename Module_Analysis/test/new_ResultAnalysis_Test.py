import os
import unittest

from Config import ROOT
from Module_Analysis.src.new_ResultAnalysis import NewResultAnalysis
from Module_Analysis.src.old_ResultAnalysis import OldResultAnalysis


class oldResultAnalysis_Test(unittest.TestCase):
    def setUp(self):
        self.newResultAnalysis = NewResultAnalysis()


    def test_result_analysis(self):
        Lora = '16'
        Model = 'CodeLlama'
        Diversity = '20'
        jsonFile = f'Result_Output/HumanEval/{Model}/OriginalResult/DiverseBeamSearch{Diversity}/Lora{Lora}/Json/Lora{Lora}_E2_DBS_{Diversity}.json'
        self.newResultAnalysis.resultAnalysis(jsonFile)

if __name__ == '__main__':
    unittest.main()
