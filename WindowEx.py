import tkinter as tk

class QQStatusApp:
    def __init__(self, master):
        self.master = master
        self.master.title("QQ Status")
        
        self.status = "default"  # 初始状态为默认
        
        self.status_label = tk.Label(self.master, text="Status: Default", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 设置状态栏更新定时器
        self.update_status()

    def update_status(self):
        if self.status == "default":
            self.status_label.config(text="Status: Default")
        elif self.status == "blink":
            self.status_label.config(text="Status: Blinking", bg="yellow")
            self.master.after(500, self.toggle_blink)  # 每500毫秒切换状态
        elif self.status == "bw_icon":
            self.status_label.config(text="Status: Black & White Icon", bg="gray")
        self.master.after(1000, self.update_status)  # 每1000毫秒更新一次状态

    def toggle_blink(self):
        if self.status == "blink":
            self.status = "default"
        else:
            self.status = "blink"
        self.update_status()

    def set_bw_icon_status(self):
        self.status = "bw_icon"
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    app = QQStatusApp(root)
    root.mainloop()
