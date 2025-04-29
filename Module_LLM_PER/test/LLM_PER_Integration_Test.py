import unittest

from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama
from Module_LLM_PER.src.LLM_PER import LLM_PER



class LLM_Model_Integration_Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.promptEngineer = LLM_LangChain_CodeLlama()

    def setUp(self):
        pass

    def test_prompt_Compile_LLM_Prediction(self):
        self.promptEngineer.setJavaFilePath('Module_LLM_PER/test/testFile/BREADTH_FIRST_SEARCH_TEST_99.java')
        self.promptEngineer.setPER_RepairTimes(1)
        self.promptEngineer.needCompileJavaFiles()
        self.promptEngineer.promtRepair_Compile()
        print("*****************************************************")
        print(self.promptEngineer.LLM_Prediction())
        print("*****************************************************")
        self.assertEqual(len(self.promptEngineer.getNeedCompileJavas()), 2)
        self.assertNotEqual(len(self.promptEngineer.getErrorMessage()), 0)




if __name__ == '__main__':
    unittest.main()