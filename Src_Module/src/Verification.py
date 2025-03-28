import subprocess
from Config import *


class Verification:
    def __init__(self):
        self.googleJavaFormat = 'Tool/google-java-format-1.18.1-all-deps'


    def subprocess_run_JavaFormat(self, filePath):
        result = subprocess.run(
            ["java", "-jar", JAVA_FORMAT_PATH , "--replace", filePath],
            capture_output=True,
            text=True
        )
        return result
