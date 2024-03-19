import wmi
import ctypes
import time
class DeviceManager:
    def __init__(self):
        self.c = wmi.WMI()

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
        
        # 判断是否有指定设备名称连接到计算机
        for device in connected_devices:
            if device_name in device:
                return 1
        return 0

    def lock_screen(self):
        # 使用Windows API锁定屏幕
        time.sleep(3)
        ctypes.windll.user32.LockWorkStation()
