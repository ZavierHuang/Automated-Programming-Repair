import os

from Module_Analysis.src.new_ResultAnalysis import NewResultAnalysis
from Module_LLM_PER.src.LLM_LangChain_Qwen import LLM_LangChain_Qwen
from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs


def setUp(Lora, CurrentRoot):
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')

    verification_QuixBugs.setTestDataResult(
        f'{CurrentRoot}/Patch/QuixBugs_Lora{Lora}_Demo.jsonl')
    verification_QuixBugs.setJsonResultPath(
        f'{CurrentRoot}/Json/Qwen3_Lora{Lora}_BS.json')
    verification_QuixBugs.setLogFolderPath(
        f'{CurrentRoot}/Log')
    verification_QuixBugs.setRepairProgramPath(
        f'{CurrentRoot}/repairProgram')
    verification_QuixBugs.setPromptRepairProgramPath(
        f'{CurrentRoot}/promptRepairProgram')
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


def generatePatchResult(LLM, BaseModel, Lora, diversity, CurrentRoot, dataSet, beamSize):
    verification_QuixBugs.getLLMModel().setIsLora(True)
    verification_QuixBugs.getLLMModel().setLoraAndEpoch(LLM, Lora, 2)
    verification_QuixBugs.getLLMModel().setNumBeams(beamSize)
    verification_QuixBugs.getLLMModel().setDiversity(diversity)
    verification_QuixBugs.getLLMModel().setDataSourceFilePath(dataSet)
    verification_QuixBugs.getLLMModel().setResultOutputFilePath(rf'{CurrentRoot}/Patch/QuixBugs_Lora{Lora}_Demo.jsonl')
    verification_QuixBugs.getLLMModel().setBaseModelPath(BaseModel)
    verification_QuixBugs.getLLMModel().llmPredictPatch()

###########################################################################################################

def prompt_repair(CurrentRoot, PromptRoot, verification_QuixBugs, Lora):
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')
    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()

    verification_QuixBugs.setJsonResultPath(f'{PromptRoot}/Json/QuixBugs_Lora{Lora}_PRE_RES.json')
    verification_QuixBugs.setLogFolderPath(f'{PromptRoot}/Log')

    promptEngineer = LLM_LangChain_Qwen()
    promptEngineer.setPromptRepairFileRoot(PromptRoot)
    promptEngineer.setPendingRepairFileListPath(f'{CurrentRoot}/promptRepairProgram')
    promptEngineer.copyAndCreatePromptRepairFiles()
    promptEngineer.setOutputJsonFilePath(f'{PromptRoot}/Json/QuixBugs_Lora{Lora}_PRE_FOM.json')
    promptEngineer.setPER_RepairTimes(5)
    promptEngineer.promptRepair()
    promptEngineer.copyFileToTest(verification_QuixBugs.getJunitModuleTestEnvironment(), verification_QuixBugs.getDataSetName())
    return promptEngineer.getPromptRepairFilesPath()


def Prompt_load_and_run_test_case(verification_QuixBugs, promptRepairFilesFolder):
    verification_QuixBugs.promptRepairCreateFramework(promptRepairFilesFolder)
    runFileList = verification_QuixBugs.getAllRunTestCaseFileList()
    dictionary = verification_QuixBugs.getFileAndModuleDict(runFileList)
    verification_QuixBugs.runScriptBatchFile(dictionary)
    verification_QuixBugs.PromptRepairUpdateJsonResult()

if __name__ == '__main__':
    Lora = '04'
    LLM = 'Qwen'
    BaseModel = 'Qwen/Qwen2.5-Coder-1.5B'
    CurrentRoot = 'Result_Output/Demo'
    dataSet = 'Data_Storage/QuixBugs/Qwen/Original_Data/QuixBugs_Qwen_IR4OR2_TEST.jsonl'
    beamSize = 10

    verification_QuixBugs = setUp(Lora, CurrentRoot)
    generatePatchResult(LLM, BaseModel, Lora, 0, CurrentRoot, dataSet, beamSize)
    load_and_run_test_case(verification_QuixBugs)

    newResultAnalysis  = NewResultAnalysis()
    newResultAnalysis.getReport(verification_QuixBugs.getJsonResultPath(), verification_QuixBugs.getLLMModel().getNumBeams())

    PromptRoot = os.path.join(CurrentRoot, 'PromptRepairFolder')
    promptRepairFilesFolder = prompt_repair(CurrentRoot, PromptRoot, verification_QuixBugs, Lora)
    Prompt_load_and_run_test_case(verification_QuixBugs, promptRepairFilesFolder)

