import os
from overrides import overrides

from Config import GRADLE_PATH
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
    def createJsonFramework(self):
        data = self.jsonFileIO.readJsonLineData(self.getTestData())
        dictionary = []

        for item in data:
            buggyId = item['bug_id']
            buggyCode = item['buggy_code']
            output = item['output']
            solution = item['gold_patch']
            subdictionary = {'output': {}}
            for i in range(len(output)):
                patchFileName = '{}_TEST_{}'.format(buggyId, str(i))
                patchCode = output[str(i)]['output_patch']
                target = os.path.join(self.getJunitEnvironment(),
                                      'Module_{}/{}.java'.format(buggyId, patchFileName))
                targetModule = os.path.join(self.getJunitModuleTestEnvironment(),
                                            'Module_{}/src/main/java/{}.java'.format(buggyId, patchFileName))

                methodCode = self.model_CodeLlama.patchReplaceByModel(buggyCode, patchCode)

                javaFormatLog, javaFormatResult = self.checkJavaFormat(methodCode, patchFileName, buggyId)
                compileLog, compileResult = self.checkJavaCompile(target, javaFormatResult)

                print(compileResult, compileLog)
                self.fileIO.moveFile(target, targetModule, compileResult)

                subdictionary['output'][i] = (
                    self.jsonFileIO.getJsonResultSubItem(
                        patchCode, compileLog, compileResult,
                        javaFormatLog, javaFormatResult, solution))

            dictionary.append(subdictionary)

        self.jsonFileIO.writeJsonFile(dictionary, self.getJsonResultPath())

    @overrides
    def runScriptBatchFile(self, directory):
        for item in directory.items():
            newName = item[0] + '.'                     # ADD_TEST_9.
            oldName = item[1] + '.'                     # ADD.
            moduleName = 'Module_{}'.format(item[1])
            testFilePath = os.path.join(
                self.getJunitModuleTestEnvironment(),
                "{}/src/test/java/{}_TEST.java".format(moduleName, item[1])
            )
            self.fileIO.replaceName(testFilePath, oldName, newName)
            self.runScriptSingleFile(item[0], moduleName)
            self.fileIO.replaceName(testFilePath, newName, oldName)

    @overrides
    def runScriptSingleFile(self, patchFileName, moduleName):
        # params = [testModuleName, programFileName, logFolder, gradlePath, junitModuleEnvironment]

        #patchFileName = ADD_ELEMENTS_TEST_4
        #moduleName = Module_ADD_ELEMENTS

        print('run ', patchFileName)

        params = [
            moduleName,
            patchFileName,
            self.getLogFolderPath(),
            GRADLE_PATH,
            self.getJunitModuleTestEnvironment()
        ]
        self.runBashScript(params)