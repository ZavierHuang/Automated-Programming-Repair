import json
import os

import torch
from peft import PeftModel
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    GenerationConfig,
    BitsAndBytesConfig,
)
from tqdm import tqdm

import torch

from Config import ROOT


class LLM_Model:
    def __init__(self):
        self.name = None
        self.isLora = None
        self.lora = None
        self.loraPath = None
        self.baseModelPath = None
        self.numBeams = None
        self.diversity = None

        self.dataSourceFilePath = None
        self.resultOutputFilePath = None

    def setLLMName(self, name):
        self.name = name

    def setIsLora(self, isLora):
        self.isLora = isLora

    def setLoraAndEpoch(self, lora, epoch):
        pass

    def setBaseModelPath(self, baseModelPath):
        self.setBaseModelPath(baseModelPath)

    def setNumBeams(self, numBeams):
        self.numBeams = numBeams

    def setDiversity(self, diversity):
        self.diversity = diversity

    def setDataSourceFilePath(self, dataSourceFilePath):
        self.dataSourceFilePath = os.path.join(ROOT, dataSourceFilePath)

    def setResultOutputFilePath(self, resultOutputFilePath):
        self.resultOutputFilePath = os.path.join(ROOT, resultOutputFilePath)

    def getLLMName(self):
        return self.name

    def getIsLora(self):
        return self.isLora

    def getLoraPath(self):
        return self.loraPath

    def getBaseModelPath(self):
        return self.baseModelPath

    def getNumBeams(self):
        return self.numBeams

    def getDiversity(self):
        return self.diversity

    def getDataSourceFilePath(self):
        return self.dataSourceFilePath

    def getResultOutputFilePath(self):
        return self.resultOutputFilePath


    def patchReplaceByModel(self, buggyCode, patchCode):
       pass

    def remarkErrorPosition(self, buggyCode):
        pass

    def getLLMModel(self):
        if self.isLora is True:
            model = AutoModelForCausalLM.from_pretrained(
                self.baseModelPath,
                torch_dtype=torch.float16,
                trust_remote_code=True,
                quantization_config=BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_threshold=6.0
                ),
            )
            model = PeftModel.from_pretrained(
                model,
                self.loraPath,
                torch_dtype=torch.float16,
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                self.baseModelPath,
                torch_dtype=torch.float16,
            )
        return model

    def checkGUP(self):
        print("PyTorch Version:", torch.__version__)
        print("CUDA Available:", torch.cuda.is_available())
        if torch.cuda.is_available():
            print("Device Name:", torch.cuda.get_device_name(0))
            print("CUDA Version:", torch.version.cuda)
        return torch.cuda.is_available()

    def llmPredictPatch(self):
        model = self.getLLMModel()
        tokenizer = AutoTokenizer.from_pretrained(self.baseModelPath, trust_remote_code=True)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.config.pad_token = tokenizer.pad_token = tokenizer.unk_token
        model.to(device)

        print('device:',device)

        print("We now use beam search to generate the patches.")
        if self.diversity != 0:
            generation_config = GenerationConfig(
                num_beams = self.numBeams,
                num_beam_groups = self.numBeams // 2,
                diversity_penalty = self.diversity,
                early_stopping = True,
            )
        else:
            generation_config = GenerationConfig(
                num_beams=self.numBeams,
                early_stopping=True,
            )
        buggy_code_list = []
        llama2_output = []
        with open(self.dataSourceFilePath, 'r', encoding='utf-8') as tf:
            for sample in tf.readlines():
                buggy_code_list.append(json.loads(sample))

        for sample in tqdm(buggy_code_list, desc="Generating..."):
            tmp_dict = {}
            buggy_code = sample["buggy_code"]

            inputs = tokenizer(buggy_code, return_tensors='pt')
            inputs_len = inputs.input_ids.shape[1]
            input_ids = inputs.input_ids.to(device)

            try:
                with torch.no_grad():
                    outputs = model.generate(
                        input_ids=input_ids,
                        max_new_tokens=256,
                        num_return_sequences=self.numBeams,
                        pad_token_id=tokenizer.pad_token_id,
                        eos_token_id=tokenizer.eos_token_id,
                        generation_config=generation_config,
                    )
            except Exception as e:
                print(e)
                print("The code sequence of bug {} is too long, {}.".format(sample['bug_id'], inputs_len))
                continue

            output_ids = outputs[:, inputs_len:]
            output_diff = tokenizer.batch_decode(output_ids, skip_special_tokens=True,
                                                 clean_up_tokenization_spaces=False)
            original_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True,
                                                      clean_up_tokenization_spaces=False)

            output_dict = {}

            for i in range(len(output_diff)):
                output_dict[i] = {
                    "original_output": original_outputs[i],
                    "output_patch": output_diff[i],
                }

            tmp_dict['bug_id'] = sample['bug_id']
            tmp_dict['output'] = output_dict
            tmp_dict['buggy_code'] = buggy_code
            tmp_dict['gold_patch'] = sample['fixed_chunk']

            llama2_output.append(tmp_dict)

        print("output_file:", self.resultOutputFilePath)
        with open(self.resultOutputFilePath, 'w') as pd_file:
            for each in llama2_output:
                pd_file.write(json.dumps(each))
                pd_file.write('\n')