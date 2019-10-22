import tkinter as tk

print("Start Program")
def onclick():
	print("Dilli Smells")
	#print message to textbox
	#Take away the "I am a button"
	#

root = tk.Tk() #builds your main wind
#Widget/Element is an element in a GUI
#Button, Textbox, Input box, Slider, drop down,
#Image,
#Step 1: Construct the widget.
btn1 = tk.Button(root, width = 20, height = 3)
#Step 2: Configure the widget.
btn1.config(text = "I am a button")
#Step 3: Place the widget - pack(), grid(),
btn1.pack()

output = tk.Text(root, width = 50, height = 20)
output.config()
output.pack();

btn2 = tk.Button(root, text ="Click For Secret", command = onclick, width = 15, height = 3)

btn2.config()
btn2.pack()


root.mainloop()

print("END PROGRAM")