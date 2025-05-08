import os
import shutil

from Config import ROOT
from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs

def setUp(PromptRoot, name):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')
    verification_QuixBugs.setJsonResultPath(f'{PromptRoot}/Json/{name}_PRE_RES.json')
    verification_QuixBugs.setLogFolderPath(f'{PromptRoot}/Log')

    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
    return verification_QuixBugs

def load_and_run_test_case(verification_QuixBugs, promptRepairFilesFolder):
    verification_QuixBugs.promptRepairCreateFramework(promptRepairFilesFolder)
    runFileList = verification_QuixBugs.getAllRunTestCaseFileList()
    dictionary = verification_QuixBugs.getFileAndModuleDict(runFileList)
    verification_QuixBugs.runScriptBatchFile(dictionary)
    verification_QuixBugs.PromptRepairUpdateJsonResult()


def prompt_repair(CurrentRoot, PromptRoot, verification_QuixBugs, name):
    promptEngineer = LLM_LangChain_CodeLlama()
    promptEngineer.setPromptRepairFileRoot(PromptRoot)
    promptEngineer.setPendingRepairFileListPath(f'{CurrentRoot}/promptRepairProgram')
    promptEngineer.copyAndCreatePromptRepairFiles()
    promptEngineer.setOutputJsonFilePath(f'{PromptRoot}/Json/{name}_PRE_FEM.json')
    promptEngineer.setPER_RepairTimes(5)
    promptEngineer.promptRepair()
    promptEngineer.copyFileToTest(verification_QuixBugs.getJunitModuleTestEnvironment(), verification_QuixBugs.getDataSetName())
    return promptEngineer.getPromptRepairFilesPath()


if __name__ == '__main__':
    CurrentRoot = 'Result_Output/QuixBugs/CodeLlama/diversityBeamSearch100/Lora04'
    name = 'DBS_Lora04_100_CodeLlama'

    PromptRoot = os.path.join(CurrentRoot,'PromptRepairFolder')

    # test
    if os.path.exists(os.path.join(ROOT,PromptRoot)):
        shutil.rmtree(os.path.join(ROOT,PromptRoot))

    verification_QuixBugs = setUp(PromptRoot, name)
    promptRepairFilesFolder = prompt_repair(CurrentRoot, PromptRoot, verification_QuixBugs, name)

    load_and_run_test_case(verification_QuixBugs, promptRepairFilesFolder)


