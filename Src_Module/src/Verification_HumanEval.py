import os
import shutil

from overrides import overrides

from Config import ROOT
from Src_Module.src.Verification import Verification


class Verification_HumanEval(Verification):
    def __init__(self):
        super().__init__()

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
    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        # ADD --> ADD_TEST_1
        methodCode = methodCode.replace(buggyId, patchFileName)

        # Add.txt
        remainderCode = self.readRemainderCode(os.path.join(self.getRemainderCodePath(), buggyId + '.txt'))

        importContent = self.getImportContent(buggyId)

        javaCode = self.createJavaValidCode(patchFileName, methodCode, remainderCode, importContent)

        target = self.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        self.fileIO.writeFileData(target, javaCode)

        result = self.subprocess_run_JavaFormat(target)

        return result, result.returncode == 0

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
                return result, True
            return result, False
        return result, True


