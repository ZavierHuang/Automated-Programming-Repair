#!/bin/bash
echo "Run Start..."
echo "========== Qwen Lora 04 - Epoch 05 - Patch 01 =========="
C:/Users/islab/anaconda3/envs/tensorflow_env/python.exe f:/My_APR/Experiment_CodeLlama/repairllama/src/lora/llama_pred_utf-8.py ^
--do_sample True ^
--only_do_beam True ^
--only_do_topp False ^
--only_do_topk False ^
--only_do_temp False ^
--temperature 0.8 ^
--top_k 0 ^
--top_p 0.95 ^
--num_beams 1 ^
--request_num 1 ^
--data_path F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval ^
--test_file HumanEvalPrograms_Qwen_IR4OR2.jsonl ^
--output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Result_Qwen/HumanEval_Qwen_Lora04_E5_Patch01.jsonl ^
--is_lora True ^
--lora_path F:/My_APR/Experiment_CodeLlama/repairllama/model_Qwen/model_Lora04/checkpoint-epoch-5.0/ ^
--base_model_path Qwen/Qwen2.5-Coder-1.5B

echo "========== Qwen Lora 04 - Epoch 05 - Patch 05 =========="
C:/Users/islab/anaconda3/envs/tensorflow_env/python.exe f:/My_APR/Experiment_CodeLlama/repairllama/src/lora/llama_pred_utf-8.py ^
--do_sample True ^
--only_do_beam True ^
--only_do_topp False ^
--only_do_topk False ^
--only_do_temp False ^
--temperature 0.8 ^
--top_k 0 ^
--top_p 0.95 ^
--num_beams 5 ^
--request_num 5 ^
--data_path F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval ^
--test_file HumanEvalPrograms_Qwen_IR4OR2.jsonl ^
--output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Result_Qwen/HumanEval_Qwen_Lora04_E5_Patch05.jsonl ^
--is_lora True ^
--lora_path F:/My_APR/Experiment_CodeLlama/repairllama/model_Qwen/model_Lora04/checkpoint-epoch-5.0/ ^
--base_model_path Qwen/Qwen2.5-Coder-1.5B

echo "========== Qwen Lora 04 - Epoch 05 - Patch 10 =========="
C:/Users/islab/anaconda3/envs/tensorflow_env/python.exe f:/My_APR/Experiment_CodeLlama/repairllama/src/lora/llama_pred_utf-8.py ^
--do_sample True ^
--only_do_beam True ^
--only_do_topp False ^
--only_do_topk False ^
--only_do_temp False ^
--temperature 0.8 ^
--top_k 0 ^
--top_p 0.95 ^
--num_beams 10 ^
--request_num 10 ^
--data_path F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval ^
--test_file HumanEvalPrograms_Qwen_IR4OR2.jsonl ^
--output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Result_Qwen/HumanEval_Qwen_Lora04_E5_Patch10.jsonl ^
--is_lora True ^
--lora_path F:/My_APR/Experiment_CodeLlama/repairllama/model_Qwen/model_Lora04/checkpoint-epoch-5.0/ ^
--base_model_path Qwen/Qwen2.5-Coder-1.5B

echo "Run End"
