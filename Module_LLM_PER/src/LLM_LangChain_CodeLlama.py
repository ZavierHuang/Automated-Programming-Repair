# Prompt Engineering Repair
from Module_LLM_PER.src.LLM_PER import LLM_PER


class LLM_LangChain_CodeLlama(LLM_PER):
    def __init__(self):
        super().__init__()
        self.langChainName = 'codeLlama:7b-instruct'


