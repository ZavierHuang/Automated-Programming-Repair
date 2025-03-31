import json
import os

from Util_Module.src.FileIO import FileIO


class JsonFileIO(FileIO):
    def __init__(self):
        super().__init__()

    def readJsonLineData(self, jsonLineFilePath):
        if self.isPathExist(jsonLineFilePath):
            with open(jsonLineFilePath, 'r', encoding='utf-8') as jsonFile:
                data = [json.loads(line) for line in jsonFile if line.strip()]
            return data
        return None

    def getJsonResultSubItem(self, patchCode, compileLog, compileResult, javaFormatLog, javaFormatResult, solution):
        subItem = {
            'patchCode': patchCode,
            'exactlyMatch': self.normalize(patchCode) == self.normalize(solution),
            'formatCheck':{
                'formatResult': javaFormatResult,
                'javaFormatLog': javaFormatLog
            },
            'compileCheck':{
                'compileResult': compileResult,
                'compileLog': compileLog
            },
            'RunTestCase':False
        }
        return subItem

    def writeJsonFile(self, dictionary, writeJsonFilePath):
        try:
            os.makedirs(os.path.dirname(writeJsonFilePath), exist_ok=True)
            with open(writeJsonFilePath, 'w', encoding='utf-8') as jsonFile:
                json.dump(dictionary, jsonFile, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to write {writeJsonFilePath}: {e}")
            raise

