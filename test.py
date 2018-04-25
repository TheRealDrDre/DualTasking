#!/usr/bin/env python

import wx

class DualTaskPanel(wx.Panel):
    """A Dual Task object"""
    def __init__(self, parent, id):
        super(DualTaskPanel, self).__init__(parent=parent, id=id)
        self.task_name = None
        self.InitUI()

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
    
    def __init__(self, parent, id):
        super(TypingTaskPanel, self).__init__(parent=parent, id=id)


    def InitUI(self):
        self.SetBackgroundColour("#FF5555")


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
        
        typing = TypingTaskPanel(mainpanel, -1)
        mainbox.Add(typing, 1, wx.EXPAND | wx.ALL, 10)
        
        subtraction = SubtractionTaskPanel(mainpanel, -1)
        mainbox.Add(subtraction, 1, wx.EXPAND | wx.ALL, 10)

        mainpanel.SetSizer(mainbox)
 
        
if __name__ == "__main__":
    app = wx.App()
    e = DualTaskFrame(None, "Dual Task")
    app.MainLoop()
