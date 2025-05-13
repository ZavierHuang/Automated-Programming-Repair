import os
import shutil

from Config import ROOT
from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama
from Module_Src.src.Verification_HumanEval import Verification_HumanEval

def setUp(PromptRoot, name):
    verification_HumanEval = Verification_HumanEval()
    verification_HumanEval.setDataSetName('HumanEval')
    verification_HumanEval.setRemainderCodePath(None)
    verification_HumanEval.setScriptPath('Tool/execute_python.sh')
    verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
    verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')
    verification_HumanEval.setJsonResultPath(f'{PromptRoot}/Json/{name}_PRE_RES.json')
    verification_HumanEval.setLogFolderPath(f'{PromptRoot}/Log')

    verification_HumanEval.junitEnvironment_Initialize()
    verification_HumanEval.junitEnvironment_Run_Initialize()
    verification_HumanEval.juniEnvironment_TEST_File_Initialize()
    return verification_HumanEval

def load_and_run_test_case(verification_HumanEval, promptRepairFilesFolder):
    verification_HumanEval.promptRepairCreateFramework(promptRepairFilesFolder)
    runFileList = verification_HumanEval.getAllRunTestCaseFileList()
    dictionary = verification_HumanEval.getFileAndModuleDict(runFileList)
    verification_HumanEval.runScriptBatchFile(dictionary)
    verification_HumanEval.PromptRepairUpdateJsonResult()


def prompt_repair(CurrentRoot, PromptRoot, verification_HumanEval, name):
    promptEngineer = LLM_LangChain_CodeLlama()
    promptEngineer.setPromptRepairFileRoot(PromptRoot)
    promptEngineer.setPendingRepairFileListPath(f'{CurrentRoot}/promptRepairProgram')
    promptEngineer.copyAndCreatePromptRepairFiles()
    promptEngineer.setOutputJsonFilePath(f'{PromptRoot}/Json/{name}_PRE_FEM.json')
    promptEngineer.setPER_RepairTimes(5)
    promptEngineer.promptRepair()
    promptEngineer.copyFileToTest(verification_HumanEval.getJunitModuleTestEnvironment(), verification_HumanEval.getDataSetName())
    return promptEngineer.getPromptRepairFilesPath()


if __name__ == '__main__':
    Lora = '08'
    CurrentRoot = f'Result_Output/HumanEval/CodeLlama/OriginalResult/BeamSearch/Lora{Lora}'
    name = f'BS_Lora{Lora}_CodeLlama'

    PromptRoot = os.path.join(CurrentRoot,'PromptRepairFolder')

    print("ABS PromptRoot:", os.path.join(ROOT, PromptRoot))

    # test
    if os.path.exists(os.path.join(ROOT,PromptRoot)):
        shutil.rmtree(os.path.join(ROOT,PromptRoot))

    verification_HumanEval = setUp(PromptRoot, name)
    promptRepairFilesFolder = prompt_repair(CurrentRoot, PromptRoot, verification_HumanEval, name)

    load_and_run_test_case(verification_HumanEval, promptRepairFilesFolder)


