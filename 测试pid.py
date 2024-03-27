# import os

# pid = os.getpid()

# def read_pid_from_file(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             content = file.read().strip()  # 读取文件内容并去除首尾的空白字符
#             file_pid = int(content)  # 将内容转换为整数
#             return file_pid
#     except FileNotFoundError:
#         print(f"文件 '{file_path}' 不存在。")
#     except ValueError:
#         print(f"文件 '{file_path}' 中的内容不是有效的数字。")

# file_path = "lock.pid"  # PID文件路径
# file_pid = read_pid_from_file(file_path)
# if file_pid != pid:
#     print("文件中的数字是:", file_pid)
#     print("程序PID是:", pid)
import psutil

def get_process_name(pid):
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return f"进程ID为 {pid} 的进程不存在。"

pid = 10612  # 替换为你要查询的进程ID
process_name = get_process_name(pid)
print(f"进程ID为 {pid} 的程序名是: {process_name}")
