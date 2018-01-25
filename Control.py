from Tkinter import *

class Control(Canvas):
    def __init__(self,parent):
        Canvas.__init__(self,parent)
        #player menu
        self.var = StringVar(self)
        self.var.set("start")  # initial value
        self.option = OptionMenu(self, self.var, "start", "goal", "wall")
        self.option.config(height=3, width=8)
        self.option.grid(row=3, column=0)
        #heuristic menu
        self.var1 = StringVar(self)
        self.var1.set("Manhatten") # initial value
        self.option1 = OptionMenu(self, self.var1, "Manhatten", "Euclidean")
        self.option1.config(height=3, width=8)
        self.option1.grid(row=4, column=0)
        #buttons
        self.runButton = Button(self, text="RUN", bg="green", height=3, width=10)
        self.runButton.grid(row=0, column=0)
        self.clearButton = Button(self, text="CLEAR ALL", bg="orange", height=3, width=10)
        self.clearButton.grid(row=1, column=0)
        self.quitButton = Button(self, text="QUIT", bg="red", height=3, width=10)
        self.quitButton.grid(row=2, column=0)