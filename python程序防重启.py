import psutil

def is_program_running(program_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == program_name:
            return True
    return False

if is_program_running('program.py'):
    print("程序已经在运行！")
else:
    print("程序没有在运行。")