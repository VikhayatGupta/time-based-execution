from Execution import TimeBasedExectuion
import sys
import threading
import os.path

if __name__ == "__main__":
    input_len = len(sys.argv)
    if input_len > 2:
        print("Single argument parameter is supported")
    elif input_len == 1:
        print(f"please provide absolute file path as an argument.\n\t-For Example python run.py <File name>")
    elif input_len == 2:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            time_based_exec = TimeBasedExectuion(file_path)
            thread = threading.Thread(target=time_based_exec.monitor_and_execute)
            thread.start()
        else:
            sys.exit(f"File ' {file_path} 'Not found.")
