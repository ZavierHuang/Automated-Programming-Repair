import json
import os
import subprocess
import tempfile
import shutil
from tqdm import tqdm

import json
from typing import Optional
from dataclasses import dataclass, field
from pathlib import Path

import torch
import transformers
from peft import PeftModel
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    GenerationConfig, 
    HfArgumentParser, 
    BitsAndBytesConfig,
)
from tqdm import tqdm

def ModelInit(LLM, LORA, EPOCH):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(LLM, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        LLM,
        torch_dtype=torch.float16,
        load_in_8bit=True,
        trust_remote_code=True,
        quantization_config=BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0
        ),
    )

    model_folder_path = r'F:\My_APR\Experiment_CodeLlama\repairllama\model_Qwen\model_Lora{}\checkpoint-epoch-{}.0'.format(LORA, EPOCH)

    model = PeftModel.from_pretrained(
        model,
        model_folder_path,
        torch_dtype=torch.float16,
    )
    model.config.pad_token = tokenizer.pad_token = tokenizer.unk_token = tokenizer.eos_token
    model.to(device)
    print('===================================================================================================')
    print('============                                                               ========================')
    print('============                                                               ========================')
    print('============                                                               ========================')
    print('============   Model Init LLM:{} LORA:{} EPOCH:{}      ========================'.format(LLM, LORA, EPOCH))
    print('============                                                               ========================')
    print('============                                                               ========================')
    print('============                                                               ========================')
    print('===================================================================================================')
    return model, tokenizer


def flatten_BFS_Beam_Search(model, tokenizer, buggy_Code, BEAM_NUM):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    inputs = tokenizer(buggy_Code, return_tensors="pt")
    inputs_len = inputs["input_ids"].shape[1]
    inputs_ids = inputs["input_ids"].to(device)

    generation_config = GenerationConfig(
        num_beams=BEAM_NUM,
        max_length = 512,
        early_stopping=True,
    )

    outputs = model.generate(
        input_ids=inputs_ids,
        max_new_tokens=256,
        num_return_sequences=BEAM_NUM, 
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        generation_config=generation_config,
    )

    output_ids = outputs[:, inputs_len:]
    output_patch = tokenizer.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)

    return output_patch

def readJsonLine(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def createFolder(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.mkdir(folder_path)
    except:
        print('remove {} error'.format(folder_path))

def checkJavaFormat(java_code, jar_path, folder_path, patchFileName, buggy_ID):
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    os.chdir(script_dir)

    if not os.path.isfile(jar_path):
        return (f"Google Java Format JAR file not found: {jar_path}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as temp_file:
        temp_filename = temp_file.name

        full_java_code = f"""
        public class {patchFileName} {{
            {java_code}
        }}
        """
        temp_file.write(full_java_code.encode())

    if not os.path.isfile(temp_filename):
        raise FileNotFoundError(f"Temporary file not found: {temp_filename}")

    result = subprocess.run(
        ["java", "-jar", jar_path, "--replace", temp_filename],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return (f"Google Java Format Error: {result.stderr}")

    with open(temp_filename, "r") as f:
        formatted_code = f.read()

    os.remove(temp_filename)

    formatted_code = importContent(buggy_ID) + '\n' + formatted_code

    # print("PATH:", folder_path + '/' + patchFileName + '.java')


    with open(folder_path + '/' + patchFileName + '.java', 'w', encoding='utf-8') as file:
        file.write(formatted_code)

    # print(formatted_code)

    if 'Node' in formatted_code and 'WeightedEdge' in formatted_code:
        return 'Node WeightedEdge'
    if 'Node' in formatted_code:
        return 'Node'
    if 'WeightedEdge' in formatted_code:
        return 'WeightedEdge'
    
    return 'Java Format Check Successfully'

def checkJavaCompile(patchFilePath, javaFormatResult):
    try:
        output_dir = './class_file/'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        java_files = [patchFilePath]

        if 'Node' in javaFormatResult:
            java_files.append('F:/My_APR/QuixBugTest/dataStructure/Node.java')
        
        if 'WeightedEdge' in javaFormatResult:
            java_files.append('F:/My_APR/QuixBugTest/dataStructure/WeightedEdge.java')

        result = subprocess.run(['javac', '-d', output_dir] + java_files, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        print("Error: javac is not installed or not found in PATH.")
        return False

def importContent(fileName):
    import_folder_path = "F:/My_APR/QuixBugs_Program/eachFileImport/"
    import_content = ""
    file_import_path = import_folder_path + fileName + '_ImportInfo.java'

    with open(file_import_path, 'r', encoding='utf-8') as importFile:
        for line in importFile:
            import_content += line

    return import_content

def list_subdirectories(directory):
        subdirectories = []
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                subdirectories.append(os.path.join(root, dir_name))
        return subdirectories

def Clear_BFS_AllModuleFolder():
    # 範例用法
    folder_path = "F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis_BFS/"  # 替換為你的資料夾路徑
    all_subdirectories = list_subdirectories(folder_path)

    module_subdirectories = [subfolder for subfolder in all_subdirectories if subfolder[subfolder.rfind('/')+1:].startswith('Module') is True]
    for subdirectory in module_subdirectories:
        createFolder(subdirectory)


def generateTwiceFill(LORA, EPOCH, PATCH):
    MIDDLE = '<|fim_middle|>'
    SUFFIX = '<|fim_suffix|>'
    PREFIX = '<|fim_prefix|>'

    Clear_BFS_AllModuleFolder()
    print("====================================================================")
    print("====================================================================")
    print("===============            Clear All Folder          ===============")
    print("====================================================================")
    print("====================================================================")


    MAIN_PATH = 'F:/My_APR/Experiment_CodeLlama/repairllama/'
    json_file_path = r'Verification_QuixBugs_Output\Result_Qwen_2.5\QuixBugs_Lora{}\QuixBugs_Lora{}_Patch{}\QuixBugs_Qwen_Lora{}_E{}_Patch{}.jsonl'.format(LORA, LORA, PATCH, LORA, EPOCH, PATCH)

    file_path = MAIN_PATH + json_file_path.replace('\\', '/')

    print("file_path:", file_path)


    google_java_format_path = "F:/My_APR/util/javaFormat/google-java-format-1.15.0-all-deps.jar"

    data = readJsonLine(file_path)

    # pendingList = ['BREADTH_FIRST_SEARCH']
    pendingList = ['BREADTH_FIRST_SEARCH', 'FLATTEN', 'LCS_LENGTH']

    
    with tqdm(total=len(data), desc="Processing Patches") as pbar:

        for item in data:
            index = 0

            buggy_ID = item['bug_id']
            buggy_Code = item['buggy_code']
            folder_path = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis_BFS/Module_{}'.format(buggy_ID)

            if buggy_ID not in pendingList:
                pbar.update(1)
                continue
            
            print("LORA:{} PATCH:{} EPOCH:{}".format(LORA, PATCH, EPOCH))
            createFolder(folder_path)        
                
            print(buggy_ID)

            BEAM_NUM = len(item['output'])

            for i in range(BEAM_NUM):
                patch = item['output'][str(i)]['output_patch']
                patch = patch.replace('</s>', '')
                patch = patch.strip()

                # Qwen2.5
                buggyCode = buggy_Code.replace(SUFFIX, patch, 1)
                buggyCode = buggyCode[:buggyCode.find(MIDDLE)+len(MIDDLE)]
                TwiceBuggy = buggyCode[buggyCode.find('// buggy code') : buggyCode.find('// fill') + len('// fill')]
                buggyCode = buggyCode.replace(TwiceBuggy, SUFFIX)
                patchCode = buggyCode + '\n' + TwiceBuggy[:-len('// fill')]


                results = flatten_BFS_Beam_Search(model, tokenizer, patchCode, BEAM_NUM)

                print("i:",i,"results:",results)

                for result in results:
                    patchFileName = buggy_ID + '_TEST_' + str(index)
                    patchFilePath = folder_path + '/' + patchFileName + '.java'


                    patchCodeTwice = patchCode.replace(SUFFIX, result.replace('</s>','').strip(), 1)
                    patchCodeTwice = patchCodeTwice.replace(PREFIX, '')
                    patchCodeTwice = patchCodeTwice.replace(patchCode[patchCode.find(MIDDLE):], '')
                    javaFormatResult = checkJavaFormat(patchCodeTwice, google_java_format_path, folder_path, patchFileName, buggy_ID)

                    if javaFormatResult.startswith('Google Java Format Error'):
                        # print(javaFormatResult)
                        continue
                    
                    checkCompileResult = checkJavaCompile(folder_path + '/' + patchFileName + '.java', javaFormatResult)
                    # print(checkCompileResult)
                    # print(index,folder_path + '/' + patchFileName + '.java')
                    
                    if checkCompileResult is False:
                        os.remove(patchFilePath)

                    index = index + 1
                
            pbar.update(1)

    for Module_Folder in pendingList:   
        source_folder = MAIN_PATH + r"Verification_QuixBugs_Output\Analysis_BFS\Module_{}".format(Module_Folder)
        destination_base_folder = MAIN_PATH + r"Verification_QuixBugs_Output\Analysis_Pending\Qwen2.5\Lora{}-E{}-{}".format(LORA, EPOCH, PATCH)

        # 確保目標資料夾存在
        os.makedirs(destination_base_folder, exist_ok=True)

        # 獲取來源資料夾的名稱
        folder_name = os.path.basename('Module_' + Module_Folder.rstrip("/\\"))
        # 定義目標路徑
        destination_folder = os.path.join(destination_base_folder, folder_name)
        try:
            shutil.copytree(source_folder, destination_folder)
            print(f"Copy {source_folder} To {destination_folder} Successfully")
        except FileExistsError:
            print(f"{destination_folder} Existed")
        except Exception as e:
            print(f"Copy Failure")

if __name__ == '__main__':

    LLM = 'Qwen/Qwen2.5-Coder-1.5B'

    # LORA_LIST = ['04', '08', '16']
    LORA_LIST = ['16']
    EPOCH_LIST = ['1', '2', '3', '4', '5']
    PATCH_LIST = ['01', '05', '10']

    for LORA in LORA_LIST:
        for EPOCH in EPOCH_LIST:
            model, tokenizer = ModelInit(LLM, LORA, EPOCH)
            for PATCH in PATCH_LIST:
                print("=====================================================")
                print("======== LORA:{} PATCH:{} EPOCH:{} ===============".format(LORA, PATCH, EPOCH))
                print("=====================================================")
                generateTwiceFill(LORA, EPOCH, PATCH)

                print("============================ Step1 LLM:{} LORA:{} PATCH:{} EPOCH:{} Done =================================\n\n".format(LLM, LORA, PATCH, EPOCH))
