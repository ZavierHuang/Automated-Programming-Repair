import os
import shutil

from Config import ROOT
from Src_Module.src.Verification import Verification


class Verification_HumanEval(Verification):
    def __init__(self):
        super().__init__()

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

    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        # ADD --> ADD_TEST_1
        methodCode = methodCode.replace(buggyId, patchFileName)

        # Add.txt
        remainderCode = self.readReaminderCode(os.path.join(self.getRemainderCodePath(), buggyId + '.txt'))

        importContent = self.getImportContent(buggyId)

        javaCode = self.createJavaValidCode(patchFileName, methodCode, remainderCode, importContent)

        target = self.getJunitEnvironmentFailure() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        self.fileIO.writeFileData(target, javaCode)

        result = self.subprocess_run_JavaFormat(target)

        if result.returncode == 0:
            target_pass = self.getJunitEnvironmentPass() + '/Module_{}/{}.java'.format(buggyId, patchFileName)
            shutil.move(target, target_pass)
