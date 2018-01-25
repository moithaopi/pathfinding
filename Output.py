from Tkinter import *

class Output(Canvas):
    def __init__(self,parent):
        Canvas.__init__(self,parent)
        #result
        self.resultName = Label(self, text="RESULT: ", font=55)
        self.resultName.grid(row=0, column=0)
        self.result = Label(self,font=55)
        self.result.grid(row=0, column=1)
        #time
        self.timeName=Label(self,text="DURATION: ",font=55)
        self.timeName.grid(row=0, column=2)
        self.timeValue=Label(self,font=30)
        self.timeValue.grid(row=0, column=3)