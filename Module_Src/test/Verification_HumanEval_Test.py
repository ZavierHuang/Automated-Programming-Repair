import os
import re
import shutil
import subprocess
import time
import unittest

from Config import ROOT, CACHE_PATH, GRADLE_PATH
from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.Verification import Verification
from Module_Src.src.Verification_HumanEval import Verification_HumanEval
from Module_Util.src.FileIO import FileIO
from Module_Util.src.JsonFileIO import JsonFileIO


class Verification_HumanEval_Test(unittest.TestCase):
    def setUp(self):
        self.verification = Verification()
        self.verification_HumanEval = Verification_HumanEval()
        self.verification_HumanEval.setDataSetName('HumanEval')
        self.verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
        self.verification_HumanEval.setScriptPath('Tool/execute_python.sh')
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
        self.verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')

        self.verification_HumanEval.setTestDataResult('Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/patch/HumanEval_CodeLlama_Lora_Demo_Patch05_TEST.jsonl')

        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()
        self.model_CodeLlama = LLM_CodeLlama()

    def setUp2(self):
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

    def normalize(self, text):
        # Replace all symbols other than numbers and letters with empty
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
        self.verification_HumanEval.junitEnvironment_Initialize()
        javaCode = f"""
        import java.util.*;
        public class ADD_TEST_1 {{
        public static int add(int x,int y){{
            return x + y;
        }}
        }}
        """

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
        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        result = self.verification_HumanEval.subprocess_run_JavaFormat(target)
        self.assertEqual(result.returncode, 0)

    def test_check_STRING_TO_MD5_Compile(self):
        javaFile = os.path.join(ROOT, 'Module_Util/test/compileCheckTestFile/STRING_TO_MD5.java')
        compileLog, compileResult = self.verification_HumanEval.checkJavaCompile(javaFile, True)

        """
        CompletedProcess(args=['javac', '-d', \
        'F:\\GITHUB\\Automated-Programming-Repair\\cache/class_file', \
        'F:\\GITHUB\\Automated-Programming-Repair\\Module_Util/test/compileCheckTestFile/STRING_TO_MD5.java'], \
        returncode=1,
        stdout='',
        stderr='F:\\GITHUB\\Automated-Programming-Repair\\Module_Util\\test\\compileCheckTestFile\\STRING_TO_MD5.java:\
        3: error: package javax.xml.bind does not exist\nimport javax.xml.bind.DatatypeConverter;\n                     ^\n
        F:\\GITHUB\\Automated-Programming-Repair\\Module_Util\\test\\compileCheckTestFile\\STRING_TO_MD5.java:12: error: cannot find symbol\n
        return DatatypeConverter.printHexBinary(digest).toLowerCase();\n               ^\n
        symbol:   variable DatatypeConverter\n
        location: class STRING_TO_MD5\n2 errors\n')
        """

        self.assertTrue(compileResult)

    def test_batchSize_load_junit_environment_create_json_framework(self):
        self.setUp2()
        self.verification_HumanEval.junitEnvironment_Initialize()
        self.verification_HumanEval.junitEnvironment_Run_Initialize()
        self.verification.HumanEval.juniEnvironment_TEST_File_Initialize()
        data = self.jsonFileIO.readJsonLineData(self.verification_HumanEval.getTestData())
        dictionary = []

        passNums = 0

        for item in data:

            buggyId = item['bug_id']
            buggyCode = item['buggy_code']
            output = item['output']
            solution = item['gold_patch']

            subdictionary = {
                'buggyId': buggyId,
                'repair': False,
                'solution': solution,
                'type': self.verification_HumanEval.checkBuggyMethodLine(buggyCode),
                'output': {}
            }

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
                self.fileIO.copyFile(target, targetModule, compileResult)
                self.fileIO.moveFile(target, self.verification_HumanEval.getRepairProgramPath(), compileResult)

                subdictionary['output'][i] = self.jsonFileIO.getJsonResultSubItem(patchCode, compileLog, compileResult, javaFormatLog, javaFormatResult, solution)

                if compileResult is True:
                    passNums += 1

            dictionary.append(subdictionary)

        print(dictionary)

        self.assertEqual(passNums, len(self.verification_HumanEval.getAllRunTestCaseFileList()))
        self.jsonFileIO.writeJsonFile(dictionary, self.verification_HumanEval.getJsonResultPath())
        self.assertTrue(os.path.exists(os.path.join(ROOT, self.verification_HumanEval.getJsonResultPath(),)))

    def test_copy_promptRepairProgram_from_Junit_Environment(self):
        self.verification_HumanEval.setPromptRepairProgramPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/promptRepairProgram')

        source = self.verification_HumanEval.getJunitEnvironment()
        destination = self.verification_HumanEval.getPromptRepairProgramPath()

        shutil.copytree(source, destination, dirs_exist_ok=True)

        self.assertTrue(os.path.exists(destination))
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(source)), len(self.fileIO.getFileListUnderFolder(destination)))

    def write_ADD_File(self, target, programFileName):
        javaCode = f"""
            import java.util.*;
            public class {programFileName} {{
                public static int add(int x, int y) {{
                return x+y;
            }}
            }}
        """

        if self.fileIO.isPathExist(target):
            self.fileIO.deleteFileData(target)

        self.fileIO.writeFileData(target, javaCode)

    def test_run_test_case_script_expect_failure(self):
        # make sure the program can run test case
        self.verification_HumanEval.junitEnvironment_Initialize()
        self.verification_HumanEval.junitEnvironment_Run_Initialize()
        self.verification.HumanEval.juniEnvironment_TEST_File_Initialize()

        self.verification_HumanEval.setLogFolderPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/Log')

        LogFolder = self.verification_HumanEval.getLogFolderPath()

        testModuleName = 'Module_ADD'
        programFileName = 'ADD_TEST_1'

        target = os.path.join(ROOT, 'JUnit_ModuleTest/RunTestCase_HumanEval/Module_ADD/src/main/java/{}.java'.format(programFileName))
        self.write_ADD_File(target, programFileName)

        self.assertTrue(self.fileIO.isPathExist(target))

        junitModuleEnvironment = self.verification_HumanEval.getJunitModuleTestEnvironment()

        params = [testModuleName, programFileName, LogFolder, GRADLE_PATH, junitModuleEnvironment]

        self.verification_HumanEval.runBashScript(params)
        target = os.path.join(LogFolder,'{}.txt'.format(programFileName))
        self.assertTrue(os.path.exists(target))

        logContent = self.fileIO.readFileData(target)
        self.assertTrue('BUILD FAILED' in logContent)

    def test_run_test_case_batchSize_get_dictionary(self):
        self.setUp2()
        self.verification_HumanEval.createJsonFramework([])
        """
        【Movement】 move file from junit_environment_pass folder to junit_module_environment and ready to run testcase
        【Replace】if file name is ADD_TEST_1, then all 'ADD' will be replaced with 'ADD_TEST_1' in the testcase file
        【Recovery】when all test case end, then all 'ADD_TEST_1' will be replaced with 'ADD' in the testcase file
        """
        runFileList = self.verification_HumanEval.getAllRunTestCaseFileList()
        pass_file_module_dic = self.verification_HumanEval.getFileAndModuleDict(runFileList)

        failureFileList = self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getJunitEnvironment())
        failure_file_module_dic = self.verification_HumanEval.getFileAndModuleDict(failureFileList)

        print(pass_file_module_dic)
        print(failure_file_module_dic)

        total_item = len(set(pass_file_module_dic.values()) or set(failure_file_module_dic.values()))
        total_program = len(pass_file_module_dic.keys()) + len(failure_file_module_dic.keys())

        self.assertEqual(total_item * 5, total_program)

    def test_run_script_starter(self):
        self.verification_HumanEval.junitEnvironment_Initialize()
        self.verification_HumanEval.junitEnvironment_Run_Initialize()
        self.verification.HumanEval.juniEnvironment_TEST_File_Initialize()

        self.verification_HumanEval.setLogFolderPath(
            'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Demo/Log')

        pendingRunningFile = """
        import java.util.*;
        public class ADD_TEST_9{
            public static int add(int x, int y){
                return x + y;
            }
        }
        """

        targetFile = os.path.join(self.verification_HumanEval.getJunitModuleTestEnvironment(), 'Module_ADD/src/main/java/ADD_TEST_9.java')

        self.fileIO.writeFileData(targetFile, pendingRunningFile)
        self.assertTrue(os.path.exists(targetFile))

        runFileList = self.verification_HumanEval.getAllRunTestCaseFileList()

        # {'ADD_TEST_9': 'ADD'}
        pass_file_module_dic = self.verification_HumanEval.getFileAndModuleDict(runFileList)

        for item in pass_file_module_dic.items():
            newName = item[0] + '.'                     # ADD_TEST_9.
            oldName = item[1] + '.'                     # ADD.
            moduleName = 'Module_{}'.format(item[1])
            testFilePath = os.path.join(
                self.verification_HumanEval.getJunitModuleTestEnvironment(),
                "{}/src/test/java/{}_TEST.java".format(moduleName, item[1])
            )
            self.fileIO.replaceName(testFilePath, oldName, newName)
            self.verification_HumanEval.runScriptSingleFile(item[0], moduleName)
            self.fileIO.replaceName(testFilePath, newName, oldName)


        self.assertTrue(os.path.exists(os.path.join(self.verification_HumanEval.getLogFolderPath(), 'ADD_TEST_9.txt')))
        self.fileIO.deleteFileData(os.path.join(self.verification_HumanEval.getLogFolderPath(), 'ADD_TEST_9.txt'))
        self.fileIO.deleteFileData(targetFile)
        self.assertFalse(os.path.exists(os.path.join(self.verification_HumanEval.getLogFolderPath(), 'ADD_TEST_9.txt')))
        self.assertFalse(os.path.exists(targetFile))

    def test_check_buggy_method_buggy_Line(self):
        buggyMethod = """
        public static int add(int x, int y){
            // buggy code
            // return x*y
            return x + y;
        }
        """
        self.assertEqual(self.verification_HumanEval.checkBuggyMethodLine(buggyMethod), 'Single')

if __name__ == '__main__':
    unittest.main()


