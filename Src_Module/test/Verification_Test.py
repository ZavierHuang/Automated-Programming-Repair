import os
import shutil
import subprocess
import unittest

from Src_Module.src.Verification import Verification
from Util_Module.src.FileIO import FileIO
from Config import ROOT, CACHE_PATH


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

    def test_subprocess_run_JavaCompile_Pass(self):
        filePath = os.path.join(ROOT, 'Util_Module/test/compileCheckTestFile/compilePass.java')
        javaFiles = [filePath]
        result = self.verification.subprocess_run_JavaCompile(javaFiles)

        """
        CompletedProcess(args=['javac', '-d', \
        'F:\\GITHUB\\Automated-Programming-Repair\\cache/class_file', \
        'F:\\GITHUB\\Automated-Programming-Repair\\Util_Module/test/compileCheckTestFile/compilePass.java'], \
        returncode=0, stdout='', stderr='')
        """

        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stderr), 0)

    def test_subprocess_run_JavaCompile_Failure(self):
        filePath = os.path.join(ROOT, 'Util_Module/test/compileCheckTestFile/compileFailure.java')
        javaFiles = [filePath]
        result = self.verification.subprocess_run_JavaCompile(javaFiles)

        """
        CompletedProcess(args=['javac', '-d', \
        'F:\\GITHUB\\Automated-Programming-Repair\\cache/class_file', \
        'F:\\GITHUB\\Automated-Programming-Repair\\Util_Module/test/compileCheckTestFile/compileFailure.java'], \
        returncode=1, stdout='', \
        stderr='F:\\GITHUB\\Automated-Programming-Repair\\Util_Module\\test\\compileCheckTestFile\\compileFailure.java:\
        1: error: class errorName is public, should be declared in a file named errorName.java\npublic class errorName{\n       ^\n1 error\n')
        """

        self.assertEqual(result.returncode, 1)
        self.assertNotEqual(len(result.stderr), 0)

    def test_clear_run_test_case_module_folder(self):
        junitModuleTestEnvironment = os.path.join(ROOT, 'Util_Module/test/moduleTestFolder')
        os.makedirs(junitModuleTestEnvironment, exist_ok=True)
        self.fileIO.writeFileData(os.path.join(junitModuleTestEnvironment, 'Module_ADD/src/main/java/test1.java'), '')

        subFolderList = self.fileIO.getSubFolderList(junitModuleTestEnvironment)
        sub_Module_Folder_List = [subFolder for subFolder in subFolderList if 'Module_' in subFolder]

        for subModuleFolderPath in sub_Module_Folder_List:
            # F:\\GITHUB\\Automated-Programming-Repair\\Util_Module/test/moduleTestFolder\\Module_ADD
            self.fileIO.deleteSubFolderAndCreate(subModuleFolderPath, [os.path.join(subModuleFolderPath, 'src/main/java')])
            self.assertEqual(self.fileIO.getFileListUnderFolder(os.path.join(subModuleFolderPath, 'src/main/java')), [])

        shutil.rmtree(junitModuleTestEnvironment)



if __name__ == '__main__':
    unittest.main()