import os
import shutil
import json
import os
import subprocess
import tempfile
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import pandas as pd
import os
import shutil
import subprocess
from tqdm import tqdm

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
    MIDDLE = '<|fim_middle|>'
    SUFFIX = '<|fim_suffix|>'
    PREFIX = '<|fim_prefix|>'
    
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

        patchCode = buggy_Code.replace(SUFFIX, patch, 1)
        patchCode = patchCode.replace(PREFIX, '')
        patchCode = patchCode.replace(patchCode[patchCode.find(MIDDLE):], '')

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

#=========================================================================================#

def readFile(file_path):
    content = ''
    with open(file_path) as file:
        content += file.read()
    return content

def list_all_files(directory, extension):
    fileList = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                fileList.append(os.path.join(root, file))
    return fileList

def get_subdirectories(directory):
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return subdirectories

def clear_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path) and filename != 'dataStructures':
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"delete {file_path} error: {e}")
    else:
        print(f"folder {directory_path} is not existed!")

def clear_RunTestCase_Module_Folder(directory): # directory = 'F:/My_APR/RunTestCase'
    module_directories = []
    subdirectories = get_subdirectories(directory)
    for subdir in subdirectories:
        if subdir[:6] == 'Module':
            module_directories.append(subdir)

    for subdir in module_directories:
        directory = 'F:/My_APR/RunTestCase/' + subdir + '/src/main/java' 
        clear_directory(directory)
    print('Step1. All files are deleted')

def add_dataStructure_Import(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        import_datastructures_str = 'import dataStructures.*;\n\n'

        if import_datastructures_str not in content:
            new_content = import_datastructures_str + content
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            return True
        else:
            return True
    except:
        return False

def copy_and_update_files(directory, copy_folder_path):
    for root, _ , files in os.walk(directory):
        for filename in files:
            if filename == 'Node.java' or filename == 'WeightedEdge.java':
                continue

            file_path = os.path.join(root, filename)
            if add_dataStructure_Import(file_path):
                shutil.copy2(file_path, copy_folder_path)

def add_import_and_Copy_File(directory):
    # directory = 'F:/My_APR/java_programs'  # 產生候選程式的目標資料夾路徑

    subdirectories = get_subdirectories(directory)

    if 'class_file' in subdirectories:
        subdirectories.remove('class_file')
    
    if 'OutputResult' in subdirectories:
        subdirectories.remove('OutputResult')

    for subdir in subdirectories:
        copy_folder_path = 'F:/My_APR/RunTestCase/' + subdir + '/src/main/java'
        copy_and_update_files(directory + '/' + subdir, copy_folder_path)

    print("Step2.",len(subdirectories),"Programs Generate Patch")

def getMoudleNameList(directory):
    module_directories = []
    subdirectories = get_subdirectories(directory)

    for subdir in subdirectories:
        if subdir[:6] == 'Module':
            module_directories.append(subdir)
    return module_directories
    
def get_all_testFile_List(directory):
    module_directories = getMoudleNameList(directory)
    
    runList = []
    for dir in module_directories:
        patchFile_path = directory + '/' + dir + '/src/main/java'
        for filename in os.listdir(patchFile_path):
            file_path = os.path.join(patchFile_path, filename)
            if os.path.isfile(file_path):
                runList.append(filename)
    return runList
       
def run_bash_script(script_path, params):
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found.")
        return

    bash_path = "C:/Program Files/Git/bin/bash.exe" 
    command = [bash_path, script_path] + params

    try:
        subprocess.run(command, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print("Error executing script:")
        print(e.stderr)

def runTestCase(TestModuleName, programName, dateFolder):
    params = []
    params.append(TestModuleName)
    params.append(programName)
    params.append(dateFolder)

    RunTestCase_Path = 'F:/My_APR/RunTestCase'
    # 切換到 RunTestCase 的路徑底下
    os.chdir(RunTestCase_Path)

    script_path = 'F:/My_APR/QuixBugTest/execute_python.sh'

    run_bash_script(script_path, params)

    # 切換為原本的路徑
    os.chdir('F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis/')

def replaceProgramName(testFilePath, oldProgramName, newProgramName):
    try:
        with open(testFilePath, 'r', encoding='utf-8') as file:
            content = file.read()

        modified_content = content.replace(oldProgramName + '.', newProgramName + '.')

        with open(testFilePath, 'w', encoding='utf-8') as file:
            file.write(modified_content)

    except FileNotFoundError:
        print(f"Error: File {testFilePath} not found.")  
    except Exception as e:
        print(f"An error occurred: {e}")

def replace_TestFile_ProgramName_And_Run_TestCase(RunTestCase_Path, runList, dataFolder):
    for testFile in tqdm(runList, desc="Replacing program names and running test cases"):

        # pendingList = ['LCS_LENGTH', 'MINIMUM_SPANNING_TREE', 'POWERSET', 'REVERSE_LINKED_LIST']

        oldProgramName = testFile[:testFile.find('_TEST')]                                                     # BITCOUNT

        # if oldProgramName in pendingList:
        if True:
            newPorgramName = testFile[:testFile.find('.java')]                                                      # BITCOUNT_TEST_0
            testModuleName = 'Module_' + testFile[:testFile.rfind('TEST')-1]                                        # Module_BITCOUNT
            testFileName = testFile[:testFile.rfind('_')] + '.java'                                                 # BITCOUNT_TEST
            testFilePath = RunTestCase_Path + '/' + testModuleName + '/' + 'src/test/java/' + testFileName
            # print(newPorgramName + ' Run TestCase')
            replaceProgramName(testFilePath, oldProgramName, newPorgramName)
            runTestCase(testModuleName, newPorgramName, dataFolder)
            replaceProgramName(testFilePath, newPorgramName, oldProgramName)


def list_subfolders(folder_path):
    # 列出資料夾中的所有子資料夾
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    return subfolders

def get_all_folder_list():
    # 指定資料夾路徑
    folder_path = "F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis"

    # 取得子資料夾檔名
    subfolders = list_subfolders(folder_path)

    subfolderList = []

    # 印出子資料夾檔名
    for subfolder in subfolders:
        if subfolder.startswith('Module'):
            subfolderList.append(subfolder[subfolder.find('_')+1:] + '_TEST')

    return subfolderList

def runTestCaseScript(dataFolder, patchFile_Directory):
    RunTestCase_Path = 'F:/My_APR/RunTestCase'

    print(patchFile_Directory)

    patchFile_Directory = patchFile_Directory.replace('/','\\')
    
    clear_RunTestCase_Module_Folder(RunTestCase_Path)                                                   # Step1. Clear RunTestCase Module Folder
    add_import_and_Copy_File(patchFile_Directory)                                                       # Step2. Add datastructrues import and Copy File to RunTestCase
    runList = get_all_testFile_List(RunTestCase_Path)                                                   # Step3. Get all testFile List
    replace_TestFile_ProgramName_And_Run_TestCase(RunTestCase_Path, runList, dataFolder)                # Step4 & Step5.Replace File and Run TestCase
    print("Total Files run TestCase:", len(runList))
    
    experimentResultPath = 'F:/My_APR/QuixBugTest/' + dataFolder
    file_List = list_all_files(experimentResultPath, '.txt')

    compileError = 0
    Failure_Recover = 0
    Part_Recover = 0
    Success_Recover = 0
    
    buildSuccessfulList = []
    buildSuccessfulSet = set()

    for file_path in tqdm(file_List, desc="Processing result files"):
        result = []
        fileName = file_path[file_path.rfind('\\')+1:-4]
        
        print('file_Name:',fileName)        
        content = readFile(file_path)
        result.append(fileName)

        testCaseResult = re.search(r"(\d+) tests completed, (\d+) failed", content)
        buildSuccessful = re.search('BUILD SUCCESSFUL',content)

        if buildSuccessful:
            Success_Recover += 1
            buildSuccessfulList.append(fileName)
            buildSuccessfulSet.add(fileName[:fileName.rfind('_')])

        elif testCaseResult:
            total = int(testCaseResult.group(1))                        # total => 9
            failed = int(testCaseResult.group(2))                       # failed => 8

            if failed == total:
                Failure_Recover += 1
                continue
            else:
                Part_Recover += 1

        else:
            compileError += 1
            continue
    
    buildSuccessfulSet = sorted(list(buildSuccessfulSet))
    result += 'dataFolder:' + str(dataFolder) + '\n'
    result = 'total:' + str(len(file_List)) + '\n'
    result += 'compileError:' + str(compileError) + '\n'
    result += 'Failure_Recover:' + str(Failure_Recover) + '\n'
    result += 'Part_Recover:' + str(Part_Recover) + '\n'
    result += 'Success_Recover:' + str(Success_Recover) + '\n'
    result += 'QuixBugs:' + str(len(buildSuccessfulSet)) + ' / 40\n'
    result += 'buildSuccessfulList:\n' + '\n'.join((map(str, buildSuccessfulList))) + '\n\n'
    result += 'buildSuccessfulSet:\n'  + '\n'.join((map(str, buildSuccessfulSet))) + '\n\n'


    subfolderList = get_all_folder_list()

    for passfile in buildSuccessfulSet:
        if passfile in subfolderList:
            subfolderList.remove(passfile)


    result += 'Failure Repair:' + '\n'.join((map(str, subfolderList))) + '\n\n'


    print(result)
    
    with open('F:/My_APR/QuixBugTest/TempResultReport/' + 'Result_' + dataFolder + '.txt', 'w') as file:
        file.write(result)
    
    
def runTestCase_Start(LLM, LORA, PATCH, EPOCH):
    dataFolder = '{}_Lora{}_Patch{}-{}'.format(LLM, LORA, PATCH, EPOCH)

    patchFile_Directory = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis'
    
    runTestCaseScript(dataFolder, patchFile_Directory)

    source = "F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Analysis/"

    destination = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_QuixBugs_Output/Patch/'
    destination = destination + dataFolder

    try: 
        shutil.copytree(source, destination)
        print("Folder copied successfully.")
    except FileExistsError:
        print("Destination folder already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("============================ Step3 LLM{} LORA:{} PATCH:{} EPOCH:{} Done =================================".format(LLM, LORA, PATCH, EPOCH))

def read_PatchFile_Data(LLM, LORA, PATCH, EPOCH):

    ClearAllModuleFolder()

    MAIN_PATH = 'F:/My_APR/Experiment_CodeLlama/repairllama/'
    json_file_path = r'Verification_QuixBugs_Output\Result_{}\QuixBugs_Lora{}\QuixBugs_Lora{}_Patch{}\QuixBugs_{}_Lora{}_E{}_Patch{}.jsonl'.format(LLM, LORA, LORA, PATCH, LLM, LORA, EPOCH, PATCH)
    file_path = MAIN_PATH + json_file_path.replace('\\', '/')
    
    google_java_format_path = "F:/My_APR/util/javaFormat/google-java-format-1.15.0-all-deps.jar"
    data = readJsonLine(file_path)
    
    BFS_Flatten_LCS_Folder = MAIN_PATH + r'Verification_QuixBugs_Output\Analysis_Pending\{}\Lora{}\Lora{}-E{}-{}'.format(LLM, LORA, LORA, EPOCH,PATCH)
    target_Folder = MAIN_PATH + r'Verification_QuixBugs_Output\Analysis'
    print("==============================================================================================")
    print("==============================================================================================")
    print('BFS_Flatten_LCS_Folder:', BFS_Flatten_LCS_Folder)
    print("==============================================================================================")
    print("==============================================================================================\n")



    copy_folder_contents(BFS_Flatten_LCS_Folder, target_Folder)

    pendingList = ['BREADTH_FIRST_SEARCH', 'FLATTEN', 'LCS_LENGTH']

    with tqdm(total=len(data), desc="Processing Patches") as pbar:
        with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust max_workers as needed
            futures = [
                executor.submit(processPatch, item, google_java_format_path)
                for item in data if item['bug_id'] not in pendingList
            ]

            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception as e:
                    print(f"Error occurred: {e}")
                pbar.update(1)
    

def StartMessage(LLM, LORA, PATCH, EPOCH):
    print("==============================================================================================")
    print("==============================================================================================")
    print("======================= LLM{} LORA:{} PATCH:{} EPOCH:{} ============================".format(LLM, LORA, PATCH, EPOCH))
    print("==============================================================================================")
    print("==============================================================================================\n\n")


if __name__ == '__main__':
    LORA_LIST = ['16']
    PATCH_LIST = ['01', '05', '10']
    EPOCH_LIST = ['1', '2', '3', '4', '5']
    LLM = 'Qwen'

    for LORA in LORA_LIST:
        for PATCH in PATCH_LIST:
            for EPOCH in EPOCH_LIST:
                StartMessage(LLM, LORA, PATCH, EPOCH)

                print("==============================================================================================")
                print("==============================================================================================")
                print("===================================== Clear All ==============================================")
                print("==============================================================================================")
                print("==============================================================================================\n\n")
                
                ClearAllModuleFolder()
                
                print("============================ Step1 LLM{} LORA:{} PATCH:{} EPOCH:{} Start =================================".format(LLM, LORA, PATCH, EPOCH))
                read_PatchFile_Data(LLM, LORA, PATCH, EPOCH)
                
                print("============================ Step2 LLM{} LORA:{} PATCH:{} EPOCH:{} Start =================================".format(LLM, LORA, PATCH, EPOCH))
                runTestCase_Start(LLM, LORA, PATCH, EPOCH)

                print("============================ LLM:{} LORA:{} PATCH:{} EPOCH:{} Done ============================\n\n".format(LLM, LORA, PATCH, EPOCH))


