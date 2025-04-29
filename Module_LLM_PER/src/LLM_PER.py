# Prompt Engineering Repair
import os.path
import subprocess

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

from Config import ROOT, CACHE_PATH
from Module_Util.src.FileIO import FileIO


class LLM_PER:
    def __init__(self):
        self.langChainName = None
        self.PER_RepairTimes = None
        self.promptRepairFileListPath = None
        self.promptRepairFileList = []

        self.buggyJavaCode = None
        self.errorMessage = 'Error'
        self.compileResult = None           # returnCode = 0 (Pass)
        self.javaFilePath = None
        self.compileJavaFiles = []
        self.outputJsonList = []
        self.fileIO = FileIO()


    def getLangChanName(self):
        return self.langChainName

    def setPromptRepairFileListPath(self, promptRepairFileListPath):
        self.promptRepairFileListPath = os.path.join(ROOT, promptRepairFileListPath)

    def setJavaFilePath(self, javaFilePath):
        self.javaFilePath = os.path.join(ROOT, javaFilePath)
        self.compileJavaFiles.append(self.javaFilePath)
        self.buggyJavaCode = self.fileIO.readFileData(self.javaFilePath).replace('import dataStructures.*;', '').strip()
        self.fileIO.writeFileData(self.javaFilePath, self.buggyJavaCode)

    # Test
    def setBuggyCode(self, buggyJavaCode):
        self.buggyJavaCode = buggyJavaCode

    def setPER_RepairTimes(self, times):
        self.PER_RepairTimes = times

    def getCompileResult(self):
        return self.compileResult

    def getPromptRepairFileListPath(self):
        return self.promptRepairFileListPath

    def getPromptRepairFileList(self):
        fileList = self.fileIO.getFileListUnderFolder(self.promptRepairFileListPath)

        for file in fileList:
            filePath = os.path.join(self.promptRepairFileListPath, file)
            self.promptRepairFileList.append(os.path.join(ROOT, filePath))

        return self.promptRepairFileList

    def getJavaFilePath(self):
        return self.javaFilePath

    def getPER_RepairTimes(self):
        return self.PER_RepairTimes

    def getNeedCompileJavas(self):
        return self.compileJavaFiles

    def getBuggyCode(self):
        return self.buggyJavaCode

    def getErrorMessage(self):
        return self.errorMessage

    def getOutputJsonList(self):
        return self.outputJsonList

    def needCompileJavaFiles(self):
        for item in ['Node', 'QuixFixOracleHelper', 'WeightedEdge']:
            if item in self.buggyJavaCode:
                self.compileJavaFiles.append(
                    # Node.java , Weighted, QuixFixOracleHelper doesn't have "package datastructures;"
                    os.path.join(ROOT, f'Data_Storage/QuixBugs/dataStructures/{item}.java'))

    def subprocess_run_JavaCompile(self, javaFiles):
        result = subprocess.run(
            ['javac', '-d', CACHE_PATH] + javaFiles,
            capture_output=True,
            text=True
        )
        return result


    def promtRepair_Compile(self):
        result = self.subprocess_run_JavaCompile(self.compileJavaFiles)
        self.errorMessage = str(result.stderr)
        self.compileResult = result.returncode



    def LLM_Prediction(self):
        llm = Ollama(model = self.langChainName)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI programmer proficient in Java, specializing in fixing errors in Java programs. 
                 I will provide a piece of Java code with errors along with the error messages, and I need you to correct them.
                 Please infer the behavior from the class name and fix the method errors.
                 Please only output corrected code and not include any other information."""),
            ("user", "{input}")
        ])

        chain = prompt | llm
        promptRepairInput = self.buggyJavaCode + '\n' + self.errorMessage
        result = chain.invoke({"input": promptRepairInput})

        correctedCode = result[result.find('corrected'):]
        return correctedCode[correctedCode.find('```')+len('```'):correctedCode.rfind('```')]

    def createItemJsonFramework(self, repairFile):
        buggyId = repairFile[repairFile.find(self.promptRepairFileListPath) + len(self.promptRepairFileListPath) + 1:repairFile.rfind('.java')]

        subItemDictionary = {
            'buggyId': buggyId,
            'repair': False,
            'repairTimes': 0,
            'output': {str(i): {'errorMessage': 'None'} for i in range(1, self.PER_RepairTimes + 1)}
        }

        return subItemDictionary

    def promptRepair(self):
        for repairFile in self.promptRepairFileList:
            self.setJavaFilePath(repairFile)
            self.compileJavaFiles.clear()
            self.errorMessage = 'Error'

            subItemDictionary = self.createItemJsonFramework(repairFile)

            for i in range(self.PER_RepairTimes):
                self.needCompileJavaFiles()
                self.promtRepair_Compile()
                self.LLM_Prediction()

                if self.compileResult == 0:
                    subItemDictionary['repair'] = True
                    subItemDictionary['repairTimes'] = i
                    subItemDictionary['output'][str(i)]['errorMessage'] = 'Compile Success'
                    break

            self.outputJsonList.append(subItemDictionary)





