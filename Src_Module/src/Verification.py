import subprocess
from Config import *
from Util_Module.src.FileIO import FileIO


class Verification:
    def __init__(self):
        self.googleJavaFormat = 'Tool/google-java-format-1.18.1-all-deps'
        self.fileIO = FileIO()


    def subprocess_run_JavaFormat(self, filePath):
        result = subprocess.run(
            ["java", "-jar", JAVA_FORMAT_PATH , "--replace", filePath],
            capture_output=True,
            text=True
        )
        return result

    def addClassOutSide(self, patchFileName, methodCode, remainderCode):
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

    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        pass
