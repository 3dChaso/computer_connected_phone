import tkinter as tk
from searchMyPhone import DeviceManager

# 创建 DeviceManager 实例
device_manager = DeviceManager()

# 设置全局变量来控制循环
keep_checking = False

def check_device():
    global keep_checking
    # 判断是否有 "Apple iPhone" 连接到计算机
    result = device_manager.contains_device("Apple iPhone")
    print("Result:", result)
    # 设置标题文字和颜色
    if result:
        title_label.config(text="正常连接", fg="green")
    else:
        title_label.config(text="连接失败", fg="red")
        # 当检测到连接失败时，停止循环并延迟3秒后锁定屏幕
        keep_checking = False
        root.after(3000, device_manager.lock_screen)
    # 每5秒执行一次 check_device()
    if keep_checking:
        root.after(5000, check_device)

def start_checking():
    global keep_checking
    keep_checking = True
    check_device()

def test():
    # 测试
    device_manager.lock_screen()

# 创建主窗口
root = tk.Tk()
root.title("Device Check")
root.geometry("150x200")
root.resizable(False, False)  # 设置主窗口大小不可调整
root.attributes('-topmost', True)  # 置顶窗口

# 添加标题控件，并设置默认文字和颜色
title_label = tk.Label(root, text="等待检测", font=("Helvetica", 18), fg="gray")
title_label.pack(pady=10)

# 添加按钮，并直接绑定 start_checking() 函数
btn_check = tk.Button(root, text="开始检测", command=start_checking)
btn_check.pack(pady=10)

btn_check = tk.Button(root, text="测试按钮", command=test)
btn_check.pack(pady=10)

# 运行界面循环
root.mainloop()
