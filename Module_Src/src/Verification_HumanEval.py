import os

from openpyxl.packaging.manifest import Override
from overrides import overrides

from Config import GRADLE_PATH
from Module_Src.src.Verification import Verification


class Verification_HumanEval(Verification):
    def __init__(self):
        super().__init__()

    @overrides
    def junitEnvironment_Run_Initialize(self):
        super().junitEnvironment_Run_Initialize()

    @overrides
    def getImportContent(self, buggyId):
        importContent = 'import java.util.*;'
        importDict = {
            'ISCUBE': [
                'import java.math.BigDecimal;',
                'import java.math.RoundingMode;'
            ],

            'TRIANGLE_AREA_2': [
                'import java.math.BigDecimal;',
                'import java.math.RoundingMode;'
            ],

            'DO_ALGEBRA': [
                'import javax.script.ScriptEngine;',
                'import javax.script.ScriptEngineManager;',
                'import javax.script.ScriptException;'
            ],
            'STRING_TO_MD5': [
                'import javax.xml.bind.DatatypeConverter;',
                'import java.security.MessageDigest;',
                'import java.security.NoSuchAlgorithmException;'
            ]
        }

        if buggyId in importDict.keys():
            importContent = importContent + '\n' +  ('\n'.join(importDict[buggyId]))

        return importContent

    @overrides
    def createJavaValidCode(self,patchFileName, methodCode, remainderCode, importContent):
        if 'DECODE_CYCLIC' in patchFileName:
            javaCode = f"""
                {importContent}
                public class {patchFileName} {{
                    public static String decode_cyclic(String str) {{
                        class Cyclic{{
                            {methodCode}
                        }}
                        {remainderCode}
                    }}
                }}
                """
            return javaCode

        if 'SORT_ARRAY_BINARY' in patchFileName:
            javaCode = f"""
                {importContent}
                public class {patchFileName} {{
                    Collections.sort(arr, new Comparator<Integer>() {{
                        @Override
                        {methodCode}
                    }}
                    {remainderCode}
                }}
                """
            return javaCode

        return super().createJavaValidCode(patchFileName, methodCode, remainderCode, importContent)

    @overrides
    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        # ADD --> ADD_TEST_1
        methodCode = methodCode.replace(buggyId, patchFileName)

        # Add.txt
        remainderCode = self.readRemainderCode(os.path.join(self.getRemainderCodePath(), buggyId + '.txt'))

        importContent = self.getImportContent(buggyId)

        javaCode = self.createJavaValidCode(patchFileName, methodCode, remainderCode, importContent)

        target = self.getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        self.fileIO.writeFileData(target, javaCode)

        result = self.subprocess_run_JavaFormat(target)

        return result.stderr, result.returncode == 0

    @overrides
    def getNeedCompileJavaFiles(self, javaFile):
        return [javaFile]

    @overrides
    def checkJavaCompile(self, javaFile, javaFormatResult):
        if javaFormatResult is False:
            return 'FormatError', False

        javaFiles = self.getNeedCompileJavaFiles(javaFile)
        result = self.subprocess_run_JavaCompile(javaFiles)

        if result.returncode != 0:
            if ('STRING_TO_MD5' in result.stderr and
                'error: cannot find symbol' in result.stderr and
                'symbol:   variable DatatypeConverter' in result.stderr):
                return '', True
            return result.stderr, False
        return result.stderr, True

    @overrides
    def updateJsonResult(self):
        fileList = self.fileIO.getFileListUnderFolder(self.getLogFolderPath())
        data = self.jsonFileIO.readJsonData(self.getJsonResultPath())

        for file in fileList:
            buggyId = file[:file.find('_TEST')]                                     # ADD_TEST_0.txt --> ADD
            sequence = file[file.find('_TEST_') + len('_TEST_'):-4]                 # ADD_TEST_0.txt --> 0
            logContent = self.fileIO.readFileData(os.path.join(self.getLogFolderPath(), file))
            print(buggyId, sequence, 'BUILD SUCCESSFUL' in logContent)
            if 'BUILD SUCCESSFUL' in logContent:
                for item in data:
                    if item['buggyId'] == buggyId:
                        item['repair'] = True
                        item['output'][str(sequence)]['PassTestCase'] = True
                        break

        self.jsonFileIO.writeJsonFile(data, self.getJsonResultPath())