# ALL Native LLM Use <FILL_ME> Type Generate Program
from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs
from Module_Util.src.JsonFileIO import JsonFileIO


def setUp(name, model):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setTestDataResult(
        f'Result_Output/QuixBugs/Native/{model}/Patch/QuixBugs_{model}_Base10.jsonl')
    verification_QuixBugs.setJsonResultPath(
        f'Result_Output/QuixBugs/Native/{model}/Json/{name}.json')
    verification_QuixBugs.setLogFolderPath(
        f'Result_Output/QuixBugs/Native/{model}/Log')
    verification_QuixBugs.setRepairProgramPath(
        f'Result_Output/QuixBugs/Native/{model}/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        f'Result_Output/QuixBugs/Native/{model}/promptRepairProgram')

    verification_QuixBugs.setLLMModel(LLM_CodeLlama())

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


def result_analysis():
    jsonFileIO = JsonFileIO()
    data = jsonFileIO.readJsonData(verification_QuixBugs.getJsonResultPath())

    for item in data:
        if item['repair'] is False:
            print(item['buggyId'])


if __name__ == '__main__':
    LLM = ['GPT4O']

    for model in LLM:
        name = f'{model}_QuixBugs_Base10'
        verification_QuixBugs = setUp(name, model)
        load_and_run_test_case(verification_QuixBugs)
        result_analysis()


