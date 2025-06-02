# ALL Native LLM Use <FILL_ME> Type Generate Program

from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.Verification_HumanEval import Verification_HumanEval
from Module_Util.src.JsonFileIO import JsonFileIO

def setUp(LLM, Name):
    verification_HumanEval = Verification_HumanEval()
    verification_HumanEval.setDataSetName('HumanEval')
    verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
    verification_HumanEval.setScriptPath('Tool/execute_python.sh')
    verification_HumanEval.setJunitEnvironment('JUnit_Environment/JUnit_HumanEval_Environment')
    verification_HumanEval.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_HumanEval')

    verification_HumanEval.setTestDataResult(
        f'Result_Output/HumanEval/Native/{LLM}/Patch/HumanEval_{LLM}_Base10.jsonl')
    verification_HumanEval.setJsonResultPath(
        f'Result_Output/HumanEval/Native/{LLM}/Json/{Name}.json')
    verification_HumanEval.setLogFolderPath(
        f'Result_Output/HumanEval/Native/{LLM}/Log')
    verification_HumanEval.setRepairProgramPath(
        f'Result_Output/HumanEval/Native/{LLM}/repairProgram')
    verification_HumanEval.setPromptRepairProgramPath(
        f'Result_Output/HumanEval/Native/{LLM}/promptRepairProgram')
    verification_HumanEval.setLLMModel(LLM_CodeLlama())
    return verification_HumanEval

def load_and_run_test_case(verification_HumanEval):
    verification_HumanEval.junitEnvironment_Initialize()
    verification_HumanEval.junitEnvironment_Run_Initialize()
    verification_HumanEval.juniEnvironment_TEST_File_Initialize()
    verification_HumanEval.createJsonFramework([])
    runFileList = verification_HumanEval.getAllRunTestCaseFileList()
    dictionary = verification_HumanEval.getFileAndModuleDict(runFileList)
    verification_HumanEval.runScriptBatchFile(dictionary)
    verification_HumanEval.updateJsonResult()


def result_analysis():
    jsonFileIO = JsonFileIO()
    data = jsonFileIO.readJsonData(verification_HumanEval.getJsonResultPath())

    for item in data:
        if item['repair'] is False:
            print(item['buggyId'])

if __name__ == '__main__':
    verification_HumanEval = setUp('Qwen_3', 'Qwen3_HumanEval_Base10')
    load_and_run_test_case(verification_HumanEval)
    result_analysis()
