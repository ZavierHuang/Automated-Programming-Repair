from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama


def setUp():
    promptEngineer = LLM_LangChain_CodeLlama()
    return promptEngineer


def test_prompt_repair(promptEngineer):
    promptEngineer.setPromptRepairFileRoot('Module_LLM_PER/test/SingleFileTest')

    if fileIO.isPathExist(os.path.join(promptEngineer.getPromptRepairFileRoot(), 'PromptRepairFile')):
        shutil.rmtree(os.path.join(promptEngineer.getPromptRepairFileRoot(), 'PromptRepairFile'))
        assertFalse(
            fileIO.isPathExist(os.path.join(promptEngineer.getPromptRepairFileRoot(), 'PromptRepairFile')))

    promptEngineer.setPendingRepairFileListPath('Module_LLM_PER/test/SingleFileTest/testFile')
    promptEngineer.setOutputJsonFilePath('Module_LLM_PER/test/SingleFileTest/test.json')
    promptEngineer.setPER_RepairTimes(5)
    promptEngineer.promptRepair()
    assertTrue(fileIO.isPathExist(promptEngineer.getOutputJsonFilePath()))





if __name__ == '__main__':
    promptEngineer = setUp()


