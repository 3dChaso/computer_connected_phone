import os
import wmi
import pystray
from PIL import Image
import time
import ctypes

# 程序锁----------------------------------------------------------------------------
LOCK_FILE = "lock.pid"
def create_lock():
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def remove_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def is_already_running():
    return os.path.isfile(LOCK_FILE)
# 初始化变量----------------------------------------------------------------------------
pid = os.getpid() # 本程序的PID
DeviceName = "Apple iPhone"
keep_checking = False
c = wmi.WMI()
# 检测程序----------------------------------------------------------------------------
def start_checking():
    keep_checking = True
    check_device()

def check_device():
    while keep_checking:
            # 判断是否有设备连接到计算机
            contains_device(DeviceName)
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
 # 系统设备检测----------------------------------------------------------------------------           
    def get_connected_devices():
        # 查询所有连接到计算机的设备
        devices = c.Win32_PnPEntity()
        
        # 创建一个列表来存储设备信息
        equipment = []
        
        # 将设备信息存储在equipment列表中
        for device in devices:
            if device.Name is not None:
                equipment.append(device.Name)
        return equipment

    def contains_device(device_name):
        # 获取所有连接到计算机的设备名称
        connected_devices = get_connected_devices()
        return False
        # 判断是否有指定设备名称连接到计算机
        for device in connected_devices:
            if device_name in device:
                return True
            else:
                return False
    def lock_screen():
        # 使用Windows API锁定屏幕
        ctypes.windll.user32.LockWorkStation()

# 菜单方案----------------------------------------------------------------------------
def on_quit_callback(icon):
    remove_lock()
    icon.stop()

def on_option1_selected(icon):
    icon.icon = icon_link_icon
    icon.title = "连接正常"
    icon.notify("Notification", "This is a notification message.")   # 提示气泡

def on_option2_selected(icon):
    image = Image.open("unlink.png") 
    icon.title = "连接失败"

# 主程序----------------------------------------------------------------------------
def main():
    # 程序锁
    if is_already_running():
        print("程序已运行")
        return
    create_lock()
    # 创建图标
    global icon_default_icon, icon_link_icon,icon_unlink_icon
    icon_default_icon = Image.open("default.png") 
    icon_link_icon = Image.open("link.png")
    icon_unlink_icon = Image.open("unlink.png")

    icon = pystray.Icon("example_icon", icon_default_icon, "等待中")
    icon.menu = pystray.Menu(
        pystray.MenuItem("测试按钮1", on_option1_selected),
        pystray.MenuItem("测试按钮2", on_option2_selected),
        pystray.MenuItem("退出", on_quit_callback)
    )
    # 显示图标
    icon.run()
if __name__ == "__main__":
    main()
