import os
import shutil
import unittest

from Config import ROOT
from Module_LLM_PER.src.LLM_LangChain_CodeLlama import LLM_LangChain_CodeLlama
from Module_LLM_PER.src.LLM_PER import LLM_PER
from Module_Util.src.FileIO import FileIO


class LLM_Model_Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.fileIO = FileIO()
        self.promptEngineer = LLM_LangChain_CodeLlama()

    def setUp(self):
        pass

    def test_prompt_engineering_repair(self):
        self.promptEngineer.setJavaFilePath('Module_LLM_PER/test/BatchFileTest/testFile/ADD_ELEMENTS_TEST_9.java')
        self.promptEngineer.setPER_RepairTimes(1)
        self.promptEngineer.needCompileJavaFiles()
        self.promptEngineer.promptRepair_Compile()

        print(self.promptEngineer.getErrorMessage())
        print(self.promptEngineer.getCompileResult())
        self.assertEqual(len(self.promptEngineer.getNeedCompileJavas()), 1)
        self.assertNotEqual(len(self.promptEngineer.getErrorMessage()), 0)
        self.assertNotEqual(self.promptEngineer.getCompileResult(), 0)

    def test_prompt_Copy_Tree_LLM_Prediction(self):
        self.promptEngineer.setPromptRepairFileRoot('Module_LLM_PER/test/SingleFileTest')
        self.promptEngineer.setPendingRepairFileListPath('Module_LLM_PER/test/SingleFileTest/testFile')
        self.assertTrue(self.fileIO.isPathExist(os.path.join(self.promptEngineer.getPromptRepairFileRoot(), 'PromptRepairFiles')))
        shutil.rmtree(self.promptEngineer.getPromptRepairFileListPath())
        self.assertFalse(self.fileIO.isPathExist(os.path.join(self.promptEngineer.getPromptRepairFileRoot(), 'PromptRepairFiles')))


    def test_prompt_engineering_repair_with_Node(self):
        self.promptEngineer.setJavaFilePath('Module_LLM_PER/test/BatchFileTest/testFile/BREADTH_FIRST_SEARCH_TEST_99.java')
        self.promptEngineer.setPER_RepairTimes(1)
        self.promptEngineer.needCompileJavaFiles()
        self.promptEngineer.promptRepair_Compile()

        print(self.promptEngineer.getNeedCompileJavas())
        print(self.promptEngineer.getErrorMessage())
        self.assertEqual(len(self.promptEngineer.getNeedCompileJavas()), 2)
        self.assertNotEqual(len(self.promptEngineer.getErrorMessage()), 0)

    def test_LLM_Prediction_By_Input(self):
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

    def test_compile_Success_ErrorMessage_is_Empty(self):
        self.promptEngineer.setJavaFilePath('Module_LLM_PER/test/BatchFileTest/testFile/BREADTH_FIRST_SEARCH_Compile_Pass.java')
        self.promptEngineer.setPER_RepairTimes(1)
        self.promptEngineer.needCompileJavaFiles()
        self.promptEngineer.promptRepair_Compile()

        print(self.promptEngineer.getNeedCompileJavas())
        print(self.promptEngineer.getErrorMessage())
        print(self.promptEngineer.getCompileResult())
        self.assertEqual(len(self.promptEngineer.getNeedCompileJavas()), 2)
        self.assertEqual(len(self.promptEngineer.getErrorMessage()), 0)
        self.assertEqual(self.promptEngineer.getCompileResult(), 0)

    def test_prompt_repair_file_list(self):
        self.promptEngineer.setPromptRepairFileRoot('Module_LLM_PER/test/BatchFileTest')
        self.promptEngineer.setPendingRepairFileListPath('Module_LLM_PER/test/BatchFileTest/testFile')
        promptRepairFileList = self.promptEngineer.getPromptRepairFileList()
        self.assertEqual(len(promptRepairFileList), 5)

    def test_create_output_Item_framework(self):
        self.promptEngineer.setPromptRepairFileRoot('Module_LLM_PER/test/BatchFileTest')

        if self.fileIO.isPathExist(os.path.join(self.promptEngineer.getPromptRepairFileRoot(),'PromptRepairFiles')):
            shutil.rmtree(os.path.join(self.promptEngineer.getPromptRepairFileRoot(),'PromptRepairFiles'))
            self.assertFalse(self.fileIO.isPathExist(os.path.join(self.promptEngineer.getPromptRepairFileRoot(),'PromptRepairFiles')))

        self.promptEngineer.setPendingRepairFileListPath('Module_LLM_PER/test/BatchFileTest/testFile')
        self.promptEngineer.setPER_RepairTimes(3)


        subItemDictionary = self.promptEngineer.createItemJsonFramework('BREADTH_FIRST_SEARCH_TEST_99.java')

        expected = {
            'buggyId': 'BREADTH_FIRST_SEARCH_TEST_99',
            'repair': False,
            'repairTimes': 0,
            'output': {
                '0': {'errorMessage': 'None'},
                '1': {'errorMessage': 'None'},
                '2': {'errorMessage': 'None'},
                '3': {'errorMessage': 'None'},
            }
        }
        self.assertEqual(expected, subItemDictionary)

    def test_prompt_Compile_ADD_LLM_Prediction(self):
        self.promptEngineer.setJavaFilePath('Module_LLM_PER/test/BatchFileTest/testFile/BREADTH_FIRST_SEARCH_TEST_99.java')
        self.promptEngineer.setPER_RepairTimes(1)
        self.promptEngineer.needCompileJavaFiles()
        self.promptEngineer.promptRepair_Compile()
        print(self.promptEngineer.LLM_Prediction())
        self.assertEqual(len(self.promptEngineer.getNeedCompileJavas()), 2)
        self.assertNotEqual(len(self.promptEngineer.getErrorMessage()), 0)



if __name__ == '__main__':
    unittest.main()