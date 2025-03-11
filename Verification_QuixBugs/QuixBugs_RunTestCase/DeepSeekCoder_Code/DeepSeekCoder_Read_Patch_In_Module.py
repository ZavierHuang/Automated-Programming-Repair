import os
import shutil
import json
import os
import subprocess
import tempfile
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def createFolder(folder_path):
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(folder_path[folder_path.rfind('/')+1:] + ' delete')
        os.mkdir(folder_path)
    except:
        print('remove {} error'.format(folder_path))

def list_subdirectories(directory):
        subdirectories = []
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                subdirectories.append(os.path.join(root, dir_name))
        return subdirectories

def ClearAllModuleFolder():
    # 範例用法
    folder_path = "F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis/"  # 替換為你的資料夾路徑
    all_subdirectories = list_subdirectories(folder_path)

    module_subdirectories = [subfolder for subfolder in all_subdirectories if subfolder[subfolder.rfind('/')+1:].startswith('Module') is True]
    for subdirectory in module_subdirectories:
        createFolder(subdirectory)




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
        return f"Google Java Format JAR file not found: {jar_path}"

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
        return f"Google Java Format Error: {result.stderr}"

    with open(temp_filename, "r") as f:
        formatted_code = f.read()

    os.remove(temp_filename)

    formatted_code = importContent(buggy_ID) + '\n' + formatted_code

    with open(folder_path + '/' + patchFileName + '.java', 'w', encoding='utf-8') as file:
        file.write(formatted_code)

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

        return result.returncode == 0
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

def processPatch(item, google_java_format_path):
    buggy_ID = item['bug_id']
    buggy_Code = item['buggy_code']
    folder_path = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis/Module_{}'.format(buggy_ID)

    createFolder(folder_path)
    BEAM_NUM = len(item['output'])
    results = []

    for i in range(BEAM_NUM):
        patch = item['output'][str(i)]['output_patch']
        patch = patch.replace('</s>', '').strip()

        patchFileName = f"{buggy_ID}_TEST_{i}"
        patchFilePath = f"{folder_path}/{patchFileName}.java"

        patchCode = buggy_Code.replace('<｜fim▁hole｜>', patch, 1)
        patchCode = patchCode.replace('<｜fim▁begin｜>', '')
        patchCode = patchCode.replace(patchCode[patchCode.find('<｜fim▁end｜>'):], '')

        javaFormatResult = checkJavaFormat(patchCode, google_java_format_path, folder_path, patchFileName, buggy_ID)

        if javaFormatResult.startswith('Google Java Format Error'):
            continue

        checkCompileResult = checkJavaCompile(patchFilePath, javaFormatResult)
        if not checkCompileResult:
            os.remove(patchFilePath)

        results.append((patchFileName, checkCompileResult))
    return results


def copy_folder_contents(source_folder, destination_folder):
    # 確保來源資料夾存在
    if not os.path.exists(source_folder):
        print(f"來源資料夾 {source_folder} 不存在！")
        return

    # 確保目標資料夾存在，如果不存在則建立
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍歷來源資料夾中的所有檔案和資料夾
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(destination_folder, item)

        # 如果是檔案則複製檔案，若是資料夾則遞迴複製
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

if __name__ == '__main__':

    ClearAllModuleFolder()

    LORA = '08'
    PATCH = '01'
    EPOCH = '1'
    LLM = 'DeepSeekCoder1.3B'

    MAIN_PATH = 'F:/My_APR/Experiment_CodeLlama/repairllama/'
    # json_file_path = r'Verification_QuixBugs_Output\Result_DeepSeek_1.3\QuixBugs_Lora{}\QuixBugs_Lora{}_Patch{}\QuixBugs_DeepSeek_Lora{}_E{}_Patch{}.jsonl'.format(LORA, LORA, PATCH, LORA, EPOCH, PATCH)
    # file_path = MAIN_PATH + json_file_path.replace('\\', '/')
    
    # google_java_format_path = "F:/My_APR/util/javaFormat/google-java-format-1.15.0-all-deps.jar"
    # data = readJsonLine(file_path)

    # pendingList = ['BREADTH_FIRST_SEARCH', 'FLATTEN', 'LCS_LENGTH']

    # with tqdm(total=len(data), desc="Processing Patches") as pbar:
    #     with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust max_workers as needed
    #         futures = [
    #             executor.submit(processPatch, item, google_java_format_path)
    #             for item in data if item['bug_id'] not in pendingList
    #         ]

    #         for future in as_completed(futures):
    #             try:
    #                 result = future.result()
    #             except Exception as e:
    #                 print(f"Error occurred: {e}")
    #             pbar.update(1)


    BFS_Flatten_LCS_Folder = MAIN_PATH + r'Verification_QuixBugs_Output\Analysis_Pending\DeepSeekCoder1.3B\Lora{}\Lora{}-E{}-{}'.format(LORA,LORA,EPOCH,PATCH)
    target_Folder = MAIN_PATH + r'Verification_QuixBugs_Output\Analysis'
    copy_folder_contents(BFS_Flatten_LCS_Folder, target_Folder)

    
    print("============================ Step2 LLM:{} LORA:{} PATCH:{} EPOCH:{} Done ============================".format(LLM, LORA, PATCH, EPOCH))

