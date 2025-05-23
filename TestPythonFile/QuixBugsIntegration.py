from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs
from Module_Util.src.JsonFileIO import JsonFileIO


def setUp(diversity,name,Lora):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setTestDataResult(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/Lora{Lora}/Patch/QuixBugs_{name}.jsonl')
    verification_QuixBugs.setJsonResultPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/Lora{Lora}/Json/{name}.json')
    verification_QuixBugs.setLogFolderPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/Lora{Lora}/Log')
    verification_QuixBugs.setRepairProgramPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/Lora{Lora}/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        f'Result_Output/QuixBugs/Qwen/diversityBeamSearch{diversity}/Lora{Lora}/promptRepairProgram')
    verification_QuixBugs.setLLMModel(LLM_Qwen())

    return verification_QuixBugs


def test_load_and_run_test_case(verification_QuixBugs):
    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
    verification_QuixBugs.createJsonFramework(['BREADTH_FIRST_SEARCH','FLATTEN','LCS_LENGTH'])
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
    LoraList = ['04','08','16']

    for Lora in LoraList:
        pendlingList = {
            '20': f'Qwen_Lora{Lora}_DBS_20',
            '40': f'Qwen_Lora{Lora}_DBS_40',
            '60': f'Qwen_Lora{Lora}_DBS_60',
            '80': f'Qwen_Lora{Lora}_DBS_80',
            '100':f'Qwen_Lora{Lora}_DBS_100',
        }
        for diversity, name in pendlingList.items():
            verification_QuixBugs = setUp(diversity, name, Lora)
            test_load_and_run_test_case(verification_QuixBugs)
            test_result_analysis()


