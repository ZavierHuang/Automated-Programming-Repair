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
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
        self.verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')
        self.verification_HumanEval.setScriptPath('Tool/execute_python_humanEval.sh')
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

        self.verification_HumanEval.setTestDataResult(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Lora04/patchResult/HumanEval_CodeLlama_Lora04_E1_Patch05_TEST.jsonl')

        self.verification_HumanEval.setLogFolderPath('Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Lora04/Log/Test')
        self.verification_HumanEval.setJsonResultPath('Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Lora04/Json_Result/test.json')
        self.verification_HumanEval.createJsonFramework()
        runFileList = self.verification_HumanEval.getAllRunTestCaseFileList()
        dictionary = self.verification_HumanEval.getFileAndModuleDict(runFileList)
        self.verification_HumanEval.runScriptBatchFile(dictionary)

        self.assertTrue(len(dictionary), len(self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getLogFolderPath())))




if __name__ == '__main__':
    unittest.main()