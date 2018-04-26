#!/usr/bin/env python

## ---------------------------------------------------------------- ##
## Goal is to keep all the code into a single file that can be run
## as a script
## 

import wx
import types
import string

EASY = 1001
HARD = 1002

CONDITIONS = {EASY : "easy", HARD : "hard",
              "easy" : EASY, "hard" : HARD}

class Logger():
    """Logs responses onto a file"""
    def __init__(self, filename):
        if filename is not None:
            self.log = open(filename, "w")
        
    def LogData(self, data):
        pass
    

class DualTaskPanel(wx.Panel):
    """A Dual Task object"""
    def __init__(self, parent, id):
        super(DualTaskPanel, self).__init__(parent=parent, id=id)
        self.task_name = None
        self.monofont = wx.Font(16, wx.FONTFAMILY_TELETYPE,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_BOLD)
        self.InitUI()
        self.logger = Logger(None)


    def RegisterResponse(self, response):
        """Registers a response"""
        pass
        
    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, val):
        if val == EASY or val == HARD:
            self._condition = val
        
    @property
    def task_name(self):
        return self._task_name

    @task_name.setter
    def task_name(self, val):
        self._task_name = val

    def InitUI(self):
        """Does nothing, really"""
        print("Test?")

        
class TypingTaskPanel(DualTaskPanel):
    """A panel for the Typing Task"""
    def __init__(self, parent, id, word = None, condition = EASY):
        #self.index = 0
        self.word = word
        self.condition = condition
        super(TypingTaskPanel, self).__init__(parent=parent, id=id)

            
    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        if type(val) == int and self.word is not None:
            self._index = val
        else:
            self._index = -1

    @property
    def word(self):
        """Returns the internal string representation"""
        return self._word

    @word.setter
    def word(self, val):
        """Sets the word. Value needs to be a string or None"""
        if type(val) == str:
            self._word = val
            self.index = 0
        elif val == None:
            self._word = ""
            self.index = -1

        
    def InitUI(self):
        self.SetBackgroundColour("#FF5555")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(hbox)

        text = wx.StaticText(self, -1, self.word)
        text.SetFont(self.monofont)
        
        entry = wx.TextCtrl(self, -1)
        entry.SetFont(self.monofont)
        vbox.Add(text, wx.BOTTOM, 20)
        vbox.Add(entry, wx.CENTRE, 20)

        keyboard = wx.Panel(self, -1)
        ksizer = wx.GridSizer(6, 5, 5, 5)
        keyboard.SetSizer(ksizer)
        
        for letter in string.ascii_uppercase:
            b = wx.Button(keyboard, -1, letter)
            b.SetFont(self.monofont)
            ksizer.Add(b, 20)

        vbox.Add(keyboard, wx.TOP, 20)
        hbox.Add(vbox)

        self.Bind(wx.EVT_BUTTON,  self.OnButton)

    def OnButton(self, event):
        print(event.GetEventObject().GetLabel())

class SubtractionTaskPanel(DualTaskPanel):

    def __init__(self, parent, id):
        super(SubtractionTaskPanel, self).__init__(parent=parent, id=id)

    def InitUI(self):
        self.SetBackgroundColour("#5555FF")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(hbox)

        text1 = wx.StaticText(self, -1, "1234567890")
        text1.SetFont(self.monofont)
        text2 = wx.StaticText(self, -1, "0123456789")
        text2.SetFont(self.monofont)
        entry = wx.TextCtrl(self, -1)
        entry.SetFont(self.monofont)
        vbox.Add(text1, wx.CENTRE, 20)
        vbox.Add(text2, wx.CENTRE, 20)
        vbox.Add(entry, wx.CENTRE)

        keyboard = wx.Panel(self, -1)
        ksizer = wx.GridSizer(2, 5, 5, 5)
        keyboard.SetSizer(ksizer)
        
        for digit in string.digits:
            b = wx.Button(keyboard, -1, digit)
            b.SetFont(self.monofont)
            ksizer.Add(b, 20)

        vbox.Add(keyboard)
        hbox.Add(vbox, wx.ALIGN_CENTRE)

        
class DualTaskFrame(wx.Frame):
    def __init__(self, parent, title):
        super(DualTaskFrame, self).__init__(parent, title=title, size=(800,400))
        self.InitUI()
        self.Centre()
        self.Show()

    def InitLetterButtons(self):
        pass
        
    def InitUI(self):
        "Does the layout"
        mainpanel = wx.Panel(self)
        mainbox = wx.BoxSizer(wx.HORIZONTAL)
        
        typing = TypingTaskPanel(mainpanel, -1, word="Dolicocephalus")
        mainbox.Add(typing, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        subtraction = SubtractionTaskPanel(mainpanel, -1)
        mainbox.Add(subtraction, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        mainpanel.SetSizer(mainbox)

 
        
if __name__ == "__main__":
    app = wx.App()
    e = DualTaskFrame(None, "Dual Task")
    app.MainLoop()
