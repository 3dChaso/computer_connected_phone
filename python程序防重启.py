import tkinter as tk
import threading

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Threaded Button Example")

        self.button = tk.Button(self.master, text="Click Me", command=self.run_in_thread)
        self.button.pack()

    def run_in_thread(self):
        thread = threading.Thread(target=self.long_running_task)
        thread.start()

    def long_running_task(self):
        # 模拟长时间运行的任务
        import time
        time.sleep(3)
        print("Long running task completed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
