import os
import unittest

from Config import ROOT
from Src_Module.src.LLM_CodeLlama import LLM_CodeLlama
from Src_Module.src.Verification_HumanEval import Verification_HumanEval
from Util_Module.src.FileIO import FileIO
from Util_Module.src.JsonFileIO import JsonFileIO


class Verification_HumanEval_IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.verification_HumanEval = Verification_HumanEval()
        self.verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
        self.verification_HumanEval.setScriptPath('Tool/execute_python_humanEval.sh')
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
        self.verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')
        self.verification_HumanEval.setTestDataResult(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/patch/HumanEval_CodeLlama_Lora04_E1_Patch05_TEST.jsonl')


        self.verification_HumanEval.setJsonResultPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/Json/test.json')
        self.verification_HumanEval.setLogFolderPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/Log')
        self.verification_HumanEval.setRepairProgramPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/repairProgram')
        self.verification_HumanEval.setPromptRepairProgramPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/promptRepairProgram')
        self.verification_HumanEval.setLogFolderPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/Log')

        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()
        self.model_CodeLlama = LLM_CodeLlama()

    def test_check_java_format_Pass(self):
        self.verification_HumanEval.junitEnvironment_Initialize()

        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        javaFormatLog, javaFormatResult = self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)
        print(javaFormatLog, javaFormatResult)
        self.assertTrue(javaFormatResult)

        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        self.assertTrue(self.fileIO.isPathExist(target))

    def test_check_java_format_Failure(self):
        self.verification_HumanEval.junitEnvironment_Initialize()

        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_2'
        methodCode = """
        public static int add(int x,int y){
            return x + y
        }
        """

        javaFormatLog, javaFormatResult = self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)
        self.assertFalse(javaFormatResult)

        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        self.assertTrue(self.fileIO.isPathExist(target))

    def test_clear_humanEval_run_test_case_module_folder(self):
        self.verification_HumanEval.junitEnvironment_Module_Test_Clear()
        subFolderList = self.fileIO.getRunTestCaseModuleFolderList(self.verification_HumanEval.getJunitModuleTestEnvironment())
        for subFolder in subFolderList:
            fileList = self.fileIO.getFileListUnderFolder(os.path.join(subFolder, 'src/main/java'))
            self.assertEqual(len(fileList), 0)

    def test_format_and_compile_both_pass(self):
        self.verification_HumanEval.junitEnvironment_Initialize()

        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        javaFormatLog, javaFormatResult = self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)
        compileLog, compileResult = self.verification_HumanEval.checkJavaCompile(target, javaFormatResult)
        self.assertTrue(compileResult)

    def test_format_pass_compile_error(self):
        self.verification_HumanEval.junitEnvironment_Initialize()
        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        methodCode = """
        public static int add(int x,int y){
            String a = x;
            return a + y;
        }
        """

        javaFormatLog, javaFormatResult = self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)
        compileLog, compileResult = self.verification_HumanEval.checkJavaCompile(target, javaFormatResult)
        self.assertFalse(compileResult)

    def test_load_and_run_test_case(self):
        self.verification_HumanEval.junitEnvironment_Initialize()
        self.verification_HumanEval.junitEnvironment_Run_Initialize()
        self.verification_HumanEval.createJsonFramework()
        self.verification_HumanEval.createPromptRepairProgramSet()
        runFileList = self.verification_HumanEval.getAllRunTestCaseFileList()
        dictionary = self.verification_HumanEval.getFileAndModuleDict(runFileList)
        self.verification_HumanEval.runScriptBatchFile(dictionary)
        self.verification_HumanEval.updateJsonResult()

        self.assertTrue(len(dictionary), len(self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getLogFolderPath())))


        data = self.jsonFileIO.readJsonData(self.verification_HumanEval.getJsonResultPath())
        repair = 0
        runTestCasePass = 0
        for item in data:
            if item['repair']:
                repair += 1
                output = item['output']
                for i in range(len(output)):
                    if output[str(i)]['PassTestCase']:
                        runTestCasePass += 1
        self.assertEqual(repair, 2)
        self.assertEqual(runTestCasePass, 3)

    def test_result_analysis(self):
        jsonFilePath = os.path.join(ROOT, 'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/Json/test.json')
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