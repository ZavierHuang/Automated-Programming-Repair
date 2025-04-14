from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_HumanEval import Verification_HumanEval
from Module_Util.src.JsonFileIO import JsonFileIO

def setUp(name, folder):
    verification_HumanEval = Verification_HumanEval()
    verification_HumanEval.setDataSetName('HumanEval')
    verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
    verification_HumanEval.setScriptPath('Tool/execute_python.sh')
    verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
    verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')

    verification_HumanEval.setTestDataResult(
        'Result_Output/HumanEval/Qwen/OriginalResult/{}/Lora04/Patch/HumanEval_{}.jsonl'.format(folder, name))
    verification_HumanEval.setJsonResultPath(
        'Result_Output/HumanEval/Qwen/OriginalResult/{}/Lora04/Json/{}.json'.format(folder, name))
    verification_HumanEval.setLogFolderPath(
        'Result_Output/HumanEval/Qwen/OriginalResult/{}/Lora04/{}'.format(folder, 'Log'))
    verification_HumanEval.setRepairProgramPath(
        'Result_Output/HumanEval/Qwen/OriginalResult/{}/Lora04/{}/'.format(folder, 'repairProgram'))
    verification_HumanEval.setPromptRepairProgramPath(
        'Result_Output/HumanEval/Qwen/OriginalResult/{}/Lora04/{}/'.format(folder,
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
    pendlingList = {
        'BeamSearch':'Lora04_E2_BS',
        'DiverseBeamSearch20':'Lora04_E2_DBS_20',
        'DiverseBeamSearch40':'Lora04_E2_DBS_40',
        'DiverseBeamSearch60':'Lora04_E2_DBS_60',
        'DiverseBeamSearch80':'Lora04_E2_DBS_80',
        'DiverseBeamSearch100':'Lora04_E2_DBS_100',
    }

    for folder, name in pendlingList.items():
        verification_HumanEval = setUp(name, folder)
        test_load_and_run_test_case(verification_HumanEval)
        test_result_analysis()
    
