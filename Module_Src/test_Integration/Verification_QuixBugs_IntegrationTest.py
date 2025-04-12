import os
import unittest

from Config import ROOT
from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs
from Module_Util.src.FileIO import FileIO
from Module_Util.src.JsonFileIO import JsonFileIO


class verification_QuixBugs_IntegrationTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        pass

    def demoUsedSetUp(self):
        self.verification_QuixBugs = Verification_QuixBugs()
        self.verification_QuixBugs.setRemainderCodePath(None)
        self.verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
        self.verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
        self.verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

        self.verification_QuixBugs.setTestDataResult(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/patch/QuixBugs_Qwen_Lora_Demo_Patch05_TEST.jsonl')

        self.verification_QuixBugs.setJsonResultPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/Json/test.json')
        self.verification_QuixBugs.setRepairProgramPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/repairProgram')
        self.verification_QuixBugs.setPromptRepairProgramPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/promptRepairProgram')
        self.verification_QuixBugs.setLogFolderPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/Log')

        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()
        self.verification_QuixBugs.setLLMModel(LLM_Qwen())


    def test_load_and_run_test_case(self):
        self.demoUsedSetUp()
        self.verification_QuixBugs.junitEnvironment_Initialize()
        self.verification_QuixBugs.junitEnvironment_Run_Initialize()
        self.verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
        self.verification_QuixBugs.createJsonFramework()
        self.verification_QuixBugs.createPromptRepairProgramSet()
        runFileList = self.verification_QuixBugs.getAllRunTestCaseFileList()
        dictionary = self.verification_QuixBugs.getFileAndModuleDict(runFileList)
        self.verification_QuixBugs.runScriptBatchFile(dictionary)

        self.verification_QuixBugs.updateJsonResult()
        self.assertTrue(len(dictionary), len(self.fileIO.getFileListUnderFolder(self.verification_QuixBugs.getLogFolderPath())))

    def test_result_analysis(self):
        jsonFilePath = os.path.join(ROOT, 'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/Json/test.json')
        data = self.jsonFileIO.readJsonData(jsonFilePath)

        for item in data:
            if item['repair']:
                print(item['buggyId'])
            output = item['output']
            for i in range(len(output)):
                if output[str(i)]['exactlyMatch']:
                    print(item['buggyId'], i, 'exactly match:', output[str(i)]['exactlyMatch'])
                if output[str(i)]['PassTestCase']:
                    print(item['buggyId'], i, 'pass test case:', output[str(i)]['PassTestCase'])


if __name__ == '__main__':
    # integration test
    unittest.main()