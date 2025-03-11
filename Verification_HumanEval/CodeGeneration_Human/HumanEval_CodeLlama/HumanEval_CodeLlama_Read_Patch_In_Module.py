import os
import shutil
import json
import os
import subprocess
import tempfile
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def list_subdirectories(directory):
        subdirectories = []
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                subdirectories.append(os.path.join(root, dir_name))
        return subdirectories

def ClearAllFolder():
    # 範例用法
    folder_path = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Analysis/'  # 替換為你的資料夾路徑
    all_subdirectories = list_subdirectories(folder_path)

    index = 0
    module_subdirectories = [subfolder for subfolder in all_subdirectories if subfolder[subfolder.rfind('/')+1:].startswith('Module') is True]
    for subdirectory in module_subdirectories:
        createFolder(subdirectory)
        index += 1

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

def setImportContent(buggy_ID):
    importDict = {
        'ISCUBE' : [
            'import java.math.BigDecimal;', 
            'import java.math.RoundingMode;'
        ],

        'TRIANGLE_AREA_2' : [
            'import java.math.BigDecimal;', 
            'import java.math.RoundingMode;'
        ],

        'DO_ALGEBRA' : [
            'import javax.script.ScriptEngine;', 
            'import javax.script.ScriptEngineManager;', 
            'import javax.script.ScriptException;'
        ],
        'STRING_TO_MD5' : [
            'import javax.xml.bind.DatatypeConverter;', 
            'import java.security.MessageDigest;', 
            'import java.security.NoSuchAlgorithmException;'
        ]
    }

    
    if buggy_ID in importDict.keys():
        return '\n'.join(importDict[buggy_ID])
    return ''

def read_Remainder_Code(patchFileName):
    remainder_folder_path = r'F:\My_APR\Experiment_CodeLlama\repairllama\Verification_HumanEval\RemainContent'

    remainder_file_path = os.path.join(remainder_folder_path, patchFileName)

    content = ''
    if os.path.exists(remainder_file_path):
        with open(remainder_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

    return content

def checkJavaFormat(java_code, jar_path, folder_path, patchFileName, buggy_ID):
    script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    os.chdir(script_dir)

    if not os.path.isfile(jar_path):
        return f"Google Java Format JAR file not found: {jar_path}"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as temp_file:
        temp_filename = temp_file.name

        # patchFileName = DECODE_SHIFT
        remainder_code = read_Remainder_Code(buggy_ID + '.txt')

        java_code = java_code.replace(buggy_ID, patchFileName)

        full_java_code = f"""
        public class {patchFileName} {{
            {java_code}
            {remainder_code}
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
        return f"Google Java Format Error: {result.stderr}"

    with open(temp_filename, "r") as f:
        formatted_code = f.read()

    os.remove(temp_filename)

    otherImportContent = setImportContent(buggy_ID)

    formatted_code = "import java.util.*;\n" + otherImportContent + '\n' + formatted_code

    with open(folder_path + '/' + patchFileName + '.java', 'w', encoding='utf-8') as file:
        file.write(formatted_code)

    return 'Java Format Check Successfully'

def checkJavaCompile(patchFilePath, buggy_ID):
    try:
        output_dir = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Analysis/class_file/'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        java_files = [patchFilePath]

        result = subprocess.run(['javac', '-d', output_dir] + java_files, capture_output=True, text=True)
        
        if buggy_ID == 'STRING_TO_MD5':
            if 'java:14: error: cannot find symbol' in str(result) and 'symbol:   variable DatatypeConverter' in str(result):
                return True
            return False

        return result.returncode == 0
    except FileNotFoundError:
        print("Error: javac is not installed or not found in PATH.")
        return False

def processPatch(item, google_java_format_path):
    buggy_ID = item['bug_id']
    buggy_Code = item['buggy_code']
    folder_path = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Analysis/Module_{}'.format(buggy_ID)

    createFolder(folder_path)
    BEAM_NUM = len(item['output'])
    results = []

    for i in range(BEAM_NUM):
        patch = item['output'][str(i)]['output_patch']

        patch = patch.replace('</s>', '').strip()

        patchFileName = f"{buggy_ID}_TEST_{i}"
        patchFilePath = f"{folder_path}/{patchFileName}.java"

        patchCode = buggy_Code.replace('<FILL_ME>', patch, 1)

        javaFormatResult = checkJavaFormat(patchCode, google_java_format_path, folder_path, patchFileName, buggy_ID)
        
        print(javaFormatResult)

        if javaFormatResult.startswith('Google Java Format Error'):
            continue

        checkCompileResult = checkJavaCompile(patchFilePath,buggy_ID)

        if not checkCompileResult:
            os.remove(patchFilePath)
            pass

        results.append((patchFileName, checkCompileResult))
    return results



if __name__ == '__main__':
    ClearAllFolder()

    LLM = 'CodeLlama'
    LORA = '04'
    PATCH = '01'
    EPOCH = '1'

    MAIN_PATH = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/'
    file_path = MAIN_PATH + 'Result_{}/HumanEval_Lora{}/HumanEval_Lora{}_Patch{}/HumanEval_Lora{}_E{}_Patch{}.jsonl'.format(LLM, LORA, LORA, PATCH, LORA, EPOCH, PATCH)
    google_java_format_path = "F:/My_APR/util/javaFormat/google-java-format-1.15.0-all-deps.jar"
    data = readJsonLine(file_path)

    # pendingList = ['DECODE_SHIFT', 'EVEN_ODD_PALINDROME', 'FIND_ZERO', 'GET_ROW', 'INTERSECTION', 'IS_MULTIPLY_PRIME', 'LARGEST_PRIME_FACTOR', 'MAKE_PALINDROME', 'MATCH_PARENS', 'PRIME_FIB', 'SKJKASDKD', 'SORT_ARRAY_BINARY']
    pendingList = ['DECODE_CYCLIC']

    with tqdm(total=len(data), desc="Processing Patches") as pbar:
        with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust max_workers as needed
            futures = [
                executor.submit(processPatch, item, google_java_format_path)
                for item in data if item['bug_id'] in pendingList
            ]

            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception as e:
                    print(f"Error occurred: {e}")
                pbar.update(1)
    
    print("============================ Step1 HumanEval LLM:{} LORA:{} PATCH:{} EPOCH:{} Done =================================".format(LLM, LORA, PATCH, EPOCH))


           