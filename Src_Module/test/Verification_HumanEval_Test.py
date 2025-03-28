import os
import re
import shutil
import subprocess
import unittest

from Config import ROOT, CACHE_PATH
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

    def test_get_Import_Content(self):
        buggyId = 'ADD'
        expected = 'import java.util.*;'
        self.assertEqual(self.verification_HumanEval.getImportContent(buggyId), expected)

        buggyId = 'ISCUBE'
        expected = 'import java.util.*;\nimport java.math.BigDecimal;\nimport java.math.RoundingMode;'
        self.assertEqual(self.verification_HumanEval.getImportContent(buggyId), expected)

    def test_create_Valid_Java_Code(self):
        self.verification_HumanEval.setRemainderCodePath('Data_Storage/HumanEval/RemainderCode')

        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        remainderCodeFilePath = self.verification_HumanEval.remainCodePath + '/' + buggyId + '.txt'

        methodCode = """
        public static int add(int x,int y){
            return x + y;
        }
        """

        remainderCode = self.verification.readReaminderCode(remainderCodeFilePath)
        importContent = self.verification_HumanEval.getImportContent(buggyId)

        completedJavaCode = f"""
        {importContent}
        public class {patchFileName} {{
            {methodCode}
            {remainderCode}
        }}
        """

        expectedResult = f"""
        import java.util.*;
        public class ADD_TEST_1 {{
            public static int add(int x,int y){{
                return x + y;
            }}
        }}
        """

        self.assertEqual(self.normalize(completedJavaCode), self.normalize(expectedResult))

    def test_1_junit_initialize(self):
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/HumanEval')
        self.verification_HumanEval.junitEnvironment_Clear(self.verification_HumanEval.getJunitEnvironmentPass())
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getJunitEnvironmentPass())),0)

        self.verification_HumanEval.junitEnvironment_Clear(self.verification_HumanEval.getJunitEnvironmentFailure())
        self.assertEqual(len(self.fileIO.getFileListUnderFolder(self.verification_HumanEval.getJunitEnvironmentFailure())), 0)

    def test_2_write_data_in_junit_environment(self):
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/HumanEval')

        javaCode = f"""
        import java.util.*;
        public class ADD_TEST_1 {{
        public static int add(int x,int y){{
            return x + y;
        }}
        }}
        """

        self.verification_HumanEval.junitEnvironment_Initialize()

        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format('Add', 'Add_TEST_1')
        if self.fileIO.isPathExist(target):
            self.fileIO.deleteFileData(target)

        self.fileIO.writeFileData(target, javaCode)
        self.assertTrue(self.fileIO.isPathExist(target))

        readData = self.fileIO.readFileData(target)
        self.assertEqual(self.normalize(readData), self.normalize(javaCode))

    def test_3_check_java_format_Pass(self):
        buggyId = 'ADD'
        patchFileName = 'ADD_TEST_1'
        self.verification_HumanEval.setJunitEnvironment('JUnit_Environment/HumanEval')
        self.verification_HumanEval.setGoogleJavaFormat('Tool/google-java-format-1.18.1-all-deps.jar')
        target = self.verification_HumanEval.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        result = self.verification_HumanEval.subprocess_run_JavaFormat(target)

        self.assertEqual(result.returncode, 0)
        target_pass = self.verification_HumanEval.getJunitEnvironmentPass() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
        shutil.move(target, target_pass)

        self.assertFalse(self.fileIO.isPathExist(target))
        self.assertTrue(self.fileIO.isPathExist(target_pass))

    def test_check_STRING_TO_MD5_Compile(self):
        javaFile = os.path.join(ROOT, 'Util_Module/test/compileCheckTestFile/STRING_TO_MD5.java')
        result = self.verification_HumanEval.checkJavaCompile(javaFile)

        """
        CompletedProcess(args=['javac', '-d', \
        'F:\\GITHUB\\Automated-Programming-Repair\\cache/class_file', \
        'F:\\GITHUB\\Automated-Programming-Repair\\Util_Module/test/compileCheckTestFile/STRING_TO_MD5.java'], \
        returncode=1,
        stdout='',
        stderr='F:\\GITHUB\\Automated-Programming-Repair\\Util_Module\\test\\compileCheckTestFile\\STRING_TO_MD5.java:\
        3: error: package javax.xml.bind does not exist\nimport javax.xml.bind.DatatypeConverter;\n                     ^\n
        F:\\GITHUB\\Automated-Programming-Repair\\Util_Module\\test\\compileCheckTestFile\\STRING_TO_MD5.java:12: error: cannot find symbol\n
        return DatatypeConverter.printHexBinary(digest).toLowerCase();\n               ^\n
        symbol:   variable DatatypeConverter\n
        location: class STRING_TO_MD5\n2 errors\n')
        """

        self.assertTrue(result)




if __name__ == '__main__':
    unittest.main()