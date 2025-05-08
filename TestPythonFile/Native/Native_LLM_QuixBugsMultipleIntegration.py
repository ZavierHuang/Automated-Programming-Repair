# ALL Native LLM Use <FILL_ME> Type Generate Program

import os

from Config import ROOT
from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs

def setUp(name, model):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setFirstPredictPatchPath(
        f'Result_Output/QuixBugs/Native/{model}_Multiple/Patch/QuixBugs_{model}_Base10.jsonl')      # first predict result
    verification_QuixBugs.setTestDataResult(
        f'Result_Output/QuixBugs/Native/{model}_Multiple/Patch/QuixBugs_{model}_Base10_Multiple.jsonl') # second predict result
    
    verification_QuixBugs.setJsonResultPath(
        f'Result_Output/QuixBugs/Native/{model}_Multiple/Json/{name}.json')  # final output json
    verification_QuixBugs.setRepairProgramPath(
        f'Result_Output/QuixBugs/Native/{model}_Multiple/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        f'Result_Output/QuixBugs/Native/{model}_Multiple/promptRepairProgram')
    verification_QuixBugs.setLogFolderPath(
        f'Result_Output/QuixBugs/Native/{model}_Multiple/Log')

    verification_QuixBugs.setLLMModel(LLM_CodeLlama())
    return verification_QuixBugs

def create_twice_patch(verification_QuixBugs, outputJsonFilePath):
    verification_QuixBugs.multipleFillJsonCreate(verification_QuixBugs.getFirstPredictPatchPath(), outputJsonFilePath)


def load_and_run_test_case(verification_QuixBugs):
    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
    #################################################################################
    verification_QuixBugs.setBeamSize(10)
    verification_QuixBugs.getFirstPredictPatchResult(['BREADTH_FIRST_SEARCH', 'FLATTEN', 'LCS_LENGTH'])
    verification_QuixBugs.createJsonFrameworkForMultipleError()
    #################################################################################
    runFileList = verification_QuixBugs.getAllRunTestCaseFileList()
    dictionary = verification_QuixBugs.getFileAndModuleDict(runFileList)
    verification_QuixBugs.runScriptBatchFile(dictionary)
    verification_QuixBugs.updateJsonResult()


if __name__ == '__main__':
        pendlingList = {
            'CodeLlama': f'CodeLlama_Base10_Multiple',
            'Qwen': f'Qwen_Base10_Multiple',
        }

        for model, name in pendlingList.items():
            outputJsonFilePath = os.path.join(ROOT,
                f'Result_Output/QuixBugs/Native/{model}_Multiple/Patch/QuixBugs_{model}_Base10_Multiple_Src.jsonl')
            verification_QuixBugs = setUp(name, model)
            # create_twice_patch(verification_QuixBugs, outputJsonFilePath)
            load_and_run_test_case(verification_QuixBugs)

