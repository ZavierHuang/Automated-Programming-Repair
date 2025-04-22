import logging
import os
import shutil
import time

from overrides import overrides

from Config import ROOT
from Module_Src.src.Verification import Verification


class Verification_QuixBugs(Verification):
    def __init__(self):
        super().__init__()
        self.beamSize = None
        self.firstPredictPatchPath = None
        self.firstPredictPatchResultDict = {}
    
    def setBeamSize(self, beamSize):
        self.beamSize = beamSize
    
    def setFirstPredictPatchPath(self, firstPredictPatchPath):
        self.firstPredictPatchPath = os.path.join(ROOT, firstPredictPatchPath)

    def getFirstPredictPatchPath(self):
        return self.firstPredictPatchPath

    def getFirstPredictPatchResultDict(self):
        return self.firstPredictPatchResultDict
    
    def getBeamSize(self):
        return self.beamSize
    
    @overrides
    def junitEnvironment_Run_Initialize(self):
        super().junitEnvironment_Run_Initialize()

    @overrides
    def getImportContent(self, buggyId):
        importContent = 'import java.util.*;'
        importDict = {
            'BREADTH_FIRST_SEARCH': [
                'import java.util.ArrayDeque;'
            ],
            'KNAPSACK': [
                'import java.lang.*;',
            ],
            'NEXT_PALINDROME': [
                'import java.lang.Math.*;',
            ],
            'RPN_EVAL': [
                'import java.util.function.BinaryOperator;',
            ],
            'SHORTEST_PATHS': [
                'import java.lang.Math.*;',
            ],
            'SHORTEST_PATH_LENGTHS': [
                'import java.lang.Math.*;',
            ]
        }

        if buggyId in importDict.keys():
            importContent = importContent + '\n' +  ('\n'.join(importDict[buggyId]))

        return importContent

    @overrides
    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        # ADD --> ADD_TEST_1
        methodCode = methodCode.replace(buggyId, patchFileName)

        remainderCode = ''

        importContent = self.getImportContent(buggyId)

        javaCode = self.createJavaValidCode(patchFileName, methodCode, remainderCode, importContent)

        target = self.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        self.fileIO.writeFileData(target, javaCode)

        result = self.subprocess_run_JavaFormat(target)

        return result.stderr, result.returncode == 0

    @overrides
    def getNeedCompileJavaFiles(self, javaFile):
        data = self.fileIO.readFileData(javaFile)
        compileJavaFiles = [javaFile]

        for item in ['Node', 'QuixFixOracleHelper', 'WeightedEdge']:
            if item in data:
                compileJavaFiles.append(
                    # Node.java , Weighted, QuixFixOracleHelper doesn't have "package datastructures;"
                    os.path.join(ROOT, 'Data_Storage/QuixBugs/dataStructures/{}.java'.format(item)))

        return compileJavaFiles

    @overrides
    def checkJavaCompile(self, javaFile, javaFormatResult):
        if javaFormatResult is False:
            return 'FormatError', False

        javaFiles = self.getNeedCompileJavaFiles(javaFile)
        # print('javaFiles:', javaFiles)
        result = self.subprocess_run_JavaCompile(javaFiles)

        if result.returncode != 0:
            return result.stderr, False
        return result.stderr, True

    @overrides
    def updateJsonResult(self):
        fileList = self.fileIO.getFileListUnderFolder(self.getLogFolderPath())
        data = self.jsonFileIO.readJsonData(self.getJsonResultPath())

        for file in fileList:
            buggyId = file[:file.find('_TEST')]                                         # ADD_TEST_0.txt --> ADD
            patchNumber = file[file.find('_TEST_') + len('_TEST_'):-4]                  # ADD_TEST_0.txt --> 0
            logContent = self.fileIO.readFileData(os.path.join(self.getLogFolderPath(), file))
            print(buggyId, patchNumber, 'BUILD SUCCESSFUL' in logContent)
            if 'BUILD SUCCESSFUL' in logContent:
                for item in data:
                    if item['buggyId'] == buggyId:
                        item['repair'] = True
                        item['output'][str(patchNumber)]['PassTestCase'] = True
                        break

        self.jsonFileIO.writeJsonFile(data, self.getJsonResultPath())

    def multipleFillJsonCreate(self, jsonFilePaths, outputJsonFilePaths):
        data = self.jsonFileIO.readJsonLineData(jsonFilePaths)

        outputJsonFileList = []
        for item in data:
            if item['bug_id'] not in ['BREADTH_FIRST_SEARCH', 'FLATTEN', 'LCS_LENGTH']:
                continue

            buggyCode = item['buggy_code']
            output = item['output']
            for i in range(len(output)):
                patchCode = output[str(i)]['output_patch']
                newBuggyCode = self.getLLMModel().patchReplaceByModel(buggyCode, patchCode)
                newBuggyCode = self.getLLMModel().remarkErrorPosition(newBuggyCode)
                dictionary = {
                    'bug_id': item['bug_id'] + '_' + str(i),
                    'buggy_code': newBuggyCode,
                    'fixed_chunk': item['gold_patch'],
                }
                outputJsonFileList.append(dictionary)

        self.jsonFileIO.writeJsonLineFile(outputJsonFileList, outputJsonFilePaths)

    def createJsonFrameworkForMultipleError(self):
        QuixBugsSolution = self.jsonFileIO.readJsonData(
            os.path.join(ROOT, 'Data_Storage/QuixBugs/Solution/QuixBugsSolution.json'))

        data = self.jsonFileIO.readJsonLineData(self.getTestData())
        print(self.getTestData(),self.fileIO.isPathExist(self.getTestData()))
        dictionary = []
        previousBuggyId = None

        for item in data:
            originalId = item['bug_id']                                 # BREAD_FIRST_SEARCH_0
            currentBuggyId = originalId[:originalId.rfind('_')]         # BREAD_FIRST_SEARCH
            patchNumber = int(originalId[originalId.rfind('_') + 1:])   # 0

            buggyCode = item['buggy_code']
            output = item['output']
            solution = QuixBugsSolution[currentBuggyId]

            if currentBuggyId != previousBuggyId:
                subdictionary = {
                    'buggyId': currentBuggyId,
                    'repair': False,
                    'solution': QuixBugsSolution[currentBuggyId],
                    'type': self.checkBuggyMethodLine(buggyCode),
                    'output': {}
                }

            for i in range(len(output)):
                patchFileName = '{}_TEST_{}'.format(currentBuggyId, str(self.beamSize*patchNumber+i))
                patchCode = output[str(i)]['output_patch']
                target = os.path.join(self.getJunitEnvironment(),
                                      'Module_{}/{}.java'.format(currentBuggyId, patchFileName))
                targetModule = os.path.join(self.getJunitModuleTestEnvironment(),
                                            'Module_{}/src/main/java/{}.java'.format(currentBuggyId, patchFileName))

                methodCode = self.getLLMModel().patchReplaceByModel(buggyCode, patchCode)

                javaFormatLog, javaFormatResult = self.checkJavaFormat(methodCode, patchFileName, currentBuggyId)
                compileLog, compileResult = self.checkJavaCompile(target, javaFormatResult)

                if self.DataSetName == 'QuixBugs':
                    data = self.fileIO.readFileData(target)
                    for item in ['Node', 'WeightedEdge', 'QuixFixOracleHelper']:
                        if item in data:
                            data = 'import dataStructures.*;\n' + data
                            self.fileIO.writeFileData(target, data)
                            break

                print(patchFileName, compileResult, compileLog)

                self.fileIO.copyFile(target, targetModule, compileResult)
                self.fileIO.moveFile(target, self.getRepairProgramPath(), self.getPromptRepairProgramPath(), compileResult)

                subdictionary['output'][self.beamSize*patchNumber+i] = (
                    self.jsonFileIO.getJsonResultSubItem(
                        self.firstPredictPatchResultDict[currentBuggyId][i] + ',' + patchCode, compileLog, compileResult,
                        javaFormatLog, javaFormatResult, solution))

            if currentBuggyId != previousBuggyId:
                dictionary.append(subdictionary)

            previousBuggyId = currentBuggyId

        self.jsonFileIO.writeJsonFile(dictionary, self.getJsonResultPath())

    def getFirstPredictPatchResult(self, selectedList):
        data = self.jsonFileIO.readJsonLineData(self.firstPredictPatchPath)
        """
        firstPredictPatchDict = {
            'BREADTH_FIRST_SEARCH':[patchResult1, patchResult2, .......],
            'FLATTEN':[patchResult1, patchResult2, .......],
            'LCS_LENGTH':[patchResult1, patchResult2, .......],
        }
        """

        for item in data:
            buggyId = item['bug_id']
            if buggyId in selectedList:
                self.firstPredictPatchResultDict[buggyId] = []
                output = item['output']
                for i in range(len(output)):
                    self.firstPredictPatchResultDict[buggyId].append(output[str(i)]['output_patch'])

