import os
import wmi
import pystray
from PIL import Image
import ctypes
import time
import sys
import threading
from searchMyPhone import DeviceManager
import signal
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
blink_icon = False #闪烁图标状态
connection_status = 2 # 连接状态 1为连接，0为断开，2为默认
temp_connection_status = 2 # 临时连接状态
c = wmi.WMI()
# 调用Windows平台上的消息框
MessageBox = ctypes.windll.user32.MessageBoxW
icon_default_icon = Image.open("./default.png") 
icon_link_icon = Image.open("./link.png")
icon_unlink_icon = Image.open("./unlink.png") 
icon = pystray.Icon("example_icon", icon_default_icon, "等待中")
device_manager = DeviceManager()# 创建 DeviceManager 实例
# 检测程序----------------------------------------------------------------------------
def check_device():
    global connection_status
    while True:
        connection_status = device_manager.contains_device(DeviceName) # 更新连接状态
        # print(connection_status)
        time.sleep(1)
# 读取更新状态---------------------------------------------------------------------------- 
def updataState():#图标更新状态
    global temp_connection_status
    global blink_icon
    while True:
        if temp_connection_status != connection_status:
            if connection_status == 1 :
                temp_connection_status = connection_status
                blink_icon = False
                on_option1_selected(icon)             
            else:
                temp_connection_status = connection_status
                blink_icon = True
                on_option2_selected(icon)
        time.sleep(1)
# 菜单方案----------------------------------------------------------------------------
def on_quit_callback(icon): # 退出
    remove_lock()
    icon.stop()
    os.kill(pid, signal.SIGTERM)

def on_option1_selected(icon):
    icon.icon = icon_link_icon
    icon.title = "连接正常"
    icon.notify("连接正常", "检测到连接的："+DeviceName)   # 提示气泡
def on_option2_selected(icon):
    icon.icon = icon_unlink_icon
    icon.title = "连接失败"
    icon.notify("连接失败", "没有检测到电脑连接："+DeviceName)   # 提示气泡
    b = threading.Thread(target=blinkicon, )
    b.start()
    device_manager.lock_screen()

# 图标闪烁----------------------------------------------------------------------------
def blinkicon():
    while blink_icon:
        if blink_icon:
            icon.visible = not icon.visible
            time.sleep(0.5)  # 闪烁间隔为0.5秒
        else:
            icon.visible = True
            return
    
# 主程序----------------------------------------------------------------------------
def main():
    #程序锁
    if is_already_running():
        MessageBox(None, '检测程序已经启动了，不需重复启动', '程序已经运行', 0)
        sys.exit(1)
    create_lock()
    # 创建图标
    # 创建菜单项
    # menu_item1 = pystray.MenuItem("连接状态显示", on_option1_selected)
    menu_quit = pystray.MenuItem("退出", on_quit_callback)
    # 构建菜单
    icon.menu = pystray.Menu(menu_quit)
    # 显示图标进程
    t = threading.Thread(target=icon.run, )
    t.start()
    # 读取状态进程
    w = threading.Thread(target=updataState, )
    w.start()
    # 开始检测
    MessageBox(None, '请连接你的手机', '检测程序运行中....', 0)
    check_device()
if __name__ == "__main__":
    main()
