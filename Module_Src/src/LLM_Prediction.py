# import json
# from typing import Optional
# from dataclasses import dataclass, field
# from pathlib import Path
#
# import torch
# from peft import PeftModel
# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
#     GenerationConfig,
#     HfArgumentParser,
#     BitsAndBytesConfig,
# )
# from tqdm import tqdm
#
#
# @dataclass
# class ModelArguments:
#     base_model_path: Optional[str] = field(default="null")
#     lora_path: Optional[str] = field(default="Error")
#     max_length: int = field(default=512, metadata={"help": "Maximum length of the input sequence."})
#
#
# @dataclass
# class DataArguments:
#     data_path: str = field(default=None, metadata={"help": "Path to the training data."})
#     test_file: str = field(default="test.json", metadata={"help": "Test file name."})
#     output_file: str = field(default=None, metadata={"help": "Output file name."})
#
#
# @dataclass
# class GenerationArguments:
#     max_new_tokens: int = field(
#         default=256,
#         metadata={"help": "Maximum number of new tokens to generate."},
#     )
#     is_lora: bool = field(default=True, metadata={"help": "Whether to use LORA."})
#     num_beams: int = field(default=1, metadata={"help": "Number of beams for beam search. 1 means no beam search."})
#     request_num: int = field(default=1, metadata={"help": "Number of requests."})
#     sub_request_num: int = field(default=10, metadata={"help": "Number of requests for each bug."})
#
#
# def main():
#     parser = HfArgumentParser((ModelArguments, DataArguments, GenerationArguments))
#     model_args, data_args, generation_args = parser.parse_args_into_dataclasses()
#
#     if generation_args.is_lora:
#         model = AutoModelForCausalLM.from_pretrained(
#             model_args.base_model_path,
#             torch_dtype=torch.float16,
#             load_in_8bit=True,
#             trust_remote_code=True,
#             quantization_config=BitsAndBytesConfig(
#                 load_in_8bit=True,
#                 llm_int8_threshold=6.0
#             ),
#         )
#
#         print("MODEL ARGS lora path:", model_args.lora_path)
#         print("MODEL ARGS base_model_path :", model_args.base_model_path)
#         model = PeftModel.from_pretrained(
#             model,
#             model_args.lora_path,
#             torch_dtype=torch.float16,
#         )
#     else:
#         model = AutoModelForCausalLM.from_pretrained(
#             model_args.base_model_path,
#             torch_dtype=torch.float16,
#         )
#     tokenizer = AutoTokenizer.from_pretrained(model_args.base_model_path, trust_remote_code=True)
#
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model.config.pad_token = tokenizer.pad_token = tokenizer.unk_token
#     model.to(device)
#
#     print("We now use beam search to generate the patches.")
#     generation_config = GenerationConfig(
#         num_beams=generation_args.num_beams,
#         num_beam_groups=generation_args.num_beams // 2,
#         diversity_penalty=0.8,
#         early_stopping=True,
#     )
#
#     buggy_code_list = []
#     llama2_output = []
#     data_path = Path(data_args.data_path)
#     with open(data_path / data_args.test_file, 'r', encoding='utf-8') as tf:
#         for sample in tf.readlines():
#             buggy_code_list.append(json.loads(sample))
#
#     for sample in tqdm(buggy_code_list, desc="Generating..."):
#         tmp_dict = {}
#         buggy_code = sample["buggy_code"]
#
#         inputs = tokenizer(buggy_code, return_tensors='pt')
#         inputs_len = inputs.input_ids.shape[1]
#         input_ids = inputs.input_ids.to(device)
#
#         try:
#             with torch.no_grad():
#                 outputs = model.generate(
#                     input_ids=input_ids,
#                     max_new_tokens=generation_args.max_new_tokens,
#                     num_return_sequences=generation_args.request_num,
#                     pad_token_id=tokenizer.pad_token_id,
#                     eos_token_id=tokenizer.eos_token_id,
#                     generation_config=generation_config,
#                 )
#         except Exception as e:
#             print(e)
#             print("The code sequence of bug {} is too long, {}.".format(sample['bug_id'], inputs_len))
#             continue
#         output_ids = outputs[:, inputs_len:]
#
#         output_diff = tokenizer.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
#         original_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False)
#
#         output_dict = {}
#
#         for i in range(len(output_diff)):
#             output_dict[i] = {
#                 "original_output": original_outputs[i],
#                 "output_patch": output_diff[i],
#             }
#
#         tmp_dict['bug_id'] = sample['bug_id']
#         tmp_dict['output'] = output_dict
#         tmp_dict['buggy_code'] = buggy_code
#         tmp_dict['gold_patch'] = sample['fixed_chunk']
#
#         llama2_output.append(tmp_dict)
#
#
#     print("output_file:", data_args.output_file)
#     with open(data_args.output_file, 'w') as pd_file:
#         for each in llama2_output:
#             pd_file.write(json.dumps(each))
#             pd_file.write('\n')
#
# if __name__ == "__main__":
#     main()
#
