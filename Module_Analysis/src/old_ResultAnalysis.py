from Module_Util.src.JsonFileIO import JsonFileIO


class OldResultAnalysis:
    def __init__(self):
        self.jsonFileIO = JsonFileIO()
        self.report = None

    def setLLM(self, LLM):
        self.LLM = LLM

    def setLora(self, Lora):
        self.Lora = Lora

    def setTotalProgram(self, totalProgram):
        self.totalProgram = totalProgram

    def getLLM(self):
        return self.LLM

    def getLora(self):
        return self.Lora

    def getReport(self):
        return self.report

    def createReportFormat(self):
        result = {
            self.LLM: {
                'Total Program': self.totalProgram,
                'Repair Successfully': 0,
                'Single Line': 0,
                'Multiple Line': 0,
                'Exactly Match': 0,
                'Repair Failure': 0,
            },
            'Total': {
                'Total Patch': self.totalProgram*10,
                'Format Error': 0,
                'Compile Error': 0,
                'Run Test Case': 0,
                'Fail Test Case': 0,
                'Pass Test Case': 0,
                'Exactly Match': 0,
            }
        }
        return result

    def updateProgramAnalysisData(self, jsonData):
        for item in jsonData:
            if item['repair'] == 'Success':
                self.report[self.LLM]['Repair Successfully'] += 1
                if item['Type'] == 'Single':
                    self.report[self.LLM]['Single Line'] += 1
                else:
                    self.report[self.LLM]['Multiple Line'] += 1

                output = item['output']
                for i in range(len(output)):
                    if output[str(i)]['exactlyMatch'] == True:
                        self.report[self.LLM]['Exactly Match'] += 1
                        break
            else:
                self.report[self.LLM]['Repair Failure'] += 1

    def updateTotalPatchAnalysisData(self, jsonData):
        for item in jsonData:
            output = item['output']
            for i in range(len(output)):
                if output[str(i)]['exactlyMatch'] == True:
                    self.report['Total']['Exactly Match'] += 1

                if output[str(i)]['CompileCheck'] == 'Success':
                    self.report['Total']['Run Test Case'] += 1
                    if output[str(i)]['RunTestCase_QuixBugs'] == "PASS":
                        self.report['Total']['Pass Test Case'] += 1
                    else:
                        self.report['Total']['Fail Test Case'] += 1

    def updateFormatCompileAnalysisData(self, data):
        for item in data:
            output = item['output']
            for i in range(len(output)):
                if output[str(i)]['FormatResult'] == 'FAILURE':
                    self.report['Total']['Format Error'] += 1
                else:
                    if output[str(i)]['CompileResult'] == 'FAILURE':
                        self.report['Total']['Compile Error'] += 1



    def resultAnalysis(self, resultFile, mechanismFile):
        resultData = self.jsonFileIO.readJsonData(resultFile)
        mechanismData = self.jsonFileIO.readJsonData(mechanismFile)
        self.report = self.createReportFormat()
        self.updateProgramAnalysisData(resultData)
        self.updateTotalPatchAnalysisData(resultData)
        self.updateFormatCompileAnalysisData(mechanismData)
        self.printResult()


    def printResult(self):
        print(self.LLM, self.Lora)
        for item in self.report:
            for subItem in self.report[item].items():
                print(subItem)
            print("===============================")










