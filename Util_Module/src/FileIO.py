import os
import shutil


class FileIO:
    def __init__(self):
        pass

    def isPathExist(self, filePath):
        return os.path.exists(filePath)

    def writeFileData(self, writeFilePath, writeContent):
        try:
            os.makedirs(os.path.dirname(writeFilePath), exist_ok=True)
            with open(writeFilePath, 'w', encoding='utf-8') as writeFile:
                writeFile.write(writeContent)
        except Exception as e:
            print(f"[ERROR] Failed to write {writeFilePath}: {e}")
            raise

    def readFileData(self, readFilePath):
        try:
            with open(readFilePath, 'r', encoding='utf-8') as readFile:
                readFileContent = readFile.read()
                return readFileContent
        except Exception as e:
            print(f"[ERROR] Failed to read {readFilePath}: {e}")
            raise Exception

    def deleteFileData(self, deleteFilePath):
        if self.isPathExist(deleteFilePath):
            os.remove(deleteFilePath)
        else:
            raise Exception("File doesn't exist")

    def getFileListUnderFolder(self, folderPath):
        fileList = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                fileList.append(file)
        return fileList

    def getSubFolderList(self, folderPath):
        subFolderList = []
        for root, dirs, files in os.walk(folderPath):
            for subFolder in dirs:
                subFolderList.append(os.path.join(folderPath, subFolder))

        return subFolderList

    def deleteSubFolderAndCreate(self, rootPath, subFolderList):
        for subFolder in subFolderList:
            shutil.rmtree(subFolder)
            os.mkdir(subFolder)

        return len(self.getFileListUnderFolder(rootPath)) == 0

    def getRunTestCaseModuleFolderList(self, junitModuleTestEnvironment):
        subFolderList = self.getSubFolderList(junitModuleTestEnvironment)
        return [subFolder for subFolder in subFolderList if 'Module_' in subFolder]

    def moveFile(self,source, destination, compileResult):
        if compileResult:
            shutil.move(source, destination)