import os
import re
import shutil
import subprocess
import time
import unittest

from Config import ROOT, CACHE_PATH, GRADLE_PATH
from Src_Module.src.LLM_CodeLlama import LLM_CodeLlama
from Src_Module.src.Verification import Verification
from Src_Module.src.Verification_HumanEval import Verification_HumanEval
from Util_Module.src.FileIO import FileIO
from Util_Module.src.JsonFileIO import JsonFileIO


class Verification_HumanEval_Test(unittest.TestCase):
    def setUp(self):
        self.verification = Verification()
        self.verification_HumanEval = Verification_HumanEval()
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
        self.verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
        self.verification_HumanEval.setScriptPath('Tool/execute_python_humanEval.sh')
        self.verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')
        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()
        self.model_CodeLlama = LLM_CodeLlama()

    def normalize(self, text):
        # Replace all symbols other than numbers and letters with spaces
        return re.sub(r'[^A-Za-z0-9]', '', text)

    def test_get_Import_Content(self):
        buggyId = 'ADD'
        expected = 'import java.util.*;'
        self.assertEqual(self.verification_HumanEval.getImportContent(buggyId), expected)

        buggyId = 'ISCUBE'
        expected = 'import java.util.*;\nimport java.math.BigDecimal;\nimport java.math.RoundingMode;'
        self.assertEqual(self.verification_HumanEval.getImportContent(buggyId), expected)

    def test_create_Valid_Java_Code(self):
        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        remainderCodeFilePath = self.verification_HumanEval.remainCodePath + '/' + buggyId + '.txt'

        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        remainderCode = self.verification.readRemainderCode(remainderCodeFilePath)
        importContent = self.verification_HumanEval.getImportContent(buggyId)

        completedJavaCode = f"""
        {importContent}
        public class {patchFileName} {{
            {methodCode}
            {remainderCode}
        }}
        """

        expectedResult = f"""
        import java.util.*;
        public class ADD_TEST_1 {{
            public static int add(int x,int y){{
                return x + y;
            }}
        }}
        """

        self.assertEqual(self.normalize(completedJavaCode), self.normalize(expectedResult))

    def test_1_junit_initialize(self):
        self.verification_HumanEval.junitEnvironment_Clear(self.verification_HumanEval.getJunitEnvironment())
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getJunitEnvironment())),0)

    def test_2_write_data_in_junit_environment(self):
        self.test_1_junit_initialize()
        javaCode = f"""
        import java.util.*;
        public class ADD_TEST_1 {{
        public static int add(int x,int y){{
            return x + y;
        }}
        }}
        """

        self.verification_HumanEval.junitEnvironment_Initialize()

        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format('Add', 'ADD_TEST_1')
        if self.fileIO.isPathExist(target):
            self.fileIO.deleteFileData(target)

        self.fileIO.writeFileData(target, javaCode)
        self.assertTrue(self.fileIO.isPathExist(target))

        readData = self.fileIO.readFileData(target)
        self.assertEqual(self.normalize(readData), self.normalize(javaCode))

    def test_3_check_java_format_Pass(self):
        self.test_2_write_data_in_junit_environment()
        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        self.verification_HumanEval.setGoogleJavaFormat('Tool/google-java-format-1.18.1-all-deps.jar')
        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        result = self.verification_HumanEval.subprocess_run_JavaFormat(target)

        print(self.fileIO.isPathExist(target))
        print(result)

        self.assertEqual(result.returncode, 0)

    def test_check_STRING_TO_MD5_Compile(self):
        javaFile = os.path.join(ROOT, 'Util_Module/test/compileCheckTestFile/STRING_TO_MD5.java')
        compileLog, compileResult = self.verification_HumanEval.checkJavaCompile(javaFile, True)

        """
        CompletedProcess(args=['javac', '-d', \
        'F:\\GITHUB\\Automated-Programming-Repair\\cache/class_file', \
        'F:\\GITHUB\\Automated-Programming-Repair\\Util_Module/test/compileCheckTestFile/STRING_TO_MD5.java'], \
        returncode=1,
        stdout='',
        stderr='F:\\GITHUB\\Automated-Programming-Repair\\Util_Module\\test\\compileCheckTestFile\\STRING_TO_MD5.java:\
        3: error: package javax.xml.bind does not exist\nimport javax.xml.bind.DatatypeConverter;\n                     ^\n
        F:\\GITHUB\\Automated-Programming-Repair\\Util_Module\\test\\compileCheckTestFile\\STRING_TO_MD5.java:12: error: cannot find symbol\n
        return DatatypeConverter.printHexBinary(digest).toLowerCase();\n               ^\n
        symbol:   variable DatatypeConverter\n
        location: class STRING_TO_MD5\n2 errors\n')
        """

        self.assertTrue(compileResult)

    def test_batchSize_load_junit_environment_create_json_framework(self):
        self.verification_HumanEval.junitEnvironment_Initialize()
        self.verification_HumanEval.junitEnvironment_Run_Initialize()
        self.verification_HumanEval.setTestDataResult(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/Temperature_8/Lora04/patchResult/HumanEval_CodeLlama_Lora04_E1_Patch05_TEST.jsonl')
        data = self.jsonFileIO.readJsonLineData(self.verification_HumanEval.getTestData())
        print(self.fileIO.isPathExist(self.verification_HumanEval.getTestData()))
        dictionary = []

        passNums = 0

        for item in data:

            buggyId = item['bug_id']
            buggyCode = item['buggy_code']
            output = item['output']
            solution = item['gold_patch']

            subdictionary = {'output':{}}

            for i in range(len(output)):

                patchFileName = '{}_TEST_{}'.format(buggyId, str(i))
                patchCode = output[str(i)]['output_patch']
                target = os.path.join(self.verification_HumanEval.getJunitEnvironment(),
                                      'Module_{}/{}.java'.format(buggyId, patchFileName))
                targetModule = os.path.join(self.verification_HumanEval.getJunitModuleTestEnvironment(), 'Module_{}/src/main/java/{}.java'.format(buggyId, patchFileName))

                methodCode = self.model_CodeLlama.patchReplaceByModel(buggyCode, patchCode)
                javaFormatLog, javaFormatResult = self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)
                compileLog, compileResult = self.verification_HumanEval.checkJavaCompile(target, javaFormatResult)
                print(compileResult, compileLog)
                self.fileIO.moveFile(target, targetModule, compileResult)

                subdictionary['output'][i] = self.jsonFileIO.getJsonResultSubItem(patchCode, compileLog, compileResult, javaFormatLog, javaFormatResult, solution)

                if compileResult is True:
                    passNums += 1

            dictionary.append(subdictionary)

        print(dictionary)

        self.assertEqual(passNums, len(self.verification_HumanEval.getAllRunTestCaseFileList())-163)

        self.jsonFileIO.writeJsonFile(dictionary, os.path.join(ROOT, 'Util_Module/test/json/test.json'))
        self.assertTrue(os.path.exists(os.path.join(ROOT, 'Util_Module/test/json/test.json')))

    def test_run_test_case_script(self):
        testModuleName = 'Module_ADD'
        programFileName = 'ADD_TEST'
        gradlePath = GRADLE_PATH
        logFolder = os.path.join(ROOT, 'Util_Module/test/Log')
        os.makedirs(logFolder, exist_ok=True)

        junitModuleEnvironment = self.verification_HumanEval.getJunitModuleTestEnvironment()

        params = [testModuleName, programFileName, logFolder, gradlePath, junitModuleEnvironment]
        self.verification_HumanEval.runBashScript(params)
        target = os.path.join(ROOT, 'Util_Module/test/Log/{}.txt'.format(programFileName))
        self.assertTrue(os.path.exists(target))

        logContent = self.fileIO.readFileData(target)
        self.assertTrue('BUILD FAILED' in logContent or 'BUILD SUCCESSFUL' in logContent)

    def test_run_test_case_script_batchSize(self):
        # self.test_batchSize_load_junit_environment_create_json_framework()
        """
        【Movement】 move file from junit_environment_pass folder to junit_module_environment and ready to run testcase
        【Replace】if file name is ADD_TEST_1, then all 'ADD' will be replaced with 'ADD_TEST_1' in the testcase file
        【Recovery】when all test case end, then all 'ADD_TEST_1' will be replaced with 'ADD' in the testcase file
        """
        runFileList = self.verification_HumanEval.getAllRunTestCaseFileList()
        
        for file in runFileList:
            print(file)



if __name__ == '__main__':
    unittest.main()