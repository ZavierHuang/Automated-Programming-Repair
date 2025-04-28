import os.path
import re
import shutil
import subprocess
import sys

from Config import *
from Module_Util.src.FileIO import FileIO
from Module_Util.src.JsonFileIO import JsonFileIO


class Verification:
    def __init__(self):
        self.DataSetName = None
        self.junitEnvironment = None
        self.remainCodePath = None
        self.junitModuleTestEnvironment = None
        self.testDataResult = None
        self.scriptPath = None

        self.jsonResultPath = None
        self.logFolderPath = None
        self.repairProgramPath = None
        self.promptRepairProgramPath = None

        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()
        self.LLM = None

    def setDataSetName(self, DataSetName):
        self.DataSetName = DataSetName

    def setLLMModel(self, LLModel):
        self.LLM = LLModel

    def setRepairProgramPath(self, repairProgramPath):
        self.repairProgramPath = os.path.join(ROOT, repairProgramPath)
        os.makedirs(self.repairProgramPath, exist_ok=True)

    def setPromptRepairProgramPath(self, promptRepairProgramPath):
        self.promptRepairProgramPath = os.path.join(ROOT, promptRepairProgramPath)
        os.makedirs(self.promptRepairProgramPath, exist_ok=True)

    def setLogFolderPath(self, logFolderPath):
        self.logFolderPath = os.path.join(ROOT, logFolderPath)
        os.makedirs(self.logFolderPath, exist_ok=True)

    def setJsonResultPath(self, jsonResultPath):
        self.jsonResultPath = os.path.join(ROOT, jsonResultPath)
        os.makedirs(os.path.dirname(self.jsonResultPath), exist_ok=True)

    def setScriptPath(self, scriptPath):
        self.scriptPath = os.path.join(ROOT, scriptPath)

    def setTestDataResult(self, testDataResult):
        self.testDataResult = os.path.join(ROOT, testDataResult)

    def setJunitModuleTestEnvironment(self, junitModuleTestEnvironment):
        self.junitModuleTestEnvironment = os.path.join(ROOT, junitModuleTestEnvironment)

    def setRemainderCodePath(self, remainCodePath):
        self.remainCodePath = os.path.join(ROOT, remainCodePath) if remainCodePath is not None else None

    def setJunitEnvironment(self, junit_environment):
        self.junitEnvironment = os.path.join(ROOT, junit_environment)

    def getDataSetName(self):
        return self.DataSetName

    def getLLMModel(self):
        return self.LLM

    def getLogFolderPath(self):
        return self.logFolderPath

    def getJsonResultPath(self):
        return self.jsonResultPath

    def getScriptPath(self):
        return self.scriptPath

    def getTestData(self):
        return self.testDataResult

    def getJunitModuleTestEnvironment(self):
        return self.junitModuleTestEnvironment

    def getRemainderCodePath(self):
        return self.remainCodePath

    def getJunitEnvironment(self):
        return self.junitEnvironment

    def getRepairProgramPath(self):
        return self.repairProgramPath

    def getPromptRepairProgramPath(self):
        return self.promptRepairProgramPath

    def subprocess_run_JavaFormat(self, filePath):
        result = subprocess.run(
            ["java", "-jar", JAVA_FORMAT_PATH , "--replace", filePath],
            capture_output=True,
            text=True
        )
        return result

    def subprocess_run_JavaCompile(self, javaFiles):
        result = subprocess.run(
            ['javac', '-d', CACHE_PATH] + javaFiles,
            capture_output=True,
            text=True
        )
        return result

    def createJavaValidCode(self, patchFileName, methodCode, remainderCode, importContent):
        javaCode = f"""
        {importContent}
        public class {patchFileName} {{
            {methodCode}
            {remainderCode}
        }}
        """
        return javaCode

    def readRemainderCode(self, remainderCodePath):
        readData = ''

        if remainderCodePath is not None and self.fileIO.isPathExist(remainderCodePath):
            readData = self.fileIO.readFileData(remainderCodePath)

        return readData

    def junitEnvironment_Clear(self, folderPath):
        subFolderList = self.fileIO.getSubFolderList(folderPath)
        return self.fileIO.deleteSubFolderAndCreate(folderPath, subFolderList)

    def junitEnvironment_Initialize(self):
        self.junitEnvironment_Clear(self.getJunitEnvironment())

    def junitEnvironment_Run_Initialize(self):
        sub_Module_Folder_List = self.fileIO.getRunTestCaseModuleFolderList(self.getJunitModuleTestEnvironment())
        for subModuleFolderPath in sub_Module_Folder_List:
            self.fileIO.deleteJavaFileUnderFolder(os.path.join(subModuleFolderPath, 'src/main/java'))

    def juniEnvironment_TEST_File_Initialize(self):
        sub_Module_Folder_List = self.fileIO.getRunTestCaseModuleFolderList(self.getJunitModuleTestEnvironment())
        for subModuleFolderPath in sub_Module_Folder_List:
            test_targetPath = os.path.join(subModuleFolderPath, 'src/test/java')
            fileList = self.fileIO.getFileListUnderFolder(test_targetPath)
            for file in fileList:
                filePath = os.path.join(test_targetPath, file)
                data = self.fileIO.readFileData(filePath)
                result = re.sub(r'_TEST_\d+', '', data)
                result = re.sub(r'_TEST\.', '', result)
                self.fileIO.writeFileData(filePath, result)

                # print(file)
                data = self.fileIO.readFileData(filePath)
                if '_TEST_' in data:
                    print(file,'Test File Initialize Terminated')
                    sys.exit(1)

    def getImportContent(self, buggyId):
        pass

    def getNeedCompileJavaFiles(self, javaFile):
        pass

    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        pass

    def checkJavaCompile(self, javaFile, javaFormatResult):
        pass

    def runBashScript(self, params):
        currentPath = os.getcwd()
        os.chdir(self.getJunitModuleTestEnvironment())
        command = [BASH_PATH, self.getScriptPath()] + params

        print(command)
        try:
            subprocess.run(command, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print("Error executing script:")
            print(e.stderr)
        finally:
            os.chdir(currentPath)

    def getAllRunTestCaseFileList(self):
        fileList = self.fileIO.getFileListUnderFolder(self.getJunitModuleTestEnvironment())
        return [file[:file.find('.java')] for file in fileList if file.endswith('.java') and '_TEST_' in file]

    def getFileAndModuleDict(self, fileList):
        """
        (key, value) = (patchFileName, moduleName)
        dictionary = {
            "ADD_TEST_1" : "ADD",
            "ADD_TEST_2" : "ADD",
            "GCD_TEST_1" : "GCD",
        }
        """

        dictionary = {}
        for file in fileList:
            dictionary[file] = file[:file.find('_TEST_')]

        return dictionary

    def createJsonFramework(self, exceptList):
        QuixBugsSolution = self.jsonFileIO.readJsonData(os.path.join(ROOT,'Data_Storage/QuixBugs/Solution/QuixBugsSolution.json'))
        data = self.jsonFileIO.readJsonLineData(self.getTestData())
        print(self.getTestData(),self.fileIO.isPathExist(self.getTestData()))
        dictionary = []

        for item in data:
            buggyId = item['bug_id']
            if buggyId in exceptList:
                continue

            buggyCode = item['buggy_code']
            output = item['output']

            if self.DataSetName == 'QuixBugs':
                solution = QuixBugsSolution[buggyId]
            else:
                solution = item['gold_patch']

            subdictionary = {
                'buggyId': buggyId,
                'repair': False,
                'solution': solution,
                'type': self.checkBuggyMethodLine(buggyCode),
                'output': {}
            }
            for i in range(len(output)):
                patchFileName = '{}_TEST_{}'.format(buggyId, str(i))
                patchCode = output[str(i)]['output_patch']
                target = os.path.join(self.getJunitEnvironment(),
                                      'Module_{}/{}.java'.format(buggyId, patchFileName))
                targetModule = os.path.join(self.getJunitModuleTestEnvironment(),
                                            'Module_{}/src/main/java/{}.java'.format(buggyId, patchFileName))

                methodCode = self.getLLMModel().patchReplaceByModel(buggyCode, patchCode)

                javaFormatLog, javaFormatResult = self.checkJavaFormat(methodCode, patchFileName, buggyId)
                compileLog, compileResult = self.checkJavaCompile(target, javaFormatResult)

                if self.DataSetName == 'QuixBugs':
                    data = self.fileIO.readFileData(target)
                    for item in ['Node', 'WeightedEdge', 'QuixFixOracleHelper']:
                        if item in data:
                            data = 'import dataStructures.*;\n' + data
                            self.fileIO.writeFileData(target, data)
                            break

                print(patchFileName, compileResult, compileLog)

                self.fileIO.copyFile(target, targetModule, compileResult)
                self.fileIO.moveFile(target, self.getRepairProgramPath(), self.getPromptRepairProgramPath(), compileResult)

                subdictionary['output'][i] = (
                    self.jsonFileIO.getJsonResultSubItem(
                        patchCode, compileLog, compileResult,
                        javaFormatLog, javaFormatResult, solution))

            dictionary.append(subdictionary)

        self.jsonFileIO.writeJsonFile(dictionary, self.getJsonResultPath())

    def runScriptSingleFile(self, patchFileName, moduleName):
        # params = [testModuleName, programFileName, logFolder, gradlePath, junitModuleEnvironment]

        # patchFileName = ADD_ELEMENTS_TEST_4
        # moduleName = Module_ADD_ELEMENTS

        print('run ', patchFileName)

        params = [
            moduleName,
            patchFileName,
            self.getLogFolderPath(),
            GRADLE_PATH,
            self.getJunitModuleTestEnvironment()
        ]
        self.runBashScript(params)

    def runScriptBatchFile(self, directory):
        for item in directory.items():
            newName = item[0] + '.'  # ADD_TEST_9.
            oldName = item[1] + '.'  # ADD.
            moduleName = 'Module_{}'.format(item[1])
            testFilePath = os.path.join(
                self.getJunitModuleTestEnvironment(),
                "{}/src/test/java/{}_TEST.java".format(moduleName, item[1])
            )
            if item[1] == 'GET_ROW':
                self.fileIO.replaceName(testFilePath, item[1] + '()', item[0] + '()')   # GET_ROW() --> GET_ROW_TEST_1()

            self.fileIO.replaceName(testFilePath, oldName, newName)
            self.runScriptSingleFile(item[0], moduleName)
            self.fileIO.replaceName(testFilePath, newName, oldName)

            if item[1] == 'GET_ROW':
                self.fileIO.replaceName(testFilePath, item[0] + '()', item[1] + '()')   # GET_ROW_TEST_1() --> GET_ROW()


    def checkBuggyMethodLine(self, buggyMethod):
        buggyMethod = buggyMethod[buggyMethod.find('buggy code'):]
        commentLineNums = buggyMethod.count('//')

        if commentLineNums > 1:
            return 'Multiple'

        return 'Single'


    def updateJsonResult(self):
        pass