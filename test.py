#!/usr/bin/env python

## ---------------------------------------------------------------- ##
## Goal is to keep all the code into a single file that can be run
## as a script
## 

import wx
import types

EASY = 1001
HARD = 1002

CONDITIONS = {EASY : "easy", HARD : "hard",
              "easy" : EASY, "hard" : HARD}

class DualTaskPanel(wx.Panel):
    """A Dual Task object"""
    def __init__(self, parent, id):
        super(DualTaskPanel, self).__init__(parent=parent, id=id)
        self.task_name = None
        self.InitUI()

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

    def DisplayedWord(self):
        if self.condition == EASY:
            w = self.word
            l = len(w)
            i = self.index
            if i >= l:
                res = "#" * i + w[i:]
            else:
                res = "#" * l
            return res
    
        
    def InitUI(self):
        self.SetBackgroundColour("#FF5555")
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        text = wx.StaticText(self, -1, self.word)
        entry = wx.TextCtrl(self, -1)
        vbox.Add(text, wx.EXPAND|wx.ALL, 20)
        vbox.Add(entry, wx.EXPAND|wx.ALL)



class SubtractionTaskPanel(DualTaskPanel):

    def __init__(self, parent, id):
        super(SubtractionTaskPanel, self).__init__(parent=parent, id=id)

    def InitUI(self):
        self.SetBackgroundColour("#5555FF")    

        
class DualTaskFrame(wx.Frame):
    def __init__(self, parent, title):
        super(DualTaskFrame, self).__init__(parent, title=title, size=(800,400))
        self.InitUI()
        self.Centre()
        self.Show()

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
