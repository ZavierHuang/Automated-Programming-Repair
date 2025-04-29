import os
import unittest

from Config import ROOT
from Module_Analysis.src.new_ResultAnalysis import NewResultAnalysis
from Module_Analysis.src.old_ResultAnalysis import OldResultAnalysis


class oldResultAnalysis_Test(unittest.TestCase):
    def setUp(self):
        self.newResultAnalysis = NewResultAnalysis()


    def test_result_analysis(self):
        Lora = '08'
        Model = 'Qwen'
        epoch = '5'
        jsonFile = f'Result_Output/HumanEval/{Model}/OtherEpoch/Epoch{epoch}/Lora{Lora}/Json/{Model}_Lora{Lora}_E{epoch}_BS.json'
        self.newResultAnalysis.resultAnalysis(jsonFile)

if __name__ == '__main__':
    unittest.main()
