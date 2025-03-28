import re
import unittest

from Src_Module.src.Verification import Verification
from Src_Module.src.Verification_HumanEval import Verification_HumanEval
from Util_Module.src.FileIO import FileIO


class Verification_HumanEval_Test(unittest.TestCase):
    def setUp(self):
        self.verification = Verification()
        self.verification_HumanEval = Verification_HumanEval()
        self.fileIO = FileIO()

    def normalize(self, text):
        # Replace all symbols other than numbers and letters with spaces
        return re.sub(r'[^A-Za-z0-9]', '', text)


    def test_create_Valid_Java_Code(self):
        self.verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')

        buggyId = 'ADD'
        remainderCodeFilePath = self.verification_HumanEval.remainCodePath + '/' + buggyId + '.txt'

        patchFileName = 'ADD_TEST_1'

        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        remainderCode = self.verification.readReaminderCode(remainderCodeFilePath)

        completedJavaCode = f"""
        public class {patchFileName} {{
            {methodCode}
            {remainderCode}
        }}
        """

        expectedResult = f"""
        public class 'ADD_TEST_1' {{
            public static int add(int x,int y){{
                return x + y;
            }}
        }}
        """

        self.assertEqual(self.normalize(completedJavaCode), self.normalize(expectedResult))


    def test_write_data_in_junit_environment(self):
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/HumanEval')
        self.verification_HumanEval.setGoogleJavaFormat('Tool/google-java-format-1.18.1-all-deps.jar')

        javaCode = f"""
        public class 'ADD_TEST_1' {{
        public static int add(int x,int y){{
            return x + y;
        }}
        }}
        """

        target = self.verification_HumanEval.getJunitEnvironment() + '/Module_{}/{}.java'.format('Add', 'Add_Test_1')
        self.fileIO.writeFileData(target, javaCode)
        self.assertTrue(self.fileIO.isFileExist(target))

        readData = self.fileIO.readFileData(target)
        self.assertEqual(self.normalize(readData), self.normalize(javaCode))

        self.fileIO.deleteFileData(target)
        self.assertFalse(self.fileIO.isFileExist(target))

if __name__ == '__main__':
    unittest.main()