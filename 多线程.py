import time
import threading
import wmi
c = wmi.WMI()

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
    # 判断是否有指定设备名称连接到计算机
    for device in connected_devices:
        if device_name in device:
            input("找到了")

for i in range(1, 3):
    t = threading.Thread(target=contains_device, args=("Apple iPhone", ))
    t.start()