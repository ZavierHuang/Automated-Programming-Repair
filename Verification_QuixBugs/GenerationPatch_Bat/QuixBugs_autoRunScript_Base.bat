#!/bin/bash
@echo off
echo "Run Start..."
echo "================================================================"
echo "==========                                            =========="
echo "==========                                            =========="
echo "==========    DeepSeekCoder Epoch 01 - Patch 01       =========="
echo "==========                                            =========="
echo "==========                                            =========="
echo "================================================================"
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
--data_path F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs ^
--test_file QuixBugsProgram_DeepSeekCoder_IR4OR2.jsonl ^
--output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Result_DeepSeekCoder/QuixBugs_DeepSeekCoder_Base_Patch01.jsonl ^
--is_lora False ^
--base_model_path deepseek-ai/deepseek-coder-1.3b-base

echo "================================================================"
echo "==========                                            =========="
echo "==========                                            =========="
echo "==========    DeepSeekCoder Epoch 01 - Patch 05       =========="
echo "==========                                            =========="
echo "==========                                            =========="
echo "================================================================"
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
--data_path F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs ^
--test_file QuixBugsProgram_DeepSeekCoder_IR4OR2.jsonl ^
--output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Result_DeepSeekCoder/QuixBugs_DeepSeekCoder_Base_Patch05.jsonl ^
--is_lora False ^
--base_model_path deepseek-ai/deepseek-coder-1.3b-base

echo "================================================================"
echo "==========                                            =========="
echo "==========                                            =========="
echo "==========    DeepSeekCoder Epoch 01 - Patch 10       =========="
echo "==========                                            =========="
echo "==========                                            =========="
echo "================================================================"
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
--data_path F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs ^
--test_file QuixBugsProgram_DeepSeekCoder_IR4OR2.jsonl ^
--output_file F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Result_DeepSeekCoder/QuixBugs_DeepSeekCoder_Base_Patch10.jsonl ^
--is_lora False ^
--base_model_path deepseek-ai/deepseek-coder-1.3b-base

echo "Run End"
