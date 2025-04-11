import os
import unittest

from Config import ROOT
from Module_Analysis.src.old_ResultAnalysis import OldResultAnalysis


class oldResultAnalysis_Test(unittest.TestCase):
    def setUp(self):
        self.oldResultAnalysis = OldResultAnalysis()


    def test_old_beam_search_result(self):
        resultFilePath = os.path.join(ROOT, 'BeamSearchResult/JsonResult/QuixBugs/Multiple_Position_Error/JSON_CodeLlama/QuixBugs_CodeLlama_LORA04_EPOCH_2_PATCH_10.json')
        mechanismFilePath = os.path.join(ROOT, 'BeamSearchResult/CompileAnalysis/QuixBugs_Multiple/Message/CodeLlama_QuixBugs_Lora04_Epoch2_Patch10_Message.json')
        self.oldResultAnalysis.setLLM('CodeLlama')
        self.oldResultAnalysis.setLora('LORA04')
        self.oldResultAnalysis.setTotalProgram(3)

        self.assertTrue(self.oldResultAnalysis.getLora().lower() in resultFilePath.lower())
        self.assertTrue(self.oldResultAnalysis.getLora().lower() in mechanismFilePath.lower())
        self.assertTrue(self.oldResultAnalysis.getLLM().lower() in resultFilePath.lower())
        self.assertTrue(self.oldResultAnalysis.getLLM().lower() in mechanismFilePath.lower())

        self.oldResultAnalysis.resultAnalysis(resultFilePath,mechanismFilePath)

        report = self.oldResultAnalysis.getReport()

        totalProgram = report[self.oldResultAnalysis.getLLM()]['Total Program']
        repairSuccessfully = report[self.oldResultAnalysis.getLLM()]['Repair Successfully']
        repairFailure = report[self.oldResultAnalysis.getLLM()]['Repair Failure']
        singleLine = report[self.oldResultAnalysis.getLLM()]['Single Line']
        multipleLine = report[self.oldResultAnalysis.getLLM()]['Multiple Line']
        exactlyMatch = report[self.oldResultAnalysis.getLLM()]['Exactly Match']

        totalPatch = report['Total']['Total Patch']
        formatError = report['Total']['Format Error']
        compileError = report['Total']['Compile Error']
        runTestCase = report['Total']['Run Test Case']
        failTestCase = report['Total']['Fail Test Case']
        passTestCase = report['Total']['Pass Test Case']

        self.assertEqual(repairSuccessfully, singleLine + multipleLine)
        self.assertEqual(totalProgram, repairSuccessfully + repairFailure)
        self.assertEqual(totalPatch, formatError + compileError + runTestCase)
        self.assertEqual(runTestCase, failTestCase + passTestCase)


if __name__ == '__main__':
    unittest.main()
