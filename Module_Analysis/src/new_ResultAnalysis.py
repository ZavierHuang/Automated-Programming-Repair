import os
from Config import ROOT
from Module_Util.src.JsonFileIO import JsonFileIO


class NewResultAnalysis:
    def __init__(self):
        self.jsonFileIO = JsonFileIO()


    def resultAnalysis(self, jsonFilePath):
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, jsonFilePath))

        single = 0
        multiple = 0
        repairSuccess = 0
        repairFailure = 0
        formatError = 0
        compileError = 0
        exactlyMatch = 0
        passTestCase = 0
        failTestCase = 0
        runTestCase = 0

        exactlyMatchList = []

        for item in data:
            if item['repair']:
                if item['type'] == 'Single':    single += 1
                if item['type'] == 'Multiple':  multiple += 1
                repairSuccess += 1
            else:
                repairFailure += 1

            output = item['output']

            for i in range(len(output)):
                if output[str(i)]['exactlyMatch'] == True:
                    exactlyMatch += 1
                    if item['buggyId'] not in exactlyMatchList:
                        exactlyMatchList.append(item['buggyId'])
                if output[str(i)]['formatCheck']['formatResult'] == False:  formatError += 1
                if output[str(i)]['compileCheck']['compileResult'] == False and output[str(i)]['compileCheck'][
                    'compileLog'] != 'FormatError': compileError += 1
                if output[str(i)]['compileCheck']['compileResult'] == True:
                    runTestCase += 1
                    if output[str(i)]['PassTestCase'] == True:
                        passTestCase += 1
                    else:
                        failTestCase += 1

        print('repairSuccess:', repairSuccess)
        print('single:', single)
        print('multiple:', multiple)
        print('exactlyMatchList:', len(exactlyMatchList))
        print('repairFaiulre:', repairFailure)
        print('================================================')
        print('formatError:', formatError)
        print('compileError:', compileError)
        print('runTestCase:', runTestCase)
        print('--failTestCase:', failTestCase)
        print('--passTestCase:', passTestCase)
        print('--exactly Match:', exactlyMatch)