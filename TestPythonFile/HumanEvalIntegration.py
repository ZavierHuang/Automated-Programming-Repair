from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_HumanEval import Verification_HumanEval
from Module_Util.src.JsonFileIO import JsonFileIO

def setUp(diverseBeamSearch, name):
    verification_HumanEval = Verification_HumanEval()
    verification_HumanEval.setDataSetName('HumanEval')
    verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
    verification_HumanEval.setScriptPath('Tool/execute_python.sh')
    verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
    verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')

    verification_HumanEval.setTestDataResult(
        f'Result_Output/HumanEval/Qwen/OriginalResult/{diverseBeamSearch}/Lora16/Patch/HumanEval_{name}.jsonl')
    verification_HumanEval.setJsonResultPath(
        f'Result_Output/HumanEval/Qwen/OriginalResult/{diverseBeamSearch}/Lora16/Json/{name}.json')
    verification_HumanEval.setLogFolderPath(
        f'Result_Output/HumanEval/Qwen/OriginalResult/{diverseBeamSearch}/Lora16/Log')
    verification_HumanEval.setRepairProgramPath(
        f'Result_Output/HumanEval/Qwen/OriginalResult/{diverseBeamSearch}/Lora16/repairProgram')
    verification_HumanEval.setPromptRepairProgramPath(
        f'Result_Output/HumanEval/Qwen/OriginalResult/{diverseBeamSearch}/Lora16/promptRepairProgram')
    verification_HumanEval.setLLMModel(LLM_Qwen())
    return verification_HumanEval

def test_load_and_run_test_case(verification_HumanEval):
    verification_HumanEval.junitEnvironment_Initialize()
    verification_HumanEval.junitEnvironment_Run_Initialize()
    verification_HumanEval.juniEnvironment_TEST_File_Initialize()
    verification_HumanEval.createJsonFramework([])
    runFileList = verification_HumanEval.getAllRunTestCaseFileList()
    dictionary = verification_HumanEval.getFileAndModuleDict(runFileList)
    verification_HumanEval.runScriptBatchFile(dictionary)
    verification_HumanEval.updateJsonResult()


def test_result_analysis():
    jsonFileIO = JsonFileIO()
    data = jsonFileIO.readJsonData(verification_HumanEval.getJsonResultPath())

    for item in data:
        if item['repair'] is False:
            print(item['buggyId'])

if __name__ == '__main__':
    pendlingList = {
        'DiverseBeamSearch100':'Lora16_E2_DBS_100',
    }

    for diverseBeamSearch, name in pendlingList.items():
        verification_HumanEval = setUp(diverseBeamSearch, name)
        test_load_and_run_test_case(verification_HumanEval)
        test_result_analysis()
    
