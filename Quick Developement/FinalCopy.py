import tkinter as tk
from tkinter import *
import SW


#Next Step: When you enter a licence plate adn press enter the widget should disable iteslf. 

displayFrames = [] #Creates a list of frames
displayplates = [] #Creaties a list of plates labels
startTimers = [] #holds all the timers
displayEntries = [] #Creates a list of entries
displayTimers = [] # Creates a list of start timers. 
endTimers = []

canpos = [10]



def addCar(*args):
	canpos[0] = canpos[0] + 1
	displayFrames.append(Frame(root, width=950, height=100, bd=2, highlightbackground="blue"))
	displayFrames[len(displayFrames) - 1].grid(row=canpos[0], column=0, columnspan = 9, pady=25)
	
	displayplates.append(tk.Label(displayFrames[len(displayFrames) - 1], text = "Plate Number: "))
	displayplates[len(displayplates) - 1].grid(row = 0, column = 0)
	
	displayEntries.append(tk.Entry(displayFrames[len(displayFrames) - 1]))
	displayEntries[len(displayEntries) - 1].grid(row = 0, column = 1)

	startTimers.append(tk.Button(displayFrames[len(displayFrames) - 1], text = "Start Timer"))
	startTimers[len(startTimers) - 1].grid(row = 0, column = 2)

	displayTimers.append(tk.Canvas(displayFrames[len(displayFrames) - 1], width = 200, height = 20, bg = "red")) 
	displayTimers[len(displayTimers) - 1].grid(row = 0, column = 3)

	endTimers.append(tk.Button(displayFrames[len(displayFrames) - 1], text = "Stop Timer"))
	endTimers[len(startTimers) - 1].grid(row = 0, column = 4)


root = tk.Tk()

root.configure(bg = "#b3e0ff")

w = Label(root, text="Traffic Tracker", fg = "white", bg = "blue", font = "Verdana 30 bold", width = 50)
w.grid(row = 0, column = 0, columnspan = 9)


btn3 = tk.Button(root, width = 9, height = 3, fg = "#484f54", bg = "white", font = ("Arial", 15))
#Step 2: Configure the widget.
btn3.config(text = "Slow")
#Step 3: Place the widget - pack(), grid(),
btn3.grid(row=6, column=2)


btn4 = tk.Button(root, text ="Fast", width = 9, height = 3, fg = "#3b3b3b", bg = "#484f54", font = ("Arial", 15))

btn4.config()
btn4.grid(row=6, column=3)
#Build the inside of one canvas
btn1 = tk.Button(root, width = 10, height = 5, fg = "blue", bg = "#3b3b3b", command = addCar, font = ("Arial", 25))
#Step 2: Configure the widget.
btn1.config(text = "+")
#Step 3: Place the widget - pack(), grid(),
btn1.grid(row=6, column=6)


btn2 = tk.Button(root, text ="-", width = 10, height = 5, fg = "red", bg = "white", font = ("Arial", 25))

btn2.config()
btn2.grid(row=6, column=7, pady=30)

root.mainloop()