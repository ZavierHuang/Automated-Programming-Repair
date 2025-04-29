import unittest

from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama
from Module_LLM_PER.src.LLM_PER import LLM_PER



class LLM_Model_Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.promptEngineer = LLM_LangChain_CodeLlama()

    def setUp(self):
        self.promptEngineer.setJavaFilePath('Module_LLM_PER/test/testFile/ADD_ELEMENTS_TEST_9.java')
        self.promptEngineer.setPER_RepairTimes(1)



    # def test_prompt_engineering_repair(self):
    #     self.promptEngineer.needCompileJavaFiles()
    #     self.promptEngineer.promtRepair_Compile()

    def test_LLM_Prediction(self):
        self.promptEngineer.setBuggyCode("""
        import java.util.*;
        public class ADD_ELEMENTS_TEST_9 {
                public static int add_elements(ArrayList<Integer> arr, int k) {
        int result = 0;
        for(int i = 0; i < k; i++) {
        // buggy code
        //             if(Integer.toString(arr.get(i)).length() >= 2) {
        //                 result -= arr.get(i);
                    
                    }
                }
                return result;
            }
        }
        """)
        print(self.promptEngineer.LLM_Prediction())


if __name__ == '__main__':
    unittest.main()