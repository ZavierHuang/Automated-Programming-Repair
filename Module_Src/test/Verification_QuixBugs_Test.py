import os
import re
import shutil
import time
import unittest

from Config import ROOT, GRADLE_PATH
from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification import Verification
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs
from Module_Util.src.FileIO import FileIO
from Module_Util.src.JsonFileIO import JsonFileIO


class Verification_QuixBugs_Test(unittest.TestCase):
    def setUp(self):
        self.verification = Verification()
        self.verification_QuixBugs = Verification_QuixBugs()
        self.verification_QuixBugs.setDataSetName('QuixBugs')
        self.verification_QuixBugs.setRemainderCodePath(None)
        self.verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
        self.verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
        self.verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')
        self.verification_QuixBugs.setTestDataResult('Result_Output/QuixBugs/Qwen/BeamSearch/Demo/patch/QuixBugs_Qwen_Lora_Demo_Patch05_TEST.jsonl')

        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()
        self.verification_QuixBugs.setLLMModel(LLM_Qwen())

    def setUp2(self):
        self.verification_QuixBugs.setJsonResultPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/Json/test.json')
        self.verification_QuixBugs.setRepairProgramPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/repairProgram')
        self.verification_QuixBugs.setPromptRepairProgramPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/promptRepairProgram')
        self.verification_QuixBugs.setLogFolderPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/Log')

    def test_get_Import_Content(self):
        path = os.path.join(ROOT, 'Data_Storage/QuixBugs/ImportContent')

        print(self.fileIO.isPathExist(path))
        for root, dirs, files in os.walk(path):
            for file in files:
                ID = file[:file.find('_Import')]
                result = self.fileIO.normalize(self.verification_QuixBugs.getImportContent(ID))
                expect = self.fileIO.normalize(self.fileIO.readFileData(os.path.join(root, file)))
                self.assertEqual(result, expect)

    def test_normalize(self):
        data = r"""
        import dataStructures.*;
        public class BITCOUNT_TEST {
            @org.junit.Test(timeout = 3000)
            public void test_0() throws java.lang.Exception {
                int result = BITCOUNT_TEST_1.bitcount((int)127);
                org.junit.Assert.assertEquals( (int) 7, result);
            }
        }
        """
        result = re.sub(r'_TEST_\d+', '', data)
        print(result)
        self.assertTrue('_TEST_' not in result)

    def test_check_no_file_contains_TEST_Number(self):
        sub_Module_Folder_List = self.fileIO.getRunTestCaseModuleFolderList(self.verification_QuixBugs.getJunitModuleTestEnvironment())
        for subModuleFolderPath in sub_Module_Folder_List:
            test_targetPath = os.path.join(subModuleFolderPath, 'src/test/java')
            self.assertTrue(self.fileIO.isPathExist(test_targetPath))
            fileList = self.fileIO.getFileListUnderFolder(test_targetPath)
            for file in fileList:
                filePath = os.path.join(test_targetPath, file)
                data = self.fileIO.readFileData(filePath)
                result = re.sub(r'_TEST_\d+', '', data)
                self.fileIO.writeFileData(filePath, result)

                print(file)
                data = self.fileIO.readFileData(filePath)
                self.assertTrue('_TEST_' not in data)
            print(fileList)
            print("==========================================")

    def test_check_no_file_contains_TEST_Number_Method(self):
        self.verification_QuixBugs.juniEnvironment_TEST_File_Initialize()

    def test_create_Valid_Java_Code(self):
        buggyId = 'BITCOUNT'
        patchFileName = 'BITCOUNT_TEST_1'
        methodCode = """
        public static int bitcount(int n) {
            int count = 0;
            while (n != 0) {
                n = (n & (n - 1));
                count++;
            }
            return count;
        }
        """

        remainderCode = self.verification.readRemainderCode(None)
        importContent = self.verification_QuixBugs.getImportContent(buggyId)

        completedJavaCode = f"""
        {importContent}
        public class {patchFileName} {{
            {methodCode}
            {remainderCode}
        }}
        """

        expectedResult = f"""
        import java.util.*;
        public class BITCOUNT_TEST_1 {{
            public static int bitcount(int n) {{
            int count = 0;
            while (n != 0) {{
                n = (n & (n - 1));
                count++;
            }}
            return count;
        }}
        }}
        """

        self.assertEqual(self.fileIO.normalize(completedJavaCode), self.fileIO.normalize(expectedResult))

    def test_junit_initialize(self):
        self.verification_QuixBugs.junitEnvironment_Clear(self.verification_QuixBugs.getJunitEnvironment())
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(self.verification_QuixBugs.getJunitEnvironment())),0)

    def test_1_write_data_in_junit_environment(self):
        self.verification_QuixBugs.junitEnvironment_Initialize()

        javaCode = f"""
        import java.util.*;
        public class BITCOUNT_TEST_1 {{
            public static int bitcount(int n) {{
            int count = 0;
            while (n != 0) {{
                n = (n & (n - 1));
                count++;
            }}
            return count;
        }}
        }}
        """

        target = self.verification_QuixBugs.getJunitEnvironment() + '/Module_{}/{}.java'.format('BITCOUNT', 'BITCOUNT_TEST_1')
        if self.fileIO.isPathExist(target):
            self.fileIO.deleteFileData(target)

        self.fileIO.writeFileData(target, javaCode)
        self.assertTrue(self.fileIO.isPathExist(target))

        readData = self.fileIO.readFileData(target)
        self.assertEqual(self.fileIO.normalize(readData), self.fileIO.normalize(javaCode))

    def test_2_check_java_format_Pass(self):
        self.test_1_write_data_in_junit_environment()
        buggyId = 'BITCOUNT'
        patchFileName = 'BITCOUNT_TEST_1'
        target = self.verification_QuixBugs.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        result = self.verification_QuixBugs.subprocess_run_JavaFormat(target)
        self.assertEqual(result.returncode, 0)

    def test_3_check_compile_Pass(self):
        self.test_1_write_data_in_junit_environment()
        buggyId = 'BITCOUNT'
        patchFileName = 'BITCOUNT_TEST_1'
        target = self.verification_QuixBugs.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        javaFormatResult = self.verification_QuixBugs.subprocess_run_JavaFormat(target)
        ErrorMessage, CompileResult = self.verification_QuixBugs.checkJavaCompile(target, javaFormatResult.stderr)
        self.assertTrue(CompileResult)
        self.assertTrue(len(ErrorMessage) == 0)

    def test_check_MINIMUM_SPANNING_TREE_Compile_List(self):
        filePath = os.path.join(ROOT, 'Module_Src/test/MINIMUM_SPANNING_TREE.java')
        importFileList = self.verification_QuixBugs.getNeedCompileJavaFiles(filePath)
        print(importFileList)
        self.assertEqual(len(importFileList), 3)
        self.assertTrue(os.path.join(ROOT, 'Data_Storage/QuixBugs/dataStructures/Node.java') in importFileList)
        self.assertTrue(os.path.join(ROOT, 'Data_Storage/QuixBugs/dataStructures/WeightedEdge.java') in importFileList)

    def test_check_MINIMUM_SPANNING_TREE_Compile_List_Pass(self):
        filePath = os.path.join(ROOT, 'Module_Src/test/MINIMUM_SPANNING_TREE.java')
        javaFormatResult = self.verification_QuixBugs.subprocess_run_JavaFormat(filePath)
        self.assertEqual(javaFormatResult.returncode, 0)
        ErrorMessage, CompileResult = self.verification_QuixBugs.checkJavaCompile(filePath, javaFormatResult.stderr)
        print(ErrorMessage)
        self.assertTrue(CompileResult)
        self.assertTrue(len(ErrorMessage) == 0)

    def test_batchSize_load_junit_environment_create_json_framework(self):
        self.setUp2()

        self.verification_QuixBugs.junitEnvironment_Initialize()
        self.verification_QuixBugs.junitEnvironment_Run_Initialize()
        self.verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
        data = self.jsonFileIO.readJsonLineData(self.verification_QuixBugs.getTestData())
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
                'type': self.verification_QuixBugs.checkBuggyMethodLine(buggyCode),
                'output': {}
            }

            for i in range(len(output)):

                patchFileName = '{}_TEST_{}'.format(buggyId, str(i))
                patchCode = output[str(i)]['output_patch']
                target = os.path.join(self.verification_QuixBugs.getJunitEnvironment(),
                                      'Module_{}/{}.java'.format(buggyId, patchFileName))
                targetModule = os.path.join(self.verification_QuixBugs.getJunitModuleTestEnvironment(), 'Module_{}/src/main/java/{}.java'.format(buggyId, patchFileName))

                LLM = self.verification_QuixBugs.getLLMModel()
                methodCode = LLM.patchReplaceByModel(buggyCode, patchCode)
                javaFormatLog, javaFormatResult = self.verification_QuixBugs.checkJavaFormat(methodCode, patchFileName, buggyId)
                compileLog, compileResult = self.verification_QuixBugs.checkJavaCompile(target, javaFormatResult)
                print(compileResult, compileLog)
                self.fileIO.copyFile(target, targetModule, compileResult)
                self.fileIO.moveFile(target, self.verification_QuixBugs.getRepairProgramPath(), compileResult)

                subdictionary['output'][i] = self.jsonFileIO.getJsonResultSubItem(patchCode, compileLog, compileResult, javaFormatLog, javaFormatResult, solution)

                if compileResult is True:
                    passNums += 1

            dictionary.append(subdictionary)

        print(dictionary)

        self.assertEqual(passNums, len(self.verification_QuixBugs.getAllRunTestCaseFileList()))
        self.jsonFileIO.writeJsonFile(dictionary, self.verification_QuixBugs.getJsonResultPath())
        self.assertTrue(os.path.exists(os.path.join(ROOT, self.verification_QuixBugs.getJsonResultPath(),)))

    def test_copy_promptRepairProgram_from_Junit_Environment(self):
        self.test_batchSize_load_junit_environment_create_json_framework()
        self.verification_QuixBugs.setPromptRepairProgramPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/promptRepairProgram')

        source = self.verification_QuixBugs.getJunitEnvironment()
        destination = self.verification_QuixBugs.getPromptRepairProgramPath()

        shutil.copytree(source, destination, dirs_exist_ok=True)

        self.assertTrue(os.path.exists(destination))
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(source)), len(self.fileIO.getFileListUnderFolder(destination)))

    def write_BITCOUNT_File(self, target, programFileName):
        javaCode = f"""
            import java.util.*;
            public class {programFileName} {{
                public static int bitcount(int n) {{
                int count = 0;
                while (n != 0) {{
                    n = (n & (n - 1));
                    count++;
                }}
                return count;
            }}
            }}
        """

        if self.fileIO.isPathExist(target):
            self.fileIO.deleteFileData(target)

        self.fileIO.writeFileData(target, javaCode)

    def write_MINIMUM_SPANNING_TREE_File(self, target, programFileName):
        javaCode = f"""
        import java.util.*;
        
        public class {programFileName} {{
          public static Set<WeightedEdge> minimum_spanning_tree(List<WeightedEdge> weightedEdges) {{
            Map<Node, Set<Node>> groupByNode = new HashMap<>();
            Set<WeightedEdge> minSpanningTree = new HashSet<>();
            Collections.sort(weightedEdges);
            for (WeightedEdge edge : weightedEdges) {{
              Node vertex_u = edge.node1;
              Node vertex_v = edge.node2;
        
              if (!groupByNode.containsKey(vertex_u)) {{
                groupByNode.put(vertex_u, new HashSet<>(Arrays.asList(vertex_u)));
              }}
              if (!groupByNode.containsKey(vertex_v)) {{
                groupByNode.put(vertex_v, new HashSet<>(Arrays.asList(vertex_v)));
              }}
        
              if (groupByNode.get(vertex_u) != groupByNode.get(vertex_v)) {{
                minSpanningTree.add(edge);
                groupByNode = update(groupByNode, vertex_u, vertex_v);
                for (Node node : groupByNode.get(vertex_v)) {{
                  groupByNode = update(groupByNode, vertex_u, node);
                }}
              }}
            }}
            return minSpanningTree;
          }}
        
          public static Map<Node, Set<Node>> update(
              Map<Node, Set<Node>> groupByNode, Node vertex_u, Node vertex_v) {{
            Set<Node> vertex_u_span = groupByNode.get(vertex_u);
            vertex_u_span.addAll(groupByNode.get(vertex_v));
            return groupByNode;
          }}
        }}

        """
        if self.fileIO.isPathExist(target):
            self.fileIO.deleteFileData(target)

        self.fileIO.writeFileData(target, javaCode)

    def test_run_test_case_script_expect_failure(self):
        # make sure the program can run test case
        self.verification_QuixBugs.setLogFolderPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/Log')

        LogFolder = self.verification_QuixBugs.getLogFolderPath()

        testModuleName = 'Module_BITCOUNT'
        programFileName = 'BITCOUNT_TEST_0'
        target = os.path.join(ROOT,
                'JUnit_ModuleTest/RunTestCase_QuixBugs/Module_BITCOUNT/src/main/java/{}.java'.format(programFileName))

        self.write_BITCOUNT_File(target, programFileName)
        self.assertTrue(os.path.exists(target))

        junitModuleEnvironment = self.verification_QuixBugs.getJunitModuleTestEnvironment()

        params = [testModuleName, programFileName, LogFolder, GRADLE_PATH, junitModuleEnvironment]

        self.verification_QuixBugs.runBashScript(params)
        target = os.path.join(LogFolder,'{}.txt'.format(programFileName))
        self.assertTrue(os.path.exists(target))

        logContent = self.fileIO.readFileData(target)
        self.assertTrue('BUILD FAILED' in logContent)

    def test_run_test_case_batchSize_get_dictionary(self):
        self.setUp2()
        self.verification_QuixBugs.createJsonFramework(['BREADTH_FIRST_SEARCH','FLATTEN','LONGEST_COMMON_SUBSEQUENCE'])
        """
        【Movement】 move file from junit_environment_pass folder to junit_module_environment and ready to run testcase
        【Replace】if file name is ADD_TEST_1, then all 'ADD' will be replaced with 'ADD_TEST_1' in the testcase file
        【Recovery】when all test case end, then all 'ADD_TEST_1' will be replaced with 'ADD' in the testcase file
        """
        runFileList = self.verification_QuixBugs.getAllRunTestCaseFileList()
        pass_file_module_dic = self.verification_QuixBugs.getFileAndModuleDict(runFileList)

        failureFileList = self.fileIO.getFileListUnderFolder(self.verification_QuixBugs.getJunitEnvironment())
        failure_file_module_dic = self.verification_QuixBugs.getFileAndModuleDict(failureFileList)

        print(pass_file_module_dic)
        print(failure_file_module_dic)

        total_item = len(set(pass_file_module_dic.values()) or set(failure_file_module_dic.values()))
        total_program = len(pass_file_module_dic.keys()) + len(failure_file_module_dic.keys())

        self.assertEqual(total_item * 5, total_program)

    def test_run_script_starter(self):
        self.verification_QuixBugs.junitEnvironment_Initialize()
        self.verification_QuixBugs.junitEnvironment_Run_Initialize()
        self.verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
        time.sleep(1)

        self.verification_QuixBugs.setLogFolderPath(
            'Result_Output/QuixBugs/Qwen/BeamSearch/Demo/Log')


        programFileName = 'MINIMUM_SPANNING_TREE_TEST_1'
        target = os.path.join(ROOT,
                              'JUnit_ModuleTest/RunTestCase_QuixBugs/Module_MINIMUM_SPANNING_TREE/src/main/java/{}.java'.format(
                                  programFileName))
        self.write_MINIMUM_SPANNING_TREE_File(target, programFileName)
        self.assertTrue(os.path.exists(target))

        runFileList = self.verification_QuixBugs.getAllRunTestCaseFileList()

        pass_file_module_dic = self.verification_QuixBugs.getFileAndModuleDict(runFileList)

        for item in pass_file_module_dic.items():
            newName = item[0] + '.'                     # ADD_TEST_9.
            oldName = item[1] + '.'                     # ADD.
            moduleName = 'Module_{}'.format(item[1])
            testFilePath = os.path.join(
                self.verification_QuixBugs.getJunitModuleTestEnvironment(),
                "{}/src/test/java/{}_TEST.java".format(moduleName, item[1])
            )
            self.fileIO.replaceName(testFilePath, oldName, newName)
            self.verification_QuixBugs.runScriptSingleFile(item[0], moduleName)
            self.fileIO.replaceName(testFilePath, newName, oldName)


        self.assertTrue(os.path.exists(os.path.join(self.verification_QuixBugs.getLogFolderPath(), 'MINIMUM_SPANNING_TREE_TEST_1.txt')))

    def test_check_buggy_method_buggy_Line(self):
        buggyMethod = """
        public static int add(int x, int y){
            // buggy code
            // return x*y
            return x + y;
        }
        """
        self.assertEqual(self.verification_QuixBugs.checkBuggyMethodLine(buggyMethod), 'Single')

    def test_and_run(self):
        self.setUp2()
        self.verification_QuixBugs.junitEnvironment_Initialize()
        self.verification_QuixBugs.junitEnvironment_Run_Initialize()
        self.verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
        self.verification_QuixBugs.createJsonFramework(['BREADTH_FIRST_SEARCH','FLATTEN','LONGEST_COMMON_SUBSEQUENCE'])
        self.verification_QuixBugs.createPromptRepairProgramSet()
        runFileList = self.verification_QuixBugs.getAllRunTestCaseFileList()
        dictionary = self.verification_QuixBugs.getFileAndModuleDict(runFileList)
        self.verification_QuixBugs.runScriptBatchFile(dictionary)
        self.verification_QuixBugs.updateJsonResult()
        self.assertTrue(len(dictionary),
                        len(self.fileIO.getFileListUnderFolder(self.verification_QuixBugs.getLogFolderPath())))


if __name__ == '__main__':
    unittest.main()


