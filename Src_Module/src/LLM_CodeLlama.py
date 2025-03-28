from overrides import overrides

from Src_Module.src.LLM_Model import LLM_Model


class LLM_CodeLlama(LLM_Model):
    def __init__(self):
        super().__init__()

    @overrides
    def patchReplaceByModel(self, buggyCode, patchCode):
        patchCode = patchCode.replace('</s>', '').strip()
        return buggyCode.replace('<FILL_ME>', patchCode, 1)


