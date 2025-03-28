from Src_Module.src.Verification import Verification


class Verification_HumanEval(Verification):
    def __init__(self, remainCodePath):
        super().__init__()
        self.remainCodePath = remainCodePath



    # def checkJavaFormat(self, methodCode, patchFileName, buggyId):
    #     # ADD --> ADD_TEST_1
    #     methodCode = methodCode.replace(buggyId, patchFileName)
    #
    #     # Add.txt
    #     remainderCode = super().readReaminderCode(self.remainCodePath + '/' + buggyId + '.txt')
    #
    #     javaCode = self.addClassOutSide(patchFileName, methodCode, remainderCode)
    #


