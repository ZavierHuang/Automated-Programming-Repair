import os.path
import subprocess
from Config import *
from Src_Module.src.LLM_CodeLlama import LLM_CodeLlama
from Util_Module.src.FileIO import FileIO
from Util_Module.src.JsonFileIO import JsonFileIO


class Verification:
    def __init__(self):
        self.junitEnvironment = None
        self.remainCodePath = None
        self.googleJavaFormat = None
        self.junitModuleTestEnvironment = None
        self.testDataResult = None
        self.scriptPath = None
        self.jsonResultPath = None
        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()
        self.model_CodeLlama = LLM_CodeLlama()

    def setJsonResultPath(self, jsonResultPath):
        self.jsonResultPath = os.path.join(ROOT, jsonResultPath)

    def setScriptPath(self, scriptPath):
        self.scriptPath = os.path.join(ROOT, scriptPath)

    def setTestDataResult(self, testDataResult):
        self.testDataResult = os.path.join(ROOT, testDataResult)

    def setJunitModuleTestEnvironment(self, junitModuleTestEnvironment):
        self.junitModuleTestEnvironment = os.path.join(ROOT, junitModuleTestEnvironment)

    def setGoogleJavaFormat(self, googleJavaFormat):
        self.googleJavaFormat = os.path.join(ROOT, googleJavaFormat)

    def setRemainderCodePath(self, remainCodePath):
        self.remainCodePath = os.path.join(ROOT, remainCodePath)

    def setJunitEnvironment(self, junit_environment):
        self.junitEnvironment = os.path.join(ROOT, junit_environment)

    def getJsonResultPath(self):
        return self.jsonResultPath

    def getScriptPath(self):
        return self.scriptPath

    def getTestData(self):
        return self.testDataResult

    def getJunitModuleTestEnvironment(self):
        return self.junitModuleTestEnvironment

    def getGoogleJavaFormat(self):
        return self.googleJavaFormat

    def getRemainderCodePath(self):
        return self.remainCodePath

    def getJunitEnvironment(self):
        return self.junitEnvironment

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

        if self.fileIO.isPathExist(remainderCodePath):
            readData = self.fileIO.readFileData(remainderCodePath)

        return readData

    def junitEnvironment_Clear(self, folderPath):
        subFolderList = self.fileIO.getSubFolderList(folderPath)
        return self.fileIO.deleteSubFolderAndCreate(folderPath, subFolderList)

    def junitEnvironment_Initialize(self):
        self.junitEnvironment_Clear(self.getJunitEnvironment())

    def junitEnvironment_Run_Initialize(self):
        self.junitEnvironment_Module_Test_Clear()

    def junitEnvironment_Module_Test_Clear(self):
        sub_Module_Folder_List = self.fileIO.getRunTestCaseModuleFolderList(self.getJunitModuleTestEnvironment())
        for subModuleFolderPath in sub_Module_Folder_List:
            self.fileIO.deleteSubFolderAndCreate(subModuleFolderPath,
                                                 [os.path.join(subModuleFolderPath, 'src/main/java')])

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
        try:
            subprocess.run(command, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print("Error executing script:")
            print(e.stderr)
        finally:
            os.chdir(currentPath)

    def getAllRunTestCaseFileList(self):
        fileList = self.fileIO.getFileListUnderFolder(self.getJunitModuleTestEnvironment())
        return [file for file in fileList if file.endswith('.java') and '_TEST_' in file]

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


    def createJsonFramework(self):
        pass

