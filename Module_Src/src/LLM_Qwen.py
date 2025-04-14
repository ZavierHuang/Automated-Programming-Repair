import os

from overrides import overrides

from Config import ROOT, LLM_MODEL_PATH
from Module_Src.src.LLM_Model import LLM_Model


class LLM_Qwen(LLM_Model):
    def __init__(self):
        super().__init__()
        self.name = 'Qwen'
        self.baseModelPath = 'Qwen/Qwen2.5-Coder-1.5B'

    @overrides
    def setLoraAndEpoch(self, lora, epoch):
        self.loraPath = os.path.join(LLM_MODEL_PATH, 'model_Qwen/model_{}/checkpoint-epoch-{}.0'.format(lora,epoch))

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

    @overrides
    def remarkErrorPosition(self, buggyCode):
        errorPart = buggyCode[buggyCode.find('// buggy code') + len('// buggy code'):buggyCode.find('// fill')]

        PREFIX = '<|fim_prefix|>'
        MIDDLE = '<|fim_middle|>'
        SUFFIX = '<|fim_suffix|>'

        buggyCode = buggyCode.replace('// buggy code', SUFFIX)
        buggyCode = buggyCode.replace('// fill', '')

        twiceBuggyCode = f"""
        {PREFIX}{buggyCode}
        {MIDDLE}
        // buggy code
        {errorPart}
        """

        return twiceBuggyCode
