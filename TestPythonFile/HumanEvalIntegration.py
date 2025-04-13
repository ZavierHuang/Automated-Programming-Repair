from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_HumanEval import Verification_HumanEval
from Module_Util.src.JsonFileIO import JsonFileIO

def setUp(current, diverseBeamSearch):
    verification_HumanEval = Verification_HumanEval()
    verification_HumanEval.setDataSetName('HumanEval')
    verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
    verification_HumanEval.setScriptPath('Tool/execute_python.sh')
    verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
    verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')

    verification_HumanEval.setTestDataResult(
        'Result_Output/HumanEval/CodeLlama/OriginalResult/DiverseBeamSearch40/Lora04/Patch/HumanEval_Lora04_E2_DBS_40.jsonl')
    verification_HumanEval.setJsonResultPath(
        'Result_Output/HumanEval/CodeLlama/OriginalResult/{}/Lora04/Json/{}.json'.format(diverseBeamSearch, current))
    verification_HumanEval.setLogFolderPath(
        'Result_Output/HumanEval/CodeLlama/OriginalResult/{}/Lora04/{}'.format(diverseBeamSearch, 'Log'))
    verification_HumanEval.setRepairProgramPath(
        'Result_Output/HumanEval/CodeLlama/OriginalResult/{}/Lora04/{}/'.format(diverseBeamSearch, 'repairProgram'))
    verification_HumanEval.setPromptRepairProgramPath(
        'Result_Output/HumanEval/CodeLlama/OriginalResult/{}/Lora04/{}/'.format(diverseBeamSearch,
                                                                        'promptRepairProgram'))
    verification_HumanEval.setLLMModel(LLM_Qwen())
    return verification_HumanEval

def test_load_and_run_test_case(verification_HumanEval):
    verification_HumanEval.junitEnvironment_Initialize()
    verification_HumanEval.junitEnvironment_Run_Initialize()
    verification_HumanEval.juniEnvironment_TEST_File_Initialize()
    verification_HumanEval.createJsonFramework([])
    verification_HumanEval.createPromptRepairProgramSet()
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
    diverseBeamSearch = 'DiverseBeamSearch40'
    current = 'Lora04_DBS_40'
    verification_HumanEval = setUp(current, diverseBeamSearch)
    test_load_and_run_test_case(verification_HumanEval)
    test_result_analysis()
    
