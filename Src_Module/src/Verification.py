import subprocess
from Config import *
from Util_Module.src.FileIO import FileIO


class Verification:
    def __init__(self):
        self.junitEnvironment = None
        self.junitEnvironment_Pass = None
        self.junitEnvironment_Failure = None
        self.remainCodePath = None
        self.googleJavaFormat = None
        self.junitModuleTestEnvironment = None
        self.fileIO = FileIO()

    def setJunitModuleTestEnvironment(self, junitModuleTestEnvironment):
        self.junitModuleTestEnvironment = os.path.join(ROOT, junitModuleTestEnvironment)

    def setGoogleJavaFormat(self, googleJavaFormat):
        self.googleJavaFormat = os.path.join(ROOT, googleJavaFormat)

    def setRemainderCodePath(self, remainCodePath):
        self.remainCodePath = os.path.join(ROOT, remainCodePath)

    def setJunitEnvironment(self, junit_environment):
        self.junitEnvironment = os.path.join(ROOT, junit_environment)
        self.junitEnvironment_Pass = os.path.join(self.getJunitEnvironment(), 'JUnit_Environment_Pass')
        self.junitEnvironment_Failure = os.path.join(self.getJunitEnvironment(), 'JUnit_Environment_Failure')

    def getJunitModuleTestEnvironment(self):
        return self.junitModuleTestEnvironment

    def getGoogleJavaFormat(self):
        return self.googleJavaFormat

    def getRemainderCodePath(self):
        return self.remainCodePath

    def getJunitEnvironment(self):
        return self.junitEnvironment

    def getJunitEnvironmentPass(self):
        return self.junitEnvironment_Pass

    def getJunitEnvironmentFailure(self):
        return self.junitEnvironment_Failure

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
        self.junitEnvironment_Clear(self.getJunitEnvironmentPass())
        self.junitEnvironment_Clear(self.getJunitEnvironmentFailure())

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

    def checkJavaCompile(self, javaFile):
        pass

