from Config import ROOT
from Src_Module.src.Verification import Verification


class Verification_HumanEval(Verification):
    def __init__(self):
        super().__init__()

    def checkJavaFormat(self, methodCode, patchFileName, buggyId):
        # ADD --> ADD_TEST_1
        methodCode = methodCode.replace(buggyId, patchFileName)

        # Add.txt
        remainderCode = super().readReaminderCode(self.getRemainderCodePath() + '/' + buggyId + '.txt')

        javaCode = super().createJavaValidCode(patchFileName, methodCode, remainderCode)

        # JUnit_Environment/HumanEval/Module_ADD/ADD_TEST_1.java
        target = super().getJunitEnvironment() + '/Module_{}/{}.java'.format(buggyId, patchFileName)

        super().fileIO.writeFileData(target, javaCode)









