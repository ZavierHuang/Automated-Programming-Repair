import subprocess
from Config import *
from Util_Module.src.FileIO import FileIO


class Verification:
    def __init__(self):
        self.googleJavaFormat = None
        self.fileIO = FileIO()

    def setGoogleJavaFormat(self, googleJavaFormat):
        self.googleJavaFormat = ROOT + googleJavaFormat

    def setRemainderCodePath(self, remainCodePath):
        self.remainCodePath = ROOT + remainCodePath

    def setJunitEnvironment(self, junit_environment):
        self.junitEnvironment = ROOT + junit_environment

    def getGoogleJavaFormat(self):
        return self.googleJavaFormat

    def getRemainderCodePath(self):
        return self.remainCodePath

    def getJunitEnvironment(self):
        return self.junitEnvironment


    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        pass

    def subprocess_run_JavaFormat(self, filePath):
        result = subprocess.run(
            ["java", "-jar", JAVA_FORMAT_PATH , "--replace", filePath],
            capture_output=True,
            text=True
        )
        return result

    def createJavaValidCode(self, patchFileName, methodCode, remainderCode):
        javaCode = f"""
        public class {patchFileName} {{
            {methodCode}
            {remainderCode}
        }}
        """
        return javaCode

    def readReaminderCode(self, remainderCodePath):
        readData = ''

        if self.fileIO.isFileExist(remainderCodePath):
            readData = self.fileIO.readFileData(remainderCodePath)

        return readData