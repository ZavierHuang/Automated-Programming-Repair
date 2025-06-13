import os
import re
from unittest.mock import patch

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

    def passCaseGrowthTendency(self, jsonFilePath):
        dictionary = {i : 0 for i in range(10)}
        growthTendency = {i : 0 for i in range(10)}
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, jsonFilePath))

        for item in data:
            if item['repair']:
                output = item['output']
                for i in range(len(output)):
                    if output[str(i)]['PassTestCase']:
                        dictionary[i] += 1
                        break

        for i in range(len(dictionary)):
            if i == 0:
                growthTendency[i] = dictionary[i]
            else:
                growthTendency[i] = growthTendency[i-1] + dictionary[i]

        print(growthTendency)


    def passButNotExactlyMatch(self, jsonFilePath):
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, jsonFilePath))
        resultDict = {}

        for item in data:
            counter = 0
            subList = []
            output = item['output']
            if item['repair']:
                for i in range(len(output)):
                    if output[str(i)]['PassTestCase'] == True:
                        if output[str(i)]['exactlyMatch'] == True:
                            counter += 1
                        else:
                            subList.append(i)

                if counter == 0:
                    resultDict[item['buggyId']] = subList


        for key, value in resultDict.items():
            print(key, value)

        print(len(resultDict))

        self.getDetailPatchCode(resultDict, data)

    def getDetailPatchCode(self, resultDict, data):
        for item in data:
            if item['buggyId'] in resultDict:
                print(item['buggyId'], item['solution'])
                print("========================================")
                for i in range(len(item['output'])):
                    if i in resultDict[item['buggyId']]:
                        print(i,':',item['output'][str(i)]['patchCode'])

                print("===========================================================\n")

    def promptRepairAddSuccessCase(self, promptJsonFile, APRJsonFile):
        dataAPR = self.jsonFileIO.readJsonData(os.path.join(ROOT, APRJsonFile))
        promptAPR = self.jsonFileIO.readJsonData(os.path.join(ROOT, promptJsonFile))

        APR_FailureCase = []
        for item in dataAPR:
            if item['repair'] == False:
                APR_FailureCase.append(item['buggyId'])

        promptAPR_SuccessCase = []

        for item in promptAPR:
            if item['repair'] == True:
                if item['buggyId'] in APR_FailureCase:
                    promptAPR_SuccessCase.append(item['buggyId'])

        print("\nCase:", len(set(promptAPR_SuccessCase)))
        print("ID:", set(promptAPR_SuccessCase))

    def promptRepairErrorCase(self, promptJsonFile, APRJsonFile):
        dataAPR = self.jsonFileIO.readJsonData(os.path.join(ROOT, APRJsonFile))
        promptAPR = self.jsonFileIO.readJsonData(os.path.join(ROOT, promptJsonFile))

        formatErrorCase = []
        compileErrorCase = []

        failureFormatErrorCase = []
        failureCompileErrorCase = []

        for item in dataAPR:
            buggyId = item['buggyId']
            output = item['output']
            for i in range(len(output)):
                patchFileName = f'{buggyId}_TEST_{i}'
                if output[str(i)]['formatCheck']['formatResult'] == False:
                    formatErrorCase.append(patchFileName)
                else:
                    if output[str(i)]['compileCheck']['compileResult'] == False:
                        compileErrorCase.append(patchFileName)

        for item in promptAPR:
            buggyId = item['buggyId']
            output = item['output']
            repairSuccess = False
            for i in range(len(output)):
                if output[str(i)]['errorMessage'] == 'Compile Success':
                    repairSuccess = True
                    break

            if repairSuccess is False:
                if buggyId in formatErrorCase:
                    failureFormatErrorCase.append(buggyId)
                else:
                    failureCompileErrorCase.append(buggyId)


        print(len(formatErrorCase))
        print(len(compileErrorCase))

        print(len(failureFormatErrorCase))
        print(len(failureCompileErrorCase))

    def promptRepairFormatErrorCase(self, APRJsonFile):
        formatErrorCase = {}

        dataAPR = self.jsonFileIO.readJsonData(os.path.join(ROOT, APRJsonFile))
        for item in dataAPR:
            output = item['output']
            for i in range(len(output)):
                if output[str(i)]['formatCheck']['formatResult'] == False:
                    errors = re.findall(r"error: (.+)", output[str(i)]['formatCheck']['javaFormatLog'])

                    for e in errors:
                        if e not in formatErrorCase:
                            formatErrorCase[e] = 1
                        else:
                            formatErrorCase[e] += 1

        print(len(formatErrorCase))
        for key, value in formatErrorCase.items():
            print(key, value)

    def promptRepairFormatErrorCase_Repair_Tendency(self, promptJsonFile):
        promptAPR = self.jsonFileIO.readJsonData(os.path.join(ROOT, promptJsonFile))

        dict = {}

        for item in promptAPR:
            repairTimes = item['repairTimes']
            if repairTimes not in dict:
                dict[repairTimes] = 1
            else:
                dict[repairTimes] += 1

        for key, value in dict.items():
            print(key, value)

    def getEmptyPatchCode(self, jsonFile):
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, jsonFile))

        dictionary = {i:0 for i in range(10)}

        for item in data:
            output = item['output']
            for i in range(len(output)):
                if len(output[str(i)]['patchCode'].strip()) == 0:
                    dictionary[i] += 1

        total = sum(dictionary.values())
        for value in dictionary.values():
            print(value,end=' ')
        print('\n',total)

    def getErrorCase(self, jsonFile):
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, jsonFile))

        errorCase = {'formatError':0, 'compileError':0, 'NotPassTestCase':0}

        for item in data:
            buggyId = item['buggyId']
            solution = item['solution']
            output = item['output']

            print("buggyId:", buggyId)
            print("solution:", solution)
            print("===========================================================")
            for i in range(len(output)):
                if output[str(i)]['PassTestCase'] == False:
                    print("i:", i)
                    print(output[str(i)]['patchCode'])
                    if output[str(i)]['formatCheck']['formatResult'] == False:
                        print(output[str(i)]['formatCheck']['javaFormatLog'])
                        errorCase['formatError'] += 1

                    elif output[str(i)]['compileCheck']['compileResult'] == False:
                        if output[str(i)]['compileCheck']['compileLog'] != 'FormatError':
                            print(output[str(i)]['compileCheck']['compileLog'])
                            errorCase['compileError'] += 1
                    else:
                        print("Compile Pass")
                        errorCase['NotPassTestCase'] += 1
                    print("===========================================================")


        print("errorCase:", errorCase)

    def DBS_BS_RepairPart(self, BSJsonFile, DBSJsonFile):
        dataBS = self.jsonFileIO.readJsonData(os.path.join(ROOT, BSJsonFile))
        dataDBS = self.jsonFileIO.readJsonData(os.path.join(ROOT, DBSJsonFile))

        BSRepairList = []
        DBSRepairList = []

        for item in dataBS:
            if item['repair'] is True:
                BSRepairList.append(item['buggyId'])

        for item in dataDBS:
            if item['repair'] is True:
                DBSRepairList.append(item['buggyId'])


        BSRepairSet = set(BSRepairList)
        DBSRepairSet = set(DBSRepairList)

        print()
        print(len(DBSRepairSet - BSRepairSet), DBSRepairSet - BSRepairSet)
        print("===========================================================")
        print(len(BSRepairSet - DBSRepairSet), BSRepairSet - DBSRepairSet)
        print("===========================================================")
        print("Intersection:", len(BSRepairSet & DBSRepairSet))

    def getReport(self, jsonResultPath, beamSize):
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, jsonResultPath))

        item = data[0]

        print("===========================================================")
        if item['repair']:
            print(item['buggyId'],"Repair Success")
        else:
            print(item['buggyId'], "Repair Failure")

        resultDict = {'exactlyMatch': 0, 'formatError': 0, 'compileError': 0, 'passTestCase': 0}

        output = item['output']
        for i in range(beamSize):
            if output[str(i)]['exactlyMatch']:
                resultDict['exactlyMatch'] += 1

            if output[str(i)]['formatCheck']['formatResult'] is False:
                resultDict['formatError'] += 1

            if output[str(i)]['compileCheck']['compileResult'] is False:
                resultDict['compileError'] += 1

            if output[str(i)]['PassTestCase']:
                resultDict['passTestCase'] += 1


        print('Exactly Match:', resultDict['exactlyMatch'])
        print('Format Error:', resultDict['formatError'])
        print('Compile Error:', resultDict['compileError'])
        print('Pass Test Case:', resultDict['passTestCase'])

    def failure_reason(self, jsonFile):
        data = self.jsonFileIO.readJsonData(os.path.join(ROOT, jsonFile))

        compilePassButFailure = 0
        compileError = 0
        formatError = 0

        print()
        for item in data:
            if item['repair'] is False:

                output = item['output']
                for i in range(len(output)):
                    if not output[str(i)]['PassTestCase']:
                        if output[str(i)]['compileCheck']['compileResult']:
                            compilePassButFailure += 1
                            continue
                        else:
                            print("id:", item['buggyId'])
                            print("solution:\n", item['solution'])
                            print("============================================================")
                            print("============================================================")
                            if output[str(i)]['formatCheck']['formatResult'] is False:
                                print("Format Error")
                                formatError += 1
                            elif output[str(i)]['compileCheck']['compileResult'] is False:
                                print("Compile Error")
                                compileError += 1



                        print(output[str(i)]['patchCode'])
                        print("============================================================")



        print("Compile Pass But Failure", compilePassButFailure)
        print("formatError:", formatError)
        print("compileError:", compileError)