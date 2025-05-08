from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama
from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.Verification_QuixBugs import Verification_QuixBugs

def setUp():
    verification_QuixBugs = Verification_QuixBugs()
    verification_QuixBugs.setDataSetName('QuixBugs')
    verification_QuixBugs.setRemainderCodePath(None)
    verification_QuixBugs.setScriptPath('Tool/execute_python.sh')
    verification_QuixBugs.setJunitEnvironment('JUnit_Environment/JUnit_QuixBugs_Environment')
    verification_QuixBugs.setJunitModuleTestEnvironment('JUnit_ModuleTest/RunTestCase_QuixBugs')
    return verification_QuixBugs

def test_load_and_run_test_case(verification_QuixBugs):
    verification_QuixBugs.junitEnvironment_Initialize()
    verification_QuixBugs.junitEnvironment_Run_Initialize()
    verification_QuixBugs.juniEnvironment_TEST_File_Initialize()
    verification_QuixBugs.createJsonFramework([])
    runFileList = verification_QuixBugs.getAllRunTestCaseFileList()
    dictionary = verification_QuixBugs.getFileAndModuleDict(runFileList)
    verification_QuixBugs.runScriptBatchFile(dictionary)
    verification_QuixBugs.updateJsonResult()

def test_prompt_repair(verification_QuixBugs):
    promptEngineer = LLM_LangChain_CodeLlama()

    promptEngineer.setPromptRepairFileRoot('Result_Output/QuixBugs/Demo/PromptRepairFolder')
    promptEngineer.setPendingRepairFileListPath('Result_Output/QuixBugs/Demo/promptRepairProgram')
    promptEngineer.copyAndCreatePromptRepairFiles()
    promptEngineer.setOutputJsonFilePath('Result_Output/QuixBugs/Demo/PromptRepairFolder/BS_Lora04_PRE.json')
    promptEngineer.setPER_RepairTimes(5)
    promptEngineer.promptRepair()




if __name__ == '__main__':
    verification_QuixBugs = setUp()
    test_prompt_repair(verification_QuixBugs)


