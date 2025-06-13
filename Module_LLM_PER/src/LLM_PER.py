# Prompt Engineering Repair
import os.path
import shutil
import subprocess

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

from Config import ROOT, CACHE_PATH
from Module_Src.src.Verification import Verification
from Module_Util.src.FileIO import FileIO
from Module_Util.src.JsonFileIO import JsonFileIO


class LLM_PER:
    def __init__(self):
        self.langChainName = None
        self.PER_RepairTimes = None
        self.promptRepairFileRoot = None
        self.pendingRepairFileListPath = None
        self.promptRepairFiles = None
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
        self.verification = Verification()

    def getLangChanName(self):
        return self.langChainName

    def setPromptRepairFileRoot(self, promptRepairFileRoot):
        self.promptRepairFileRoot = os.path.join(ROOT, promptRepairFileRoot)
        if(not self.fileIO.isPathExist(self.promptRepairFileRoot)):
            os.mkdir(self.promptRepairFileRoot)

    def setOutputJsonFilePath(self, outputJsonFilePath):
        self.outputJsonFilePath = os.path.join(ROOT, outputJsonFilePath)

    def setPendingRepairFileListPath(self, pendingRepairFileListPath):
        self.pendingRepairFileListPath = os.path.join(ROOT, pendingRepairFileListPath)
        self.promptRepairFiles = os.path.join(self.promptRepairFileRoot, 'PromptRepairFiles')

    def copyAndCreatePromptRepairFiles(self):
        shutil.copytree(self.pendingRepairFileListPath, self.promptRepairFiles)

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

    def getPromptRepairFilesPath(self):
        return self.promptRepairFiles

    def getPromptRepairFileList(self):
        self.promptRepairFileList = self.fileIO.getFileListUnderFolder(self.promptRepairFiles)

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
        self.compileJavaFiles.append(os.path.join(self.promptRepairFiles, repairFile))
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
            Please output only the corrected Java code without any additional explanations or comments.
            Please Pay special attention to index boundaries to prevent ArrayIndexOutOfBoundsException or StringIndexOutOfBoundsException."""),
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
            return result[sec_last_one + len('```'):fir_last_one].replace('java','').replace('import .util.*;', 'import java.util.*;')
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
            self.setJavaFilePath(os.path.join(self.promptRepairFiles,repairFile))
            self.compileJavaFiles.clear()
            self.errorMessage = 'Error'

            subItemDictionary = self.createItemJsonFramework(repairFile)

            self.needCompileJavaFiles(repairFile)


            for i in range(self.PER_RepairTimes+1):
                self.promptRepair_Compile()

                repairJavaCode = self.LLM_Prediction()

                print("============================================================")
                print("i:", i)
                print('writeFile:', os.path.join(self.getPromptRepairFilesPath(), repairFile))
                print('repairJavaCode:\n', repairJavaCode)
                print("============================================================")

                self.fileIO.writeFileData(os.path.join(self.getPromptRepairFilesPath(), repairFile), repairJavaCode)


                if self.compileResult == 0:
                    self.verification.subprocess_run_JavaFormat(os.path.join(self.getPromptRepairFilesPath(), repairFile))

                    subItemDictionary['repair'] = True
                    subItemDictionary['output'][str(i)]['errorMessage'] = 'Compile Success'
                    break

                subItemDictionary['repairTimes'] = i + 1
                subItemDictionary['output'][str(i)]['errorMessage'] = self.errorMessage
                self.buggyJavaCode = self.fileIO.readFileData(os.path.join(self.getPromptRepairFilesPath(), repairFile))


            if(subItemDictionary['repair'] is False):
                print("===================== DELETE ==================" , os.path.join(self.getPromptRepairFilesPath(), repairFile))
                self.fileIO.deleteFileData(os.path.join(self.getPromptRepairFilesPath(), repairFile))

            print("==================== SubItemDictionary =====================")
            print(subItemDictionary)
            print("============================================================")

            self.outputJsonList.append(subItemDictionary)

        self.jsonFileIO.writeJsonFile(self.outputJsonList, self.outputJsonFilePath)


    def copyFileToTest(self, junitModuleTestEnv, DataSet):
        fileList = self.fileIO.getFileListUnderFolder(self.promptRepairFiles)

        for file in fileList:
            module = file[:file.rfind('_TEST')]
            filePath = os.path.join(self.getPromptRepairFilesPath(), file)

            data = self.fileIO.readFileData(filePath)

            if 'import java.util.*;' not in data:
                data = 'import java.util.*;\n' + data

            if DataSet == 'QuixBugs':
                for item in ['Node', 'WeightedEdge', 'QuixFixOracleHelper']:
                    if item in data:
                        data = 'import dataStructures.*;\n' + data
                        self.fileIO.writeFileData(filePath, data)
                        break

            targetModuleFolderPath = os.path.join(f'{junitModuleTestEnv}/Module_{module}/src/main/java')
            shutil.copy(filePath, targetModuleFolderPath)

            print("filePath:", filePath, "targetModuleFolderPath:", targetModuleFolderPath)


