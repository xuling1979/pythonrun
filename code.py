import tkinter as tk

# 创建主窗口
root = tk.Tk()
root.title("Hello Window")   # 窗口标题
root.geometry("300x100")     # 窗口大小

# 创建一个标签，显示 Hello
label = tk.Label(root, text="Hello", font=("Arial", 16))
label.pack(expand=True)      # 让标签居中显示

# 进入事件循环，显示窗口
root.mainloop()