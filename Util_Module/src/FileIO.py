import os
import json

class FileIO:
    def __init__(self):
        pass

    def isFileExist(self, filePath):
        return os.path.exists(filePath)

    def readJsonLineData(self, jsonLineFilePath):
        if self.isFileExist(jsonLineFilePath):
            with open(jsonLineFilePath, 'r', encoding='utf-8') as jsonFile:
                data = [json.loads(line) for line in jsonFile if line.strip()]
            return data
        return None

    def writeFileData(self, writeFilePath, writeContent):
        try:
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
        if self.isFileExist(deleteFilePath):
            os.remove(deleteFilePath)
        else:
            raise Exception("File doesn't exist")