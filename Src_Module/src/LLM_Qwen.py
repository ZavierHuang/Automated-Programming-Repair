from Src_Module.src.LLM_Model import LLM_Model


class LLM_Qwen(LLM_Model):
    def __init__(self):
        super().__init__()

    def patchReplaceByModel(self, buggyCode, patchCode):
        PREFIX = '<｜fim▁begin｜>'
        MIDDLE = '<｜fim▁hole｜>'
        SUFFIX = '<｜fim▁end｜>'

        patchCode = patchCode.replace('</s>', '').strip()
        patchCode = buggyCode.replace(MIDDLE, patchCode, 1)
        patchCode = patchCode.replace(PREFIX, '')
        fixedCode = patchCode.replace(patchCode[patchCode.find(SUFFIX):], '')

        return fixedCode

