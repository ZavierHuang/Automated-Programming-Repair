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
        self.javaFilePath = None
        self.PER_RepairTimes = None
        self.buggyJavaCode = None
        self.errorMessage = ''

        self.compileJavaFiles = []
        self.fileIO = FileIO()


    def getLangChanName(self):
        return self.langChainName

    def setJavaFilePath(self, javaFilePath):
        self.javaFilePath = os.path.join(ROOT, javaFilePath)
        self.compileJavaFiles.append(self.javaFilePath)
        self.buggyJavaCode = self.fileIO.readFileData(self.javaFilePath)

    # Test
    def setBuggyCode(self, buggyJavaCode):
        self.buggyJavaCode = buggyJavaCode

    # Test
    def seterrorMessage(self, errorMessage):
        self.errorMessage = errorMessage

    def setPER_RepairTimes(self, times):
        self.PER_RepairTimes = times

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


    def needCompileJavaFiles(self):
       for item in ['Node','QuixFixOracleHelper', 'WeightedEdge']:
           if item in self.buggyJavaCode:
               self.compileJavaFiles.append(item)

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



    def LLM_Prediction(self):
        # llm = Ollama(model='qwen2.5-coder:1.5b')
        print("langchainName:",self.langChainName)
        llm = Ollama(model = self.langChainName)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI programmer proficient in Java, specializing in fixing errors in Java programs. 
                 I will provide a piece of Java code with errors along with the error messages, and I need you to correct them.
                 Please infer the behavior from the class name and fix the method errors.
                 Please only output corrected code and not include any other information."""),
            ("user", "{input}")
        ])

        chain = prompt | llm
        result = chain.invoke({"input": self.buggyJavaCode + '\n' + self.errorMessage})

        correctedCode = result[result.find('corrected code:'):]
        return correctedCode[correctedCode.find('```')+len('```'):correctedCode.rfind('```')]







