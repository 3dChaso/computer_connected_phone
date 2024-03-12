import tkinter as tk
import os
from searchMyPhone import DeviceManager

# 创建 DeviceManager 实例
device_manager = DeviceManager()

# 全局变量用于存储倒计时任务的标识
countdown_id = None
check_id = None  # 新增全局变量用于存储检测任务的标识

def check_device():
    global countdown_id, check_id
    # 判断是否有 "Apple iPhone" 连接到计算机
    result = device_manager.contains_device("Apple iPhone")
    print("Result:", result)
    # 设置标题文字和颜色
    if result:
        title_label.config(text="正常连接", fg="green")
        # 取消倒计时
        if countdown_id:
            root.after_cancel(countdown_id)
        # 隐藏计时器
        countdown_label.pack_forget()
    else:
        title_label.config(text="连接失败", fg="red")
        # 显示倒计时
        countdown_label.pack()
        # 开始倒计时
        start_countdown()
        # 取消后续的检测任务
        root.after_cancel(check_id)

def start_countdown():
    global countdown_remaining, countdown_id
    countdown_remaining = 15
    update_countdown()

def update_countdown():
    global countdown_remaining, countdown_id
    if countdown_remaining > 0:
        countdown_label.config(text=f"锁屏倒计时：{countdown_remaining}秒")
        countdown_remaining -= 1
        countdown_id = root.after(1000, update_countdown)
    else:
        # 倒计时结束后锁屏并恢复默认状态
        lock_screen()
        restore_default_state()

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def restore_default_state():
    # 恢复默认状态
    title_label.config(text="等待检测", fg="gray")
    # 恢复检测连接按钮
    btn_check.config(state="normal")
    # 隐藏倒计时组件
    countdown_label.pack_forget()


def start_check():
    # 禁用检测连接按钮
    btn_check.config(state="disabled")
    # 开始循环检测
    check_device()
    # 启动下一次检测
    global check_id
    check_id = root.after(10000, start_check)

def stop_check():
    global stop_clicked
    stop_clicked = True
    # 取消后续的检测任务和倒计时
    root.after_cancel(check_id)
    if countdown_id:
        root.after_cancel(countdown_id)  # 取消倒计时任务
    # 隐藏倒计时组件
    countdown_label.pack_forget()
    # 恢复默认状态
    restore_default_state()

# 创建主窗口
root = tk.Tk()
root.title("Device Check")
root.geometry("150x180")
root.resizable(False, False)  # 设置主窗口大小不可调整
root.attributes('-topmost', True)  # 置顶窗口

# 添加标题控件，并设置默认文字和颜色
title_label = tk.Label(root, text="等待检测", font=("Helvetica", 15), fg="gray")
title_label.pack(pady=10)

# 添加倒计时控件
countdown_label = tk.Label(root, text="", font=("Helvetica", 12))

# 添加检测连接按钮，并绑定 start_check() 函数
btn_check = tk.Button(root, text="检测连接", command=start_check)
btn_check.pack(pady=10)

# 添加停止检测按钮，并绑定 stop_check() 函数
btn_stop = tk.Button(root, text="停止检测", command=stop_check)
btn_stop.pack(pady=10)

# 变量用于跟踪是否点击了停止检测按钮
stop_clicked = False

# 运行界面循环
root.mainloop()
