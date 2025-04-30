import os

from Config import ROOT
from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs

def setUp(lora, name, diversity):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setFirstPredictPatchPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/{lora}_Multiple/Patch/QuixBugs_Qwen_{lora}_DBS_{diversity}.jsonl')      # first predict result
    verification_QuixBugs.setTestDataResult(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/{lora}_Multiple/Patch/QuixBugs_Qwen_{lora}_DBS_{diversity}_Multiple.jsonl') # second predict result
    
    verification_QuixBugs.setJsonResultPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/{lora}_Multiple/Json/{name}.json')  # final output json
    verification_QuixBugs.setRepairProgramPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/{lora}_Multiple/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/{lora}_Multiple/promptRepairProgram')
    verification_QuixBugs.setLogFolderPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/{lora}_Multiple/Log')

    verification_QuixBugs.setLLMModel(LLM_Qwen())
    return verification_QuixBugs

def create_twice_patch(lora, verification_QuixBugs, outputJsonFilePath, diversity):
    verification_QuixBugs.multipleFillJsonCreate(verification_QuixBugs.getFirstPredictPatchPath(), outputJsonFilePath)
    verification_QuixBugs.getLLMModel().setIsLora(True)
    verification_QuixBugs.getLLMModel().setLoraAndEpoch(lora, 2)
    verification_QuixBugs.getLLMModel().setNumBeams(10)
    verification_QuixBugs.getLLMModel().setDiversity(diversity)
    verification_QuixBugs.getLLMModel().setDataSourceFilePath(outputJsonFilePath)
    verification_QuixBugs.getLLMModel().setResultOutputFilePath(verification_QuixBugs.getTestData())
    verification_QuixBugs.getLLMModel().llmPredictPatch()


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
    diversityList = [20, 40, 60, 80, 100]

    for diversity in diversityList:
        pendlingList = {
            'Lora04': f'Qwen_Lora04_DBS_{diversity}_Multiple',
            'Lora08': f'Qwen_Lora08_DBS_{diversity}_Multiple',
            'Lora16': f'Qwen_Lora16_DBS_{diversity}_Multiple',
        }

        for lora, name in pendlingList.items():
            outputJsonFilePath = os.path.join(ROOT,
                f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/{lora}_Multiple/Patch/QuixBugs_Qwen_{lora}_DBS_{diversity}_Multiple_Src.jsonl')
            verification_QuixBugs = setUp(lora, name, diversity)
            create_twice_patch(lora, verification_QuixBugs, outputJsonFilePath, diversity)
            load_and_run_test_case(verification_QuixBugs)

