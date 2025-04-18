import os
import unittest

from Config import ROOT
from Module_Analysis.src.new_ResultAnalysis import NewResultAnalysis
from Module_Analysis.src.old_ResultAnalysis import OldResultAnalysis


class oldResultAnalysis_Test(unittest.TestCase):
    def setUp(self):
        self.newResultAnalysis = NewResultAnalysis()


    def test_result_analysis(self):
        jsonFile = 'Result_Output/QuixBugs/Qwen/BeamSearch/Lora04/Json/Lora04_E2_BS.json'
        self.newResultAnalysis.resultAnalysis(jsonFile)

if __name__ == '__main__':
    unittest.main()
