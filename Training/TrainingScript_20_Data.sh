#!/bin/bash

# DeepSeekCoder-Lora16
python /home/vcpuser/netdrive/Workspace/src/llama_sft_fp32_DeepSeekCoder.py \
--data_path "json" \
--cache_path "./cache/" \
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
--num_train_epochs 2 \
--per_device_train_batch_size 16 \
--model_name_or_path "deepseek-ai/deepseek-coder-1.3b-base" \
--train_file "/home/vcpuser/netdrive/Workspace/data/train_data.jsonl" \
--eval_file "/home/vcpuser/netdrive/Workspace/data/test_data.jsonl" \
--output_dir "/home/vcpuser/netdrive/Workspace/model_Test/model_DeepSeek_TEST"

# Qwen Lora04
python /home/vcpuser/netdrive/Workspace/src/llama_sft_fp32_Qwen_Lora04.py \
--data_path "json" \
--cache_path "./cache/" \
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
--num_train_epochs 2 \
--per_device_train_batch_size 8 \
--model_name_or_path "Qwen/Qwen2.5-Coder-1.5B" \
--train_file "/home/vcpuser/netdrive/Workspace/data/train_data.jsonl" \
--eval_file "/home/vcpuser/netdrive/Workspace/data/test_data.jsonl" \
--output_dir "/home/vcpuser/netdrive/Workspace/model_Test/model_Qwen_TEST"

echo "All Run Successfully"
