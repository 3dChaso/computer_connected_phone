import os
import wmi
import pystray
from PIL import Image
import time
import ctypes
from searchMyPhone import DeviceManager

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
device_manager = DeviceManager()# 创建 DeviceManager 实例
# 检测程序----------------------------------------------------------------------------
def start_checking():
    keep_checking = True
def check_device():
    device_manager.contains_device(DeviceName)


# 菜单方案----------------------------------------------------------------------------
def on_quit_callback(icon):
    remove_lock()
    icon.stop()

def on_option1_selected(icon):
    icon.icon = icon_link_icon
    icon.title = "连接正常"
    icon.notify("Notification", "This is a notification message.")   # 提示气泡

def on_option2_selected(icon):
    icon.icon = icon_unlink_icon
    icon.title = "连接失败"
    icon.notify("Notification", "This is a notification message.")   # 提示气泡
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
