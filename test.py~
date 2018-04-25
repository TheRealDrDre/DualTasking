#!/usr/bin/env python

import wx

class DualTask():
    """A Dual Task object"""
    def __init__(self):
        self.task_name = None

    @property
    def task_name(self):
        return self._task_name

    @task_name.setter
    def task_name(self, val):
        self._task_name = val

class TypingTaskPanel(wx.Panel):
    
    def _init__(self):
        pass


class SubtractionTaskPanel(wx.Panel):
    def __init__(self):
        pass
    
        
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
        
        typing = wx.Panel(mainpanel, -1)
        typing.SetBackgroundColour("#ee1111")
        mainbox.Add(typing, 1, wx.EXPAND | wx.ALL, 10)
        
        subtraction = wx.Panel(mainpanel, -1)
        subtraction.SetBackgroundColour("#11ee11")
        mainbox.Add(subtraction, 1, wx.EXPAND | wx.ALL, 10)

        mainpanel.SetSizer(mainbox)
 
        
if __name__ == "__main__":
    app = wx.App()
    e = DualTaskFrame(None, "Dual Task")
    app.MainLoop()
