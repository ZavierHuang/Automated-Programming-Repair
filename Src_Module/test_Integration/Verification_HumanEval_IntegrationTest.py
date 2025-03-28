import unittest

from Src_Module.src.Verification_HumanEval import Verification_HumanEval
from Util_Module.src.FileIO import FileIO


class Verification_HumanEval_IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.verification_HumanEval = Verification_HumanEval()
        self.verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/HumanEval')
        self.fileIO = FileIO()

    def test_check_java_format_Pass(self):
        self.verification_HumanEval.junitEnvironment_Initialize()

        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)

        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        target_Pass = self.verification_HumanEval.getJunitEnvironmentPass() + '/Module_{}/{}.java'.format(buggyId, patchFileName)


        self.assertFalse(self.fileIO.isPathExist(target))
        self.assertTrue(self.fileIO.isPathExist(target_Pass))

    def test_check_java_forma_Failure(self):
        self.verification_HumanEval.junitEnvironment_Initialize()

        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_2'
        methodCode = """
        public static int add(int x,int y){
            return x + y
        }
        """

        self.verification_HumanEval.checkJavaFormat(methodCode, patchFileName, buggyId)

        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        target_Pass = self.verification_HumanEval.getJunitEnvironmentPass() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        self.assertTrue(self.fileIO.isPathExist(target))
        self.assertFalse(self.fileIO.isPathExist(target_Pass))


if __name__ == '__main__':
    unittest.main()