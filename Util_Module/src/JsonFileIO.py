import json

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

