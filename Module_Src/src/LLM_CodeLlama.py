import os

from overrides import overrides

from Config import ROOT, LLM_MODEL_PATH
from Module_Src.src.LLM_Model import LLM_Model


class LLM_CodeLlama(LLM_Model):
    def __init__(self):
        super().__init__()
        self.name = "CodeLlama"
        self.baseModelPath = "TheBloke/CodeLlama-7B-fp16"

    @overrides
    def patchReplaceByModel(self, buggyCode, patchCode):
        patchCode = patchCode.replace('</s>', '').strip()
        return buggyCode.replace('<FILL_ME>', patchCode, 1)

    @overrides
    def remarkErrorPosition(self, buggyCode):
        return buggyCode.replace('// buggy code', '', 1)
