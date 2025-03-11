#!/bin/bash

# DeepSeekCoder-Lora16
python /home/vcpuser/netdrive/Workspace/src/llama_sft_fp32_DeepSeekCoder.py \
--data_path "json" \
--cache_path "/home/vcpuser/netdrive/Workspace/cache/" \
--do_train \
--do_eval False \
--per_device_eval_batch_size 1 \
--gradient_accumulation_steps 1 \
--evaluation_strategy "no" \
--eval_steps 10 \
--save_steps 150 \
--learning_rate 5e-4 \
--lr_scheduler_type "cosine" \
--logging_steps 10 \
--ddp_find_unused_parameters False \
--is_lora True \
--model_max_length 1024 \
--num_train_epochs 5 \
--per_device_train_batch_size 32 \
--model_name_or_path "deepseek-ai/deepseek-coder-1.3b-base" \
--train_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_DeepSeek/train_hole_data.jsonl" \
--eval_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_DeepSeek/test_hole_data.jsonl" \
--output_dir "/home/vcpuser/netdrive/Workspace/model_DeepSeek/model_DeepSeek_Lora16/"

# Qwen Lora04
python /home/vcpuser/netdrive/Workspace/src/llama_sft_fp32_Qwen_Lora04.py \
--data_path "json" \
--cache_path "/home/vcpuser/netdrive/Workspace/cache/" \
--do_train \
--do_eval False \
--per_device_eval_batch_size 1 \
--gradient_accumulation_steps 1 \
--evaluation_strategy "no" \
--eval_steps 10 \
--save_steps 150 \
--learning_rate 5e-4 \
--lr_scheduler_type "cosine" \
--logging_steps 10 \
--ddp_find_unused_parameters False \
--is_lora True \
--model_max_length 1024 \
--num_train_epochs 5 \
--per_device_train_batch_size 8 \
--model_name_or_path "Qwen/Qwen2.5-Coder-1.5B" \
--train_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_Qwen/train_qwen_middle_data.jsonl" \
--eval_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_Qwen/test_qwen_middle_data.jsonl" \
--output_dir "/home/vcpuser/netdrive/Workspace/model_Qwen/model_Qwen2.5_Lora04/"

# Qwen Lora08
python /home/vcpuser/netdrive/Workspace/src/llama_sft_fp32_Qwen_Lora08.py \
--data_path "json" \
--cache_path "/home/vcpuser/netdrive/Workspace/cache/" \
--do_train \
--do_eval False \
--per_device_eval_batch_size 1 \
--gradient_accumulation_steps 1 \
--evaluation_strategy "no" \
--eval_steps 10 \
--save_steps 150 \
--learning_rate 5e-4 \
--lr_scheduler_type "cosine" \
--logging_steps 10 \
--ddp_find_unused_parameters False \
--is_lora True \
--model_max_length 1024 \
--num_train_epochs 5 \
--per_device_train_batch_size 8 \
--model_name_or_path "Qwen/Qwen2.5-Coder-1.5B" \
--train_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_Qwen/train_qwen_middle_data.jsonl" \
--eval_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_Qwen/test_qwen_middle_data.jsonl" \
--output_dir "/home/vcpuser/netdrive/Workspace/model_Qwen/model_Qwen2.5_Lora08/"

# Qwen Lora16
python /home/vcpuser/netdrive/Workspace/src/llama_sft_fp32_Qwen_Lora16.py \
--data_path "json" \
--cache_path "/home/vcpuser/netdrive/Workspace/cache/" \
--do_train \
--do_eval False \
--per_device_eval_batch_size 1 \
--gradient_accumulation_steps 1 \
--evaluation_strategy "no" \
--eval_steps 10 \
--save_steps 150 \
--learning_rate 5e-4 \
--lr_scheduler_type "cosine" \
--logging_steps 10 \
--ddp_find_unused_parameters False \
--is_lora True \
--model_max_length 1024 \
--num_train_epochs 5 \
--per_device_train_batch_size 8 \
--model_name_or_path "Qwen/Qwen2.5-Coder-1.5B" \
--train_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_Qwen/train_qwen_middle_data.jsonl" \
--eval_file "/home/vcpuser/netdrive/Workspace/data/IR4OR2_Qwen/test_qwen_middle_data.jsonl" \
--output_dir "/home/vcpuser/netdrive/Workspace/model_Qwen/model_Qwen2.5_Lora16/"

echo "All Run Successfully"
