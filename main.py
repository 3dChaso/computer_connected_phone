import tkinter as tk
from searchMyPhone import DeviceManager
import pygetwindow as gw
import sys

class DeviceCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("Device Check")
        master.geometry("260x180")
        master.resizable(False, False)  # 设置主窗口大小不可调整
        master.attributes('-topmost', True)  # 置顶窗口

        # 创建 DeviceManager 实例
        self.device_manager = DeviceManager()

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

    def check_device(self):
        # 判断是否有设备连接到计算机
        result = self.device_manager.contains_device(self.DeviceName)
        print("Result:", result)
        # 设置标题文字和颜色
        if result:
            self.title_label.config(text="正常连接", fg="green")
        else:
            self.title_label.config(text="连接失败", fg="red")
            # 当检测到连接失败时，停止循环并延迟3秒后锁定屏幕
            self.keep_checking = False
            self.btn_check.config(state=tk.NORMAL)
            self.btn_check.config(text="开始检测")
            self.master.after(3000, self.device_manager.lock_screen)
        # 每1秒执行一次 check_device()
        if self.keep_checking:
            self.master.after(1000, self.check_device)

    def start_checking(self):
        self.keep_checking = True
        self.btn_check.config(state=tk.DISABLED)
        self.btn_check.config(text="检测中..")
        self.check_device()

if __name__ == "__main__":
    # 获取所有打开的窗口
    window_titles = gw.getAllTitles()
    # 遍历所有窗口，检查是否有名为“Device Check”的窗口
    if "Device Check" in window_titles:
        # 退出程序
        sys.exit("窗口 'Device Check' 存在！")
    else:
        root = tk.Tk()
        app = DeviceCheckerApp(root)
        root.mainloop()

