import unittest

from Src_Module.src.Verification import Verification
from Util_Module.src.FileIO import FileIO
from Config import ROOT


class Verification_Test(unittest.TestCase):
    def setUp(self):
        self.verification = Verification()
        self.fileIO = FileIO()

    def test_subprocess_run_JavaFormat_Pass(self):
        test_File = ROOT + 'Util_Module/test/tempFile/javaFormatTestFile_Pass.java'
        result = self.verification.subprocess_run_JavaFormat(test_File)

        """
        CompletedProcess(args=['java', '-jar', \
        'F:\\GITHUB\\Automated-Programming-Repair/Tool/google-java-format-1.18.1-all-deps.jar', \
        '--replace', 'F:\\GITHUB\\Automated-Programming-Repair/Util_Module/test/tempFile/javaFormatTestFile_Pass.java'], \
        returncode=0, stdout='', stderr='')
        """

        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stderr), 0)

    def test_subprocess_run_JavaFormat_Failure(self):
        test_File = ROOT + 'Util_Module/test/tempFile/javaFormatTestFile_Failure.java'
        result = self.verification.subprocess_run_JavaFormat(test_File)

        """
        CompletedProcess(args=['java', '-jar', \
        'F:\\GITHUB\\Automated-Programming-Repair/Tool/google-java-format-1.18.1-all-deps.jar', \
        '--replace', 'F:\\GITHUB\\Automated-Programming-Repair/Util_Module/test/tempFile/javaFormatTestFile_Failure.java'], \
        returncode=1, stdout='', \
        stderr="F:\\GITHUB\\Automated-Programming-Repair\\Util_Module\\test\\tempFile\\javaFormatTestFile_Failure.java:5:14: \
        error: ';' expected\n")
        """

        self.assertEqual(result.returncode, 1)
        self.assertNotEqual(len(result.stderr), 0)



if __name__ == '__main__':
    unittest.main()