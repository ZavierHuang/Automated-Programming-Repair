from Module_Util.src.JsonFileIO import JsonFileIO


class ResultAnalysis:
    def __init__(self):
        self.jsonFileIO = JsonFileIO()

    def createReportFormat(self,totalProgram):
        result = {
            'HumanEval': {
                'Total Program': totalProgram,
                'Repair Successfully': 0,
                'Exactly Match': 0,
                'Single Line': 0,
                'Multiple Line': 0,
                'Repair Failure': 0,
            },
            'Total': {
                'Total Patch': totalProgram*10,
                'Format Error:': 0,
                'Compile Error:': 0,
                'Run Test Case': 0,
                'Fail Test Case': 0,
                'Pass Test Case': 0,
                'Exactly Match': 0,
            }
        }
        return result

    def getAllAnalysisData(self, jsonData):
        result = {
            'repair success':
        }

        for item in jsonData:
            if item['repair'] == 'Success':


    def oldResultAnalysis(self, para):
        jsonFile = para[0]
        LLM = para[1]
        lora = para[2]
        dataSet = para[3]
        totalProgram = para[4]
        data = self.jsonFileIO.readJsonLineData(jsonFile)
        report = self.createReportFormat(totalProgram)

        result = self.getAllAnalysisData(data)








