import os
import shutil
import time

from overrides import overrides

from Config import ROOT
from Module_Src.src.Verification import Verification


class Verification_QuixBugs(Verification):
    def __init__(self):
        super().__init__()

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
        print('javaFiles:', javaFiles)
        result = self.subprocess_run_JavaCompile(javaFiles)

        if result.returncode != 0:
            return result.stderr, False
        return result.stderr, True

    @overrides
    def updateJsonResult(self):
        fileList = self.fileIO.getFileListUnderFolder(self.getLogFolderPath())
        data = self.jsonFileIO.readJsonData(self.getJsonResultPath())

        for file in fileList:
            buggyId = file[:file.find('_TEST')]                                     # ADD_TEST_0.txt --> ADD
            sequence = file[file.find('_TEST_') + len('_TEST_'):-4]                 # ADD_TEST_0.txt --> 0
            logContent = self.fileIO.readFileData(os.path.join(self.getLogFolderPath(), file))
            print(buggyId, sequence, 'BUILD SUCCESSFUL' in logContent)
            if 'BUILD SUCCESSFUL' in logContent:
                for item in data:
                    if item['buggyId'] == buggyId:
                        item['repair'] = True
                        item['output'][str(sequence)]['PassTestCase'] = True
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
                    'buggyCode': newBuggyCode,
                    'fixed_chunk': item['gold_patch'],
                }
                outputJsonFileList.append(dictionary)

        self.jsonFileIO.writeJsonLineFile(outputJsonFileList, outputJsonFilePaths)
