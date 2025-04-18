from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.Verification_HumanEval import Verification_HumanEval
from Module_Util.src.JsonFileIO import JsonFileIO

def setUp(epoch, name):
    verification_HumanEval = Verification_HumanEval()
    verification_HumanEval.setDataSetName('HumanEval')
    verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
    verification_HumanEval.setScriptPath('Tool/execute_python.sh')
    verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
    verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')

    verification_HumanEval.setTestDataResult(
        f'Result_Output/HumanEval/CodeLlama/OtherEpoch/{epoch}/Lora16/Patch/HumanEval_{name}.jsonl')
    verification_HumanEval.setJsonResultPath(
        f'Result_Output/HumanEval/CodeLlama/OtherEpoch/{epoch}/Lora16/Json/{name}.json')
    verification_HumanEval.setLogFolderPath(
        f'Result_Output/HumanEval/CodeLlama/OtherEpoch/{epoch}/Lora16/Log')
    verification_HumanEval.setRepairProgramPath(
        f'Result_Output/HumanEval/CodeLlama/OtherEpoch/{epoch}/Lora16/repairProgram')
    verification_HumanEval.setPromptRepairProgramPath(
        f'Result_Output/HumanEval/CodeLlama/OtherEpoch/{epoch}/Lora16/promptRepairProgram')
    verification_HumanEval.setLLMModel(LLM_CodeLlama())
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
        'epoch3':'CodeLlama_Lora16_E3_BS',
        'epoch4':'CodeLlama_Lora16_E4_BS',
        'epoch5':'CodeLlama_Lora16_E5_BS',
    }

    for epoch, name in pendlingList.items():
        verification_HumanEval = setUp(epoch, name)
        test_load_and_run_test_case(verification_HumanEval)
        test_result_analysis()
    
