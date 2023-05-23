import tkinter as tk
from src.tKot.buttons import StatusIcon
from src.tKot.common import Point
from PIL import Image


root = tk.Tk()
c = tk.Canvas(root)
c.pack()
on_image = Image.open("../data/relay_on2.png")
off_image = Image.open("../data/relay_off2.png")
s_icon = StatusIcon(c, {1: on_image, 2: off_image})
s_icon.set_size(Point(100, 100)*2)
s_icon.place(10, 10)
root.after(2000, lambda: s_icon.set_status(2))
root.after(4000, lambda: s_icon.set_status(1))
root.mainloop()
