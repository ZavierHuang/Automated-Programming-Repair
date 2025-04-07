import re
import unittest

from Src_Module.src.LLM_CodeLlama import LLM_CodeLlama
from Src_Module.src.LLM_Qwen import LLM_Qwen
from Src_Module.src.Verification_HumanEval import Verification_HumanEval


class LLM_Model_Test(unittest.TestCase):
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



if __name__ == '__main__':
    unittest.main()