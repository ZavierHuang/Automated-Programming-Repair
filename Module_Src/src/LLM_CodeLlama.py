from overrides import overrides

from Module_Src.src.LLM_Model import LLM_Model


class LLM_CodeLlama(LLM_Model):
    def __init__(self):
        super().__init__()
        self.name = "CodeLlama"

    @overrides
    def patchReplaceByModel(self, buggyCode, patchCode):
        patchCode = patchCode.replace('</s>', '').strip()
        return buggyCode.replace('<FILL_ME>', patchCode, 1)

    @overrides
    def remarkErrorPosition(self, buggyCode):
        return buggyCode.replace('// buggy code', '', 1)
