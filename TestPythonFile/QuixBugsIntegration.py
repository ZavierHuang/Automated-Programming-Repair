from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs


def setUp(Lora):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setTestDataResult(
        f'Result_Output/QuixBugs/Qwen_3/OriginalResult/BeamSearch/Lora{Lora}/Patch/QuixBugs_Qwen_3_Lora{Lora}_BS_E2.jsonl')
    verification_QuixBugs.setJsonResultPath(
        f'Result_Output/QuixBugs/Qwen_3/OriginalResult/BeamSearch/Lora{Lora}/Json/Qwen3_Lora{Lora}_BS.json')
    verification_QuixBugs.setLogFolderPath(
        f'Result_Output/QuixBugs/Qwen_3/OriginalResult/BeamSearch/Lora{Lora}/Log')
    verification_QuixBugs.setRepairProgramPath(
        f'Result_Output/QuixBugs/Qwen_3/OriginalResult/BeamSearch/Lora{Lora}/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        f'Result_Output/QuixBugs/Qwen_3/OriginalResult/BeamSearch/Lora{Lora}/promptRepairProgram')
    verification_QuixBugs.setLLMModel(LLM_Qwen())

    return verification_QuixBugs


def load_and_run_test_case(verification_QuixBugs):
    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
    verification_QuixBugs.createJsonFramework(['BREADTH_FIRST_SEARCH','FLATTEN','LCS_LENGTH'])
    runFileList = verification_QuixBugs.getAllRunTestCaseFileList()
    dictionary = verification_QuixBugs.getFileAndModuleDict(runFileList)
    verification_QuixBugs.runScriptBatchFile(dictionary)
    verification_QuixBugs.updateJsonResult()


def generatePatchResult(LLM, Lora, diversity):
    verification_QuixBugs.getLLMModel().setIsLora(True)
    verification_QuixBugs.getLLMModel().setLoraAndEpoch(LLM, Lora, 2)
    verification_QuixBugs.getLLMModel().setNumBeams(10)
    verification_QuixBugs.getLLMModel().setDiversity(diversity)
    verification_QuixBugs.getLLMModel().setDataSourceFilePath('Data_Storage/QuixBugs/Qwen/Original_Data/QuixBugs_Qwen_IR4OR2.jsonl')
    verification_QuixBugs.getLLMModel().setResultOutputFilePath(rf'Result_Output/QuixBugs/Qwen_3/OriginalResult/BeamSearch/Lora{Lora}/Patch/QuixBugs_Qwen_3_Lora{Lora}_BS_E2.jsonl')
    verification_QuixBugs.getLLMModel().setBaseModelPath('Qwen/Qwen2.5-Coder-3B')
    verification_QuixBugs.getLLMModel().llmPredictPatch()


if __name__ == '__main__':
    LoraList = ['04','08','16']

    for Lora in LoraList:
        verification_QuixBugs = setUp(Lora)
        generatePatchResult('Qwen_3B', Lora, 0)
        load_and_run_test_case(verification_QuixBugs)



