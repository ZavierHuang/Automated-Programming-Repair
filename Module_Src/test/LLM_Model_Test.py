import os
import re
import unittest

from Config import LLM_MODEL_PATH
from Module_Src.src.LLM_CodeLlama import LLM_CodeLlama
from Module_Src.src.LLM_Qwen import LLM_Qwen
from Module_Src.src.Verification_HumanEval import Verification_HumanEval
from Module_Util.src.FileIO import FileIO


class LLM_Model_Test(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.fileIO = FileIO()

    def setUp(self):
        self.model_CodeLlama = LLM_CodeLlama()
        self.model_Qwen = LLM_Qwen()
        self.dataset_HumanEval = Verification_HumanEval()

    def normalize(self, text):
        # Replace all symbols other than numbers and letters with empty
        return re.sub(r'[^A-Za-z0-9]', '', text)


    def test_patchCode_Replace_With_CodeLlama(self):
        patchCode = '</s>  return x+y;  '
        buggyCode = """
        public static int add(int x, int y) {
            // buggy code
            // return x | y;
            <FILL_ME>
        }
       """
        fixedCode = """
        public static int add(int x, int y) {
            // buggy code
            // return x | y;
            return x+y;
        }
        """
        result = self.model_CodeLlama.patchReplaceByModel(buggyCode, patchCode)

        self.assertEqual(self.normalize(result), self.normalize(fixedCode))

    def test_patchCode_Replace_With_Qwen(self):
        patchCode = '</s>  return x+y;  '
        buggyCode = """
        <|fim_prefix|>public static int add(int x, int y) {
            <|fim_suffix|>
        }
        <|fim_middle|>
        // buggy code
        //return x | y;
       """

        fixedCode = """
        public static int add(int x, int y) {
            return x+y;
        }
        """
        result = self.model_Qwen.patchReplaceByModel(buggyCode, patchCode)

        self.assertEqual(self.normalize(result), self.normalize(fixedCode))

    def test_check_GPU(self):
        model_Qwen = LLM_Qwen()
        model_Qwen.checkGUP()

    def test_create_patch_code(self):
        model_Qwen = LLM_Qwen()
        self.assertTrue(model_Qwen.checkGUP())
        model_Qwen.setIsLora(True)
        model_Qwen.setLoraAndEpoch('Lora04', 2)
        model_Qwen.setNumBeams(10)
        model_Qwen.setDiversity(0)
        model_Qwen.setDataSourceFilePath('Module_Src/test/tempPatchGenerate/Qwen_test_Multiple.jsonl')
        model_Qwen.setResultOutputFilePath('Module_Src/test/tempPatchGenerate/Qwen_test_Multiple_output.jsonl')

        self.assertEqual(model_Qwen.getBaseModelPath(), 'Qwen/Qwen2.5-Coder-1.5B')
        self.assertEqual(model_Qwen.getLoraPath(), os.path.join(LLM_MODEL_PATH, 'model_Qwen/model_Lora04/checkpoint-epoch-2.0'))

        model_Qwen.llmPredictPatch()

        self.assertTrue(self.fileIO.isPathExist(model_Qwen.getResultOutputFilePath()))

if __name__ == '__main__':
    unittest.main()