import tkinter as tk
import os
from searchMyPhone import DeviceManager

class DeviceChecker:
    def __init__(self):
        # 创建 DeviceManager 实例
        self.device_manager = DeviceManager()
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("Device Check")
        self.root.geometry("150x180")
        self.root.resizable(False, False)  # 设置窗口大小不可调整
        self.root.attributes('-topmost', True)  # 置顶窗口
        
        # 初始化界面组件
        self.create_widgets()
        
        # 初始化任务标识
        self.check_id = None
        self.countdown_id = None

    def create_widgets(self):
        # 添加标题标签
        self.title_label = tk.Label(self.root, text="等待检测", font=("Helvetica", 15), fg="gray")
        self.title_label.pack(pady=10)

        # 添加倒计时标签
        self.countdown_label = tk.Label(self.root, text="", font=("Helvetica", 12))

        # 添加检测连接按钮
        self.btn_check = tk.Button(self.root, text="检测连接", command=self.start_check)
        self.btn_check.pack(pady=10)

        # 添加停止检测按钮
        self.btn_stop = tk.Button(self.root, text="停止检测", command=self.stop_check)
        self.btn_stop.pack(pady=10)

    def check_device_loop(self):
        """循环检测设备连接状态"""
        self.check_device()
        if self.check_id is not None:
            self.check_id = self.root.after(10000, self.check_device_loop)

    def check_device(self):
        """检测设备连接状态"""
        result = self.device_manager.contains_device("Apple iPhone")
        print("Result:", result)
        if result:
            # 如果检测到设备连接，更新界面显示
            self.title_label.config(text="正常连接", fg="green")
            if self.countdown_id:
                self.root.after_cancel(self.countdown_id)
            self.countdown_label.pack_forget()
        else:
            # 如果检测到设备未连接，更新界面显示，并开始倒计时
            self.title_label.config(text="连接失败", fg="red")
            self.countdown_label.pack()
            self.start_countdown()
            if self.check_id:
                self.root.after_cancel(self.check_id)
            self.check_id = None

    def start_countdown(self):
        """开始倒计时"""
        self.countdown_remaining = 15
        self.update_countdown()

    def update_countdown(self):
        """更新倒计时"""
        if self.countdown_remaining > 0:
            self.countdown_label.config(text=f"锁屏倒计时：{self.countdown_remaining}秒")
            self.countdown_remaining -= 1
            self.countdown_id = self.root.after(1000, self.update_countdown)
        else:
            # 倒计时结束后执行锁屏操作，并恢复默认状态
            self.lock_screen()
            self.restore_default_state()

    def lock_screen(self):
        """锁定屏幕"""
        os.system("rundll32.exe user32.dll,LockWorkStation")

    def restore_default_state(self):
        """恢复默认状态"""
        self.title_label.config(text="等待检测", fg="gray")
        self.btn_check.config(state="normal")
        self.countdown_label.pack_forget()

    def start_check(self):
        """开始检测设备连接状态"""
        self.btn_check.config(state="disabled")
        self.check_device_loop()

    def stop_check(self):
        """停止检测设备连接状态"""
        self.root.after_cancel(self.check_id)
        if self.countdown_id:
            self.root.after_cancel(self.countdown_id)
        self.countdown_label.pack_forget()
        self.restore_default_state()

if __name__ == "__main__":
    app = DeviceChecker()
    app.root.mainloop()
