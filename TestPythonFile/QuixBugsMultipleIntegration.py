import os

from Config import ROOT
from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs

def setUp(lora, name):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setFirstPredictPatchPath(
        f'Result_Output/QuixBugs/CodeLlama/BeamSearch/{lora}_Multiple/Patch/QuixBugs_{lora}_BS.jsonl')      # first predict result
    verification_QuixBugs.setTestDataResult(
        f'Result_Output/QuixBugs/CodeLlama/BeamSearch/{lora}_Multiple/Patch/QuixBugs_{lora}_BS_Multiple.jsonl') # second predict result
    
    verification_QuixBugs.setJsonResultPath(
        f'Result_Output/QuixBugs/CodeLlama/BeamSearch/{lora}_Multiple/Json/{name}.json')  # final output json
    verification_QuixBugs.setRepairProgramPath(
        f'Result_Output/QuixBugs/CodeLlama/BeamSearch/{lora}_Multiple/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        f'Result_Output/QuixBugs/CodeLlama/BeamSearch/{lora}_Multiple/promptRepairProgram')
    verification_QuixBugs.setLogFolderPath(
        f'Result_Output/QuixBugs/CodeLlama/BeamSearch/{lora}_Multiple/Log')

    verification_QuixBugs.setLLMModel(LLM_CodeLlama())
    return verification_QuixBugs

def create_twice_patch(verification_QuixBugs, outputJsonFilePath):
    verification_QuixBugs.multipleFillJsonCreate(verification_QuixBugs.getFirstPredictPatchPath(), outputJsonFilePath)
    verification_QuixBugs.getLLMModel().setIsLora(True)
    verification_QuixBugs.getLLMModel().setLoraAndEpoch(lora, 2)
    verification_QuixBugs.getLLMModel().setNumBeams(10)
    verification_QuixBugs.getLLMModel().setDiversity(0)
    verification_QuixBugs.getLLMModel().setDataSourceFilePath(outputJsonFilePath)
    verification_QuixBugs.getLLMModel().setResultOutputFilePath(verification_QuixBugs.getTestData())
    verification_QuixBugs.getLLMModel().llmPredictPatch()


def load_and_run_test_case(verification_QuixBugs):
    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
    #################################################################################
    verification_QuixBugs.setBeamSize(verification_QuixBugs.getLLMModel().getBeamSize())
    verification_QuixBugs.getFirstPredictPatchResult(['BREADTH_FIRST_SEARCH', 'FLATTEN', 'LCS_LENGTH'])
    verification_QuixBugs.createJsonFrameworkForMultipleError()
    #################################################################################
    runFileList = verification_QuixBugs.getAllRunTestCaseFileList()
    dictionary = verification_QuixBugs.getFileAndModuleDict(runFileList)
    verification_QuixBugs.runScriptBatchFile(dictionary)
    verification_QuixBugs.updateJsonResult()


if __name__ == '__main__':
    pendlingList = {
        'Lora04': 'CodeLlama_Lora04_BS_Multiple',
        'Lora08': 'CodeLlama_Lora08_BS_Multiple',
        'Lora16': 'CodeLlama_Lora16_BS_Multiple',
    }
    
    for lora, name in pendlingList.items():
        outputJsonFilePath = os.path.join(ROOT,
            f'Result_Output/QuixBugs/CodeLlama/BeamSearch/{lora}_Multiple/Patch/QuixBugs_{lora}_BS_Multiple_Src.jsonl')
        verification_QuixBugs = setUp(lora, name)
        create_twice_patch(verification_QuixBugs, outputJsonFilePath)
        load_and_run_test_case(verification_QuixBugs)

