import os
import unittest

from Src_Module.src.Verification import Verification
from Util_Module.src.FileIO import FileIO
from Config import ROOT


class Verification_Test(unittest.TestCase):
    def setUp(self):
        self.verification = Verification()
        self.fileIO = FileIO()

    def test_subprocess_run_JavaFormat_Pass(self):
        test_File = os.path.join(ROOT, 'Util_Module/test/javaFormatTestFile/javaFormatTestFile_Pass.java')
        result = self.verification.subprocess_run_JavaFormat(test_File)

        """
        CompletedProcess(args=['java', '-jar', \
        'F:\\GITHUB\\Automated-Programming-Repair/Tool/google-java-format-1.18.1-all-deps.jar', \
        '--replace', 'F:\\GITHUB\\Automated-Programming-Repair/Util_Module/test/javaFormatTestFile/javaFormatTestFile_Pass.java'], \
        returncode=0, stdout='', stderr='')
        """

        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stderr), 0)

    def test_subprocess_run_JavaFormat_Failure(self):
        test_File = os.path.join(ROOT, 'Util_Module/test/javaFormatTestFile/javaFormatTestFile_Failure.java')
        result = self.verification.subprocess_run_JavaFormat(test_File)

        """
        CompletedProcess(args=['java', '-jar', \
        'F:\\GITHUB\\Automated-Programming-Repair/Tool/google-java-format-1.18.1-all-deps.jar', \
        '--replace', 'F:\\GITHUB\\Automated-Programming-Repair/Util_Module/test/javaFormatTestFile/javaFormatTestFile_Failure.java'], \
        returncode=1, stdout='', \
        stderr="F:\\GITHUB\\Automated-Programming-Repair\\Util_Module\\test\\javaFormatTestFile\\javaFormatTestFile_Failure.java:5:14: \
        error: ';' expected\n")
        """

        self.assertEqual(result.returncode, 1)
        self.assertNotEqual(len(result.stderr), 0)

    def test_read_remainder_Code_with_Existed(self):
        buggyId = 'DECODE_SHIFT'
        remainderCodePath = os.path.join(ROOT, 'Data_Storage/HumanEval/RemainderCode' + '/' + buggyId + '.txt')
        readData = None

        if self.fileIO.isPathExist(remainderCodePath):
            readData = self.fileIO.readFileData(remainderCodePath)
            self.assertNotEqual(len(readData), 0)
        else:
            self.assertIsNone(readData)

    def test_read_remainder_Code_with_NonExisted(self):
        buggyId = 'ADD'
        remainderCodePath = os.path.join(ROOT, 'Data_Storage/HumanEval/RemainderCode' + '/' + buggyId + '.txt')
        readData = None

        if self.fileIO.isPathExist(remainderCodePath):
            readData = self.fileIO.readFileData(remainderCodePath)
            self.assertNotEqual(len(readData), 0)
        else:
            self.assertIsNone(readData)



if __name__ == '__main__':
    unittest.main()