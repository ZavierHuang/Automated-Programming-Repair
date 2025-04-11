from overrides import overrides

from Module_Src.src.LLM_Model import LLM_Model


class LLM_Qwen(LLM_Model):
    def __init__(self):
        super().__init__()

    @overrides
    def patchReplaceByModel(self, buggyCode, patchCode):
        PREFIX = '<|fim_prefix|>'
        MIDDLE = '<|fim_middle|>'
        SUFFIX = '<|fim_suffix|>'

        patchCode = patchCode.replace('</s>', '').strip()
        patchCode = buggyCode.replace(SUFFIX, patchCode, 1)
        patchCode = patchCode.replace(PREFIX, '')
        fixedCode = patchCode.replace(patchCode[patchCode.find(MIDDLE):], '')

        return fixedCode

