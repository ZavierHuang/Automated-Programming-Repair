# Prompt Engineering Repair
import os.path
import shutil
import subprocess

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

from Config import ROOT, CACHE_PATH
from Module_Util.src.FileIO import FileIO
from Module_Util.src.JsonFileIO import JsonFileIO


class LLM_PER:
    def __init__(self):
        self.langChainName = None
        self.PER_RepairTimes = None
        self.promptRepairFileRoot = None
        self.pendingRepairFileListPath = None
        self.promptRepairFileListPath = None
        self.promptRepairFileList = []

        self.buggyJavaCode = None
        self.errorMessage = 'Error'
        self.compileResult = None           # returnCode = 0 (Pass)
        self.javaFilePath = None
        self.compileJavaFiles = []
        self.outputJsonList = []
        self.outputJsonFilePath = None

        self.fileIO = FileIO()
        self.jsonFileIO = JsonFileIO()


    def getLangChanName(self):
        return self.langChainName

    def setPromptRepairFileRoot(self, promptRepairFileRoot):
        self.promptRepairFileRoot = os.path.join(ROOT, promptRepairFileRoot)

    def setOutputJsonFilePath(self, outputJsonFilePath):
        self.outputJsonFilePath = os.path.join(ROOT, outputJsonFilePath)

    def setPendingRepairFileListPath(self, pendingRepairFileListPath):
        self.pendingRepairFileListPath = os.path.join(ROOT, pendingRepairFileListPath)
        self.promptRepairFileListPath = os.path.join(self.promptRepairFileRoot, 'PromptRepairFile')
        shutil.copytree(self.pendingRepairFileListPath, self.promptRepairFileListPath)

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

    def getOutputJsonFilePath(self):
        return self.outputJsonFilePath

    def getCompileResult(self):
        return self.compileResult

    def getPromptRepairFileRoot(self):
        return self.promptRepairFileRoot

    def getPendingRepairFileListPath(self):
        return self.pendingRepairFileListPath

    def getPromptRepairFileListPath(self):
        return self.promptRepairFileListPath

    def getPromptRepairFileList(self):
        self.promptRepairFileList = self.fileIO.getFileListUnderFolder(self.promptRepairFileListPath)

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

    def needCompileJavaFiles(self, repairFile):
        self.compileJavaFiles.append(os.path.join(self.promptRepairFileListPath, repairFile))
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


    def promptRepair_Compile(self):
        result = self.subprocess_run_JavaCompile(self.compileJavaFiles)
        self.errorMessage = str(result.stderr)
        self.compileResult = int(result.returncode)



    def LLM_Prediction(self):
        llm = Ollama(
            model = self.langChainName,
            temperature = 0.5
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant specializing in Java programming.
            I will provide Java code containing errors, along with the corresponding error messages.
            Your task is to fix the errors based on the method name provided.
            Please output only the corrected Java code without any additional explanations or comments"""),
            ("user", "{input}")
        ])

        chain = prompt | llm
        promptRepairInput = self.buggyJavaCode + '\n' + self.errorMessage
        result = chain.invoke({"input": promptRepairInput})

        print("==================== promptRepairInput ===============")
        print(promptRepairInput)
        print("======================================================")

        print("========================= result =====================")
        print(result)


        if result.count('```') >= 2:
            fir_last_one = result.rfind('```')
            sec_last_one = result.rfind('```', 0, fir_last_one)
            return result[sec_last_one + len('```'):fir_last_one]
        else:
            return result


    def createItemJsonFramework(self, repairFile):
        subItemDictionary = {
            'buggyId': repairFile[:repairFile.rfind('.java')],
            'repair': False,
            'repairTimes': 0,
            'output': {str(i): {'errorMessage': 'None'} for i in range(self.PER_RepairTimes+1)}
        }

        return subItemDictionary

    def promptRepair(self):
        self.getPromptRepairFileList()
        for repairFile in self.promptRepairFileList:
            self.setJavaFilePath(os.path.join(self.promptRepairFileListPath,repairFile))
            self.compileJavaFiles.clear()
            self.errorMessage = 'Error'

            subItemDictionary = self.createItemJsonFramework(repairFile)

            self.needCompileJavaFiles(repairFile)


            for i in range(self.PER_RepairTimes+1):
                self.promptRepair_Compile()

                repairJavaCode = self.LLM_Prediction()

                print("============================================================")
                print("i:", i)
                print('writeFile:', os.path.join(self.getPromptRepairFileListPath(), repairFile))
                print('repairJavaCode:\n', repairJavaCode)
                print("============================================================")

                self.fileIO.writeFileData(os.path.join(self.getPromptRepairFileListPath(), repairFile), repairJavaCode)

                if self.compileResult == 0:
                    subItemDictionary['repair'] = True
                    subItemDictionary['output'][str(i)]['errorMessage'] = 'Compile Success'
                    break

                subItemDictionary['repairTimes'] = i + 1
                subItemDictionary['output'][str(i)]['errorMessage'] = self.errorMessage
                self.buggyJavaCode = self.fileIO.readFileData(os.path.join(self.getPromptRepairFileListPath(), repairFile))



            if(subItemDictionary['repair'] is False):
                self.fileIO.deleteFileData(os.path.join(self.getPromptRepairFileListPath(), repairFile))

            print("==================== SubItemDictionary =====================")
            print(subItemDictionary)
            print("============================================================")

            self.outputJsonList.append(subItemDictionary)

        self.jsonFileIO.writeJsonFile(self.outputJsonList, self.outputJsonFilePath)




