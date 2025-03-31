import os
import shutil
import unittest

from Config import ROOT
from Src_Module.src.Verification_HumanEval import Verification_HumanEval
from Util_Module.src.FileIO import FileIO
from Util_Module.src.JsonFileIO import JsonFileIO


class Verification_HumanEval_IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.verification_HumanEval = Verification_HumanEval()
        self.verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/HumanEval')
        self.verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')
        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()

    def test_check_java_format_Pass(self):
        self.verification_HumanEval.junitEnvironment_Initialize()

        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)

        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
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

        self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)

        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
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
        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        target_pass = self.verification_HumanEval.getJunitEnvironmentPass() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        javaFormatResult = self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)

        if javaFormatResult.returncode == 0:
            compileLog, compileResult = self.verification_HumanEval.checkJavaCompile(target)
            if compileResult is True:
                shutil.move(target, target_pass)

        self.assertFalse(self.fileIO.isPathExist(target))
        self.assertTrue(self.fileIO.isPathExist(target_pass))

    def test_format_pass_compile_error(self):
        self.verification_HumanEval.junitEnvironment_Initialize()
        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        target_pass = self.verification_HumanEval.getJunitEnvironmentPass() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        methodCode = """
        public static int add(int x,int y){
            String a = x;
            return a + y;
        }
        """

        javaFormatResult = self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)

        if javaFormatResult.returncode == 0:
            compileLog, compileResult = self.verification_HumanEval.checkJavaCompile(target)
            if compileResult is True:
                shutil.move(target, target_pass)

        self.assertTrue(self.fileIO.isPathExist(target))
        self.assertFalse(self.fileIO.isPathExist(target_pass))

if __name__ == '__main__':
    unittest.main()