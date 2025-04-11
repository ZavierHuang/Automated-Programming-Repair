#!/bin/bash

runGradleTest() {
    local moduleTestName=$1
    local project_dir=$5
#    gradle :Module_ADD:test
    local gradle_test_command="$GRADLE_PATH/gradle :$moduleTestName:test"

    echo ${gradle_test_command}

    cd "$project_dir" || {
        echo "Error：switch directionary $project_dir failure." | tee -a $OUTPUT_PATH
        exit 1
    }

    $gradle_test_command 2>&1 | tee -a $OUTPUT_PATH
    # 檢查測試是否成功
    if [ $? -eq 0 ]; then
        echo "Successfully" | tee -a $OUTPUT_PATH
    else
        echo "Failure" | tee -a $OUTPUT_PATH
    fi
}

TEST_MODULE_NAME=$1
PROGRAM_FILE_NAME=$2
LOG_FOLDER=$3
GRADLE_PATH=$4
RUN_JUNIT_ENVIRONMENT=$5
OUTPUT_DIR="${LOG_FOLDER}"
OUTPUT_PATH="${OUTPUT_DIR}/${PROGRAM_FILE_NAME}.txt"

mkdir -p $OUTPUT_DIR

if [ ! -x "$GRADLE_PATH/gradle" ]; then
    echo "Error：In $GRADLE_PATH/gradle not find Gradle" | tee -a $OUTPUT_PATH
    exit 1
fi

runGradleTest "$TEST_MODULE_NAME"
echo "$TEST_MODULE_NAME" | tee -a $OUTPUT_PATH

# 顯示完成訊息
echo | tee -a $OUTPUT_PATH
echo "Task Complete!" | tee -a $OUTPUT_PATH