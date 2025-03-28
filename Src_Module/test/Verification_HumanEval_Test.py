import os
import re
import unittest

from Config import ROOT
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

        javaCode = f"""
        public class ADD_TEST_1 {{
        public static int add(int x,int y){{
            return x + y;
        }}
        }}
        """

        self.verification_HumanEval.junitEnvironment_Initialize(self.verification_HumanEval.getJunitEnvironmentPass())
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getJunitEnvironmentPass())), 0)

        self.verification_HumanEval.junitEnvironment_Initialize(self.verification_HumanEval.getJunitEnvironmentFailure())
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getJunitEnvironmentFailure())), 0)


        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format('Add', 'Add_TEST_1')
        if self.fileIO.isPathExist(target):
            self.fileIO.deleteFileData(target)

        self.fileIO.writeFileData(target, javaCode)
        self.assertTrue(self.fileIO.isPathExist(target))

        readData = self.fileIO.readFileData(target)
        self.assertEqual(self.normalize(readData), self.normalize(javaCode))

    def test_check_java_format_Pass(self):
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/HumanEval')
        self.verification_HumanEval.setGoogleJavaFormat('Tool/google-java-format-1.18.1-all-deps.jar')
        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format('Add', 'Add_TEST_1')
        result = self.verification_HumanEval.subprocess_run_JavaFormat(target)

        self.assertEqual(result.returncode, 0)





if __name__ == '__main__':
    unittest.main()