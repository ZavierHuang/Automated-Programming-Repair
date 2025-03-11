#!/bin/bash
echo "Run Start..."
@REM echo "========== DeepSeekCoder Patch 10 =========="
@REM C:/Users/islab/anaconda3/envs/tensorflow_env/python.exe f:/My_APR/Experiment_CodeLlama/repairllama/src/lora/llama_pred_utf-8.py ^
@REM --do_sample True ^
@REM --only_do_beam True ^
@REM --only_do_topp False ^
@REM --only_do_topk False ^
@REM --only_do_temp False ^
@REM --temperature 0.8 ^
@REM --top_k 0 ^
@REM --top_p 0.95 ^
@REM --num_beams 10 ^
@REM --request_num 10 ^
@REM --data_path F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval ^
@REM --test_file HumanEvalPrograms_DeepSeekCoder_IR4OR2.jsonl ^
@REM --output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Result_DeepSeekCoder/HumanEval_DeepSeekCoder_Base_Patch10.jsonl ^
@REM --is_lora False ^
@REM --base_model_path deepseek-ai/deepseek-coder-1.3b-base

echo "========== Qwen epoch 01 Patch 10 =========="
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
--test_file HumanEvalPrograms_Qwen_IR4OR2_TEST.jsonl ^
--output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Result_Qwen/HumanEval_Qwen_Base_Patch10.jsonl ^
--is_lora True ^
--lora_path F:/My_APR/Experiment_CodeLlama/repairllama/model_Qwen/model_Lora04/checkpoint-epoch-1.0/ ^
--base_model_path Qwen/Qwen2.5-Coder-1.5B