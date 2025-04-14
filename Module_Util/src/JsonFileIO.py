import json
import os

from Module_Util.src.FileIO import FileIO


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
            'exactlyMatch': self.compareEqual(patchCode, solution),
            'formatCheck':{
                'formatResult': javaFormatResult,
                'javaFormatLog': javaFormatLog
            },
            'compileCheck':{
                'compileResult': compileResult,
                'compileLog': compileLog
            },
            'PassTestCase':False
        }
        return subItem

    def writeJsonFile(self, data, writeJsonFilePath):
        try:
            os.makedirs(os.path.dirname(writeJsonFilePath), exist_ok=True)
            with open(writeJsonFilePath, 'w', encoding='utf-8') as jsonFile:
                json.dump(data, jsonFile, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to write {writeJsonFilePath}: {e}")
            raise

    def writeJsonLineFile(self, data, writeJsonLineFilePath):
        try:
            with open(writeJsonLineFilePath, "w", encoding="utf-8") as f:
                for item in data:
                    json_line = json.dumps(item)
                    f.write(json_line + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to write {writeJsonLineFilePath}: {e}")
            raise

    def readJsonData(self, jsonFilePath):
        with open(jsonFilePath, 'r', encoding='utf-8') as jsonFile:
            data = json.load(jsonFile)
        return data