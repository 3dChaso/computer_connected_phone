import tkinter as tk
import pygetwindow as gw
import sys
import time
import wmi
import ctypes
import threading


target_window = None

class DeviceCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("Device Check")
        master.geometry("260x180")
        master.resizable(False, False)  # 设置主窗口大小不可调整
        master.attributes('-topmost', True)  # 置顶窗口
        self.c = wmi.WMI()
        self.result =  False

        # 设备名称
        self.DeviceName = "Apple iPhone"

        # 设置全局变量来控制循环
        self.keep_checking = False

        # 添加标题控件，并设置默认文字和颜色
        self.title_label = tk.Label(master, text="等待检测", font=("Helvetica", 15), fg="gray")
        self.title_label.pack(pady=10)

        # 添加按钮，并直接绑定 start_checking() 函数
        self.btn_check = tk.Button(master, text="开始检测", command=self.start_checking)
        self.btn_check.pack(pady=10)

        # 添加设备名称标签
        self.device_label_2 = tk.Label(master, text="检测："+self.DeviceName)
        self.device_label_2.pack(pady=10)
#----------------------------------------------------------------------------------------------------------------#
    def get_connected_devices(self):
        # 查询所有连接到计算机的设备
        devices = self.c.Win32_PnPEntity()
        
        # 创建一个列表来存储设备信息
        equipment = []
        
        # 将设备信息存储在equipment列表中
        for device in devices:
            if device.Name is not None:
                equipment.append(device.Name)
        return equipment

    def contains_device(self, device_name):
        # 获取所有连接到计算机的设备名称
        connected_devices = self.get_connected_devices()
        self.result =  False
        # 判断是否有指定设备名称连接到计算机
        for device in connected_devices:
            if device_name in device:
                self.result =  True
    def lock_screen(self):
        # 使用Windows API锁定屏幕
        ctypes.windll.user32.LockWorkStation()
    
#----------------------------------------------------------------------------------------------------------------#
    def check_device(self):
        while self.keep_checking:
            # 判断是否有设备连接到计算机
            self.contains_device(self.DeviceName)
            print("Result:", self.result)
            # 设置标题文字和颜色
            if self.result:
                self.title_label.config(text="正常连接", fg="green")
            else:
                self.title_label.config(text="连接失败", fg="red")
                # 当检测到连接失败时，停止循环并延迟3秒后锁定屏幕
                self.keep_checking = False
                self.btn_check.config(state=tk.NORMAL)
                self.btn_check.config(text="开始检测")
                self.master.after(3000, self.lock_screen)
            # 每1秒执行一次 check_device()
            time.sleep(1)

    def start_checking(self):
        self.keep_checking = True
        self.btn_check.config(state=tk.DISABLED)
        self.btn_check.config(text="检测中..")
        added_thread = threading.Thread(target=self.check_device)
        added_thread.start()
        # result =added_thread.result()
        # self.check_device()
    def threadingtest(self):
        while True:
            result = self.contains_device(self.DeviceName)
            print("Result:", result)

# 获取所有当前打开的窗口
def activate_window(window_title):
    windows = gw.getAllWindows()
    # 在窗口列表中查找匹配标题的窗口
    global target_window
    for window in windows:
        if window.title == window_title:
            target_window = window
            break
    if target_window:
        return(False)
    else:
        return(True)

#----------------------------------------------------------------------------------------------------------------#
        
if __name__ == "__main__":
    if activate_window("Device Check"):
        root = tk.Tk()
        app = DeviceCheckerApp(root)
        root.mainloop()  

    else:
        # 激活目标窗口
        target_window.activate()      
        sys.exit("窗口 'Device Check' 存在！")  

