import tkinter
from tkinter import *


# This program is designed to count up from zero
class CountsUp(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.grid()
        self.widgets()
        self.running = False
        self.timer = [0,0,0]    # [minutes ,seconds, centiseconds]
        self.timeString = str(self.timer[0]) + ':' + str(self.timer[1]) + ':' + str(self.timer[2])
        self.update_time()

    def widgets(self):
        self.timeFrame = LabelFrame(root, text='Counts Up')
        self.timeFrame.grid(row=0,column=0, sticky=W)

        self.resetButton = Button(self.timeFrame, text='Reset', command=self.resetTime)
        self.resetButton.grid(row=2,column=1)

        self.pauseButton = Button(self.timeFrame, text='Pause', command=self.pause)
        self.pauseButton.grid(row=1,column=1)

        self.startButton = Button(self.timeFrame, text='Start', command=self.start)
        self.startButton.grid(row=0,column=1)

        self.show = Label(self.timeFrame, text='00:00:00', font=('Helvetica', 30))
        self.show.grid(row=0, column=0)

        self.quit = Button(self.timeFrame, text='QUIT', command=self.quit)
        self.quit.grid(row=3, column=1)


    def update_time(self):

        if (self.running == True):      #Clock is running

            self.timer[2] += 1          #Count Down

            if (self.timer[2] >= 100):  #100 centiseconds --> 1 second
                self.timer[2] = 0       #reset to zero centiseconds
                self.timer[1] += 1      #add 1 second

            if (self.timer[1] >= 60):   #60 seconds --> 1 minute
                self.timer[0] += 1      #add 1 minute
                self.timer[1] = 0       #reset to 0 seconds

            self.timeString = str(self.timer[0]) + ':' + str(self.timer[1]) + ':' + str(self.timer[2])
            self.show.config(text=self.timeString)
        root.after(10, self.update_time)

    def start(self):            #Start the clock
        self.running = True
        print ("Clock Running...")

    def pause(self):            #Pause the clock
        self.running = False
        print ("Clock Paused")   

    def resetTime(self):        #Reset the clock
        self.running = False
        self.timer = [0,0,0]
        print ("Clock is Reset")  
        self.show.config(text='00:00:00')

    def quit(self):             #Quit the program
        root.destroy()



# This program is designed to count down from a starting time
class CountsDown(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.grid()
        self.widgets()
        self.running = False
        self.timer = [0,0,0]    # [minutes ,seconds, centiseconds]
        self.timeString = str(self.timer[0]) + ':' + str(self.timer[1]) + ':' + str(self.timer[2])
        self.update_time()

    def widgets(self):
        self.timeFrame = LabelFrame(root, text='Counts Down')
        self.timeFrame.grid(row=2,column=0, sticky=W)

        self.resetButton = Button(self.timeFrame, text='Reset', command=self.resetTime)
        self.resetButton.grid(row=2,column=1)

        self.pauseButton = Button(self.timeFrame, text='Pause', command=self.pause)
        self.pauseButton.grid(row=1,column=1)

        self.startButton = Button(self.timeFrame, text='Start', command=self.start)
        self.startButton.grid(row=0,column=1)

        self.show = Label(self.timeFrame, text='00:00:00', font=('Helvetica', 30))
        self.show.grid(row=0, column=0)

        self.addMinute = Button(self.timeFrame, text='Add Minute', command=self.addMinute)
        self.addMinute.grid(row=2,column=0)

        self.addSecond = Button(self.timeFrame, text='Add Second', command=self.addSecond)
        self.addSecond.grid(row=3,column=0)

        self.quit = Button(self.timeFrame, text='QUIT', command=self.quit)
        self.quit.grid(row=3, column=1)


    def update_time(self):

        if (self.running == True):      #Clock is running

            self.timer[2] -= 1          #Count Down

            if (self.timer[2] < 0):     #if centiseconds is negative
                self.timer[2] = 100     #reset to 100 centiseconds
                self.timer[1] -= 1      #subtract 1 second

            if (self.timer[1] < 0):     #if seconds is negative
                self.timer[1] = 60      #reset to 60 seconds
                self.timer[1] -= 1      #subtract 1 second
                self.timer[0] -= 1      #subtract 1 minute

            self.timeString = str(self.timer[0]) + ':' + str(self.timer[1]) + ':' + str(self.timer[2])
            self.show.config(text=self.timeString)
        root.after(10, self.update_time)



    def addMinute(self):
        self.timer[0] += 1
        self.timeString = str(self.timer[0]) + ':' + str(self.timer[1]) + ':' + str(self.timer[2])
        self.show.config(text=self.timeString)

    def addSecond(self):
        self.timer[1] += 1
        self.timeString = str(self.timer[0]) + ':' + str(self.timer[1]) + ':' + str(self.timer[2])
        self.show.config(text=self.timeString)

    def start(self):            #Start the clock
        self.running = True
        print ('Clock Running...')

    def pause(self):            #Pause the clock
        self.running = False
        print ('Clock Paused')    

    def resetTime(self):        #Reset the clock
        self.running = False
        self.timer = [0,0,0]
        print ('Clock is Reset')  
        self.show.config(text='00:00:00')

    def quit(self):             #Quit the program
        root.destroy()



root = tkinter.Tk()

up = CountsUp(root)
down = CountsDown(root)

root.mainloop()