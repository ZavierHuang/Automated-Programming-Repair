import os
import shutil
import unittest

from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama
from Module_LLM_PER.src.LLM_PER import LLM_PER
from Module_Util.src.FileIO import FileIO


class LLM_Model_Integration_Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.promptEngineer = LLM_LangChain_CodeLlama()
        self.fileIO = FileIO()

    def setUp(self):
        pass

    def test_prompt_Two_File_LLM_Prediction(self):
        self.promptEngineer.setPromptRepairFileRoot('Module_LLM_PER/test/SingleFileTest')

        if self.fileIO.isPathExist(os.path.join(self.promptEngineer.getPromptRepairFileRoot(),'PromptRepairFile')):
            shutil.rmtree(os.path.join(self.promptEngineer.getPromptRepairFileRoot(),'PromptRepairFile'))
            self.assertFalse(self.fileIO.isPathExist(os.path.join(self.promptEngineer.getPromptRepairFileRoot(),'PromptRepairFile')))

        self.promptEngineer.setPendingRepairFileListPath('Module_LLM_PER/test/SingleFileTest/testFile')
        self.promptEngineer.setOutputJsonFilePath('Module_LLM_PER/test/SingleFileTest/test.json')
        self.promptEngineer.setPER_RepairTimes(5)
        self.promptEngineer.promptRepair()
        self.assertTrue(self.fileIO.isPathExist(self.promptEngineer.getOutputJsonFilePath()))




if __name__ == '__main__':
    unittest.main()