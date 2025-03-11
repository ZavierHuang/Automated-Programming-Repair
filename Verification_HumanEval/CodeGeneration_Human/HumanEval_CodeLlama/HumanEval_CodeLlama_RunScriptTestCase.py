import re
import pandas as pd
import os
import shutil
import subprocess
from tqdm import tqdm


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

def clear_RunTestCase_Module_Folder(directory): # directory = 'F:/My_APR/RunTestCase_HumanEval'
    module_directories = []
    subdirectories = get_subdirectories(directory)
    for subdir in subdirectories:
        if subdir[:6] == 'Module':
            module_directories.append(subdir)

    for subdir in module_directories:
        directory = 'F:/My_APR/RunTestCase_HumanEval/' + subdir + '/src/main/java' 
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
            # if filename == 'Node.java' or filename == 'WeightedEdge.java':
            #     continue

            file_path = os.path.join(root, filename)
            # if add_dataStructure_Import(file_path):
            shutil.copy2(file_path, copy_folder_path)

def add_import_and_Copy_File(directory):
    # directory = 'F:/My_APR/java_programs'  # 產生候選程式的目標資料夾路徑

    subdirectories = get_subdirectories(directory)

    if 'class_file' in subdirectories:
        subdirectories.remove('class_file')
    
    if 'OutputResult' in subdirectories:
        subdirectories.remove('OutputResult')

    if '.idea' in subdirectories:
        subdirectories.remove('.idea')

    for subdir in subdirectories:
        copy_folder_path = 'F:/My_APR/RunTestCase_HumanEval/' + subdir + '/src/main/java'
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

    RunTestCase_Path = 'F:/My_APR/RunTestCase_HumanEval'
    # 切換到 RunTestCase 的路徑底下
    os.chdir(RunTestCase_Path)

    script_path = 'F:/My_APR/HumanEvalTest/execute_python_humanEval.sh'

    run_bash_script(script_path, params)

    # 切換為原本的路徑
    os.chdir("F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Analysis/")

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

        # pendingList = ['LCS_LENGTH']

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
    folder_path = "F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Analysis/"

    # 取得子資料夾檔名
    subfolders = list_subfolders(folder_path)

    subfolderList = []

    # 印出子資料夾檔名
    for subfolder in subfolders:
        if subfolder.startswith('Module'):
            subfolderList.append(subfolder[subfolder.find('_')+1:] + '_TEST')

    return subfolderList

def runTestCaseScript(dataFolder, patchFile_Directory):
    RunTestCase_Path = 'F:/My_APR/RunTestCase_HumanEval'

    patchFile_Directory = patchFile_Directory.replace('/','\\')
    
    clear_RunTestCase_Module_Folder(RunTestCase_Path)                                                   # Step1. Clear RunTestCase Module Folder
    add_import_and_Copy_File(patchFile_Directory)                                                       # Step2. Add datastructrues import and Copy File to RunTestCase
    runList = get_all_testFile_List(RunTestCase_Path)                                                   # Step3. Get all testFile List
    replace_TestFile_ProgramName_And_Run_TestCase(RunTestCase_Path, runList, dataFolder)                # Step4 & Step5.Replace File and Run TestCase
    print("Total Files run TestCase:", len(runList))
    
    experimentResultPath = 'F:/My_APR/HumanEvalTest/' + dataFolder
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
        
        # print('file_Name:',fileName)        
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
    result = 'total:' + str(len(file_List)) + '\n'
    result += 'compileError:' + str(compileError) + '\n'
    result += 'Failure_Recover:' + str(Failure_Recover) + '\n'
    result += 'Part_Recover:' + str(Part_Recover) + '\n'
    result += 'Success_Recover:' + str(Success_Recover) + '\n'
    result += 'HumanEval:' + str(len(buildSuccessfulSet)) + ' / 163\n'
    result += 'buildSuccessfulList:\n' + '\n'.join((map(str, buildSuccessfulList))) + '\n\n'
    result += 'buildSuccessfulSet:\n'  + '\n'.join((map(str, buildSuccessfulSet))) + '\n\n'


    subfolderList = get_all_folder_list()

    for passfile in buildSuccessfulSet:
        if passfile in subfolderList:
            subfolderList.remove(passfile)


    result += 'Failure Repair:\n' + '\n'.join((map(str, subfolderList))) + '\n\n'


    print(result)
    
    with open('F:/My_APR/HumanEvalTest/TempResultReport/' + 'Result_' + dataFolder + '.txt', 'w') as file:
        file.write(result)
    
    
if __name__ == '__main__':

    LLM = 'CodeLlama'
    LORA = '04'
    PATCH = '10'
    EPOCH = '5'
    
    dataFolder = 'HumanEval_{}_Lora{}_Patch{}-{}'.format(LLM, LORA, PATCH, EPOCH)

    print(dataFolder)
    
    patchFile_Directory = "F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Analysis/"
    runTestCaseScript(dataFolder, patchFile_Directory)

    source = "F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Analysis/"
    destination = 'F:/My_APR/Experiment_CodeLlama/repairllama/Verification_HumanEval_Output/Patch/'
    destination = destination + dataFolder

    try:
        shutil.copytree(source, destination)
        print("Folder copied successfully.")
    except FileExistsError:
        print("Destination folder already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("============================ Step2 HumanEval LLM:{} LORA:{} PATCH:{} EPOCH:{} Done =================================".format(LLM, LORA, PATCH, EPOCH))
      