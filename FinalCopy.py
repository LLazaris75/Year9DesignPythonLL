import tkinter as tk
from tkinter import *
#Main Code:
root = tk.Tk()
#Building widgets goes before mainloop.

title = tk.Label(root, text = "Traffic Tracker", font=("Arial", 30))
title.config(fg = "blue", bg = "white")
title = tk.label(root, width = 50, height = 5)
title.pack(fill = tk.BOTH)
 #builds your main wind
#Widget/Element is an element in a GUI
#Button, Textbox, Input box, Slider, drop down,
#Image,
#Step 1: Construct the widget.
btn1 = tk.Button(root, width = 20, height = 3)
#Step 2: Configure the widget.
btn1.config(text = "Fast")
#Step 3: Place the widget - pack(), grid(),
btn1.pack()

btn2 = tk.Button(root, text ="Slow", command = onclick, width = 15, height = 3)

btn2.config()
btn2.pack()


root.mainloop()
print("End Program")




