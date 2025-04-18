from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs
from Module_Util.src.JsonFileIO import JsonFileIO

def setUp(current):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setFirstPredictPatchPath(
        'Result_Output/QuixBugs/Qwen/BeamSearch/Demo_Multiple/Patch/Qwen_Patch05_first.jsonl')
    verification_QuixBugs.setTestDataResult(
        'Result_Output/QuixBugs/Qwen/BeamSearch/Demo_Multiple/Patch/Qwen_Patch05_Multiple_twice.jsonl')
    
    verification_QuixBugs.setJsonResultPath(
        'Result_Output/QuixBugs/Qwen/BeamSearch/Demo_Multiple/Json/Qwen_test_Multiple_Patch.json')
    verification_QuixBugs.setRepairProgramPath(
        'Result_Output/QuixBugs/Qwen/BeamSearch/Demo_Multiple/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        'Result_Output/QuixBugs/Qwen/BeamSearch/Demo_Multiple/promptRepairProgram')
    verification_QuixBugs.setLogFolderPath(
        'Result_Output/QuixBugs/Qwen/BeamSearch/Demo_Multiple/Log')

    verification_QuixBugs.setLLMModel(LLM_Qwen())
    return verification_QuixBugs

def test_load_and_run_test_case(verification_QuixBugs):
    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
    #################################################################################
    verification_QuixBugs.setBeamSize(5)
    verification_QuixBugs.getFirstPredictPatchResult(['BREADTH_FIRST_SEARCH', 'FLATTEN', 'LCS_LENGTH'])
    verification_QuixBugs.createJsonFrameworkForMultipleError()
    #################################################################################
    verification_QuixBugs.createPromptRepairProgramSet()
    runFileList = verification_QuixBugs.getAllRunTestCaseFileList()
    dictionary = verification_QuixBugs.getFileAndModuleDict(runFileList)
    verification_QuixBugs.runScriptBatchFile(dictionary)
    verification_QuixBugs.updateJsonResult()

def test_result_analysis():
    jsonFileIO = JsonFileIO()
    data = jsonFileIO.readJsonData(verification_QuixBugs.getJsonResultPath())

    for item in data:
        if item['repair'] is False:
            print(item['buggyId'])

if __name__ == '__main__':
    current = 'BS_Lora04'
    verification_QuixBugs = setUp(current)
    test_load_and_run_test_case(verification_QuixBugs)
    test_result_analysis()
    
