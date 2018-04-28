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
EMPTY_STRING = ""

CONDITIONS = {EASY : "easy", HARD : "hard",
              "easy" : EASY, "hard" : HARD}

class Logger():
    """Logs responses onto a file"""
    def __init__(self, pname=None):
        self.log = None
        if pname is not None:
            self.log = open(pname, "w")

        self.stddata = []

    @property
    def stddata(self):
        """Standard set of data to save for every row"""
        return self._stddata

    @stddata.setter
    def stddata(self, val):
        """Standard set of data to save for every row"""
        if type(val) == list:
            self._stddata = val
        else:
            self._stdata = [val]
    
    def LogData(self, data):
        """logs a standard row of data in file"""
        row = self.stddata + data 
        for j in row[-1]:
            self.log.write("%s\t" % j)
        self.log.write("%s\n" % j)
    

class DualTaskPanel(wx.Panel):
    """A Dual Task object"""
    def __init__(self, parent, id, condition = EASY):
        super(DualTaskPanel, self).__init__(parent=parent, id=id)
        self.task_name = None
        self.index = 0
        self.condition = condition
        self.monofont = wx.Font(16,
                                wx.FONTFAMILY_TELETYPE,  # Monospace
                                wx.FONTSTYLE_NORMAL,     # Not slanted
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

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        if type(val) == int:
            self._index = val
        else:
            self._index = -1

        
class TypingTaskPanel(DualTaskPanel):
    """A panel for the Typing Task"""
    def __init__(self, parent, id, word = None, condition = EASY):
        #self.index = 0
        self.word = word
        self.condition = condition
        super(TypingTaskPanel, self).__init__(parent=parent, id=id)
        self.SetUp()


    @property
    def word(self):
        """Returns the internal word that is displayed."""
        return self._word

    @word.setter
    def word(self, val):
        """
        Sets the word. Value will be converted to uppercase string 
        or to empty string if None.
        """
        if type(val) == str:
            self._word = val.upper()
            self.index = 0
            
        elif val == None:
            self._word = EMPTY_STRING
            self.index = -1
            
        else:
            res = "%s" % val
            self._word = res.upper()

        
    def InitUI(self):
        """Does the layout of the panel."""
        self.SetBackgroundColour("#FF5555")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(hbox)

        entry = wx.TextCtrl(self, -1)
        entry.SetFont(self.monofont)
        vbox.Add(entry, wx.CENTRE, 20)

        keyboard = wx.Panel(self, -1)
        keys = []
        ksizer = wx.GridSizer(6, 5, 5, 5)
        keyboard.SetSizer(ksizer)
        
        for letter in string.ascii_uppercase:
            b = wx.Button(keyboard, -1, letter)
            b.SetFont(self.monofont)
            ksizer.Add(b, 20)
            keys.append(b)

        vbox.Add(keyboard, wx.TOP, 20)
        hbox.Add(vbox)

        # Save the internal components
        self.keys = keys
        self.entry = entry
        
        self.Bind(wx.EVT_BUTTON,  self.OnButton)

    def SetUp(self):
        """Correctly sets up the panel according to the condition"""
        if self.index >= 0:
            if self.condition == EASY:
                letter = self.word[self.index]
                print(letter)
                self.entry.SetValue(letter)
            elif self.condition == HARD:
                if self.index == 0:
                    self.entry.SetValue(self.word)
                else:
                    self.entry.SetValue(EMPTY_STRING)
            else:
                # Throw an exception
                pass

    def OnButton(self, event):
        """Updates the panel after pressing one of the buttons"""
        letter = event.GetEventObject().GetLabel()
        self.index += 1
        self.SetUp()
        
class SubtractionTaskPanel(DualTaskPanel):
    def __init__(self, parent, id,
                 numbers = ("1234567890", "0123456780"),
                 condition = EASY):
        self.SetNumbers(numbers)
        super(SubtractionTaskPanel, self).__init__(parent=parent, id=id,
                                                   condition=condition)
        
    @property
    def size(self):
        return len(self.number1)
        
    def SetNumbers(self, tpl):
        """Sets the internal numbers for subtraction"""
        self.number1 = tpl[0]
        self.number2 = tpl[1]

        # Convert
        n1 = int(self.number1)
        n2 = int(self.number2)
        
        # Calculate solution
        s = n1 - n2
        
        self.solution = "%.10d" % s

        
    def InitUI(self):
        """Set up the panel UI"""
        self.SetBackgroundColour("#5555FF")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(hbox)

        text1 = []   # Upper number
        text2 = []   # Lower number
        
        for j in range(self.size):
            text1.append(wx.StaticText(self,
                                       -1,
                                       self.number1[j]))

        for j in range(self.size):
            text2.append(wx.StaticText(self,
                                       -1,
                                       self.number2[j]))

        text1.append(wx.StaticText(self, -1, "-"))
        text2.append(wx.StaticText(self, -1, "="))
            
        nsizer = wx.GridSizer(2, self.size + 1, 5, 5)
        allt = text1 + text2
        
        for t in allt:
            t.SetFont(self.monofont)
            nsizer.Add(t, 5)

        vbox.Add(nsizer)
        
        entry = wx.TextCtrl(self, -1)
        entry.SetFont(self.monofont)
        entry.SetSize((50, 800))
        
        vbox.Add(entry, wx.EXPAND | wx.LEFT | wx.RIGHT)

        keyboard = wx.Panel(self, -1)
        ksizer = wx.GridSizer(2, 5, 5, 5)
        keyboard.SetSizer(ksizer)
        
        for digit in string.digits:
            b = wx.Button(keyboard, -1, digit)
            b.SetFont(self.monofont)
            ksizer.Add(b, 20)

        vbox.Add(keyboard)
        hbox.Add(vbox, wx.ALIGN_CENTRE)

        # Save all the elements
        self.entry = entry
        self.text1 = text1
        self.text2 = text2
        self.keyboard = keyboard
        
        self.Bind(wx.EVT_BUTTON,  self.OnButton)


    def SetUp(self):
        """Correctly sets up the panel according to the condition"""
        if self.index >= 0:
            if self.condition == EASY:
                self.entry.SetValue("#" * self.index)
            elif self.condition == HARD:
                self.entry.SetValue(EMPTY_STRING)
            else:
                # Throw an exception
                pass

    def OnButton(self, event):
        """Updates the panel after pressing one of the buttons"""
        digit = event.GetEventObject().GetLabel()
        self.index += 1
        self.SetUp()

        
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
        
        typing = TypingTaskPanel(mainpanel, -1,
                                 word = "Dolicocephalus",
                                 condition = EASY)
        mainbox.Add(typing, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        subtraction = SubtractionTaskPanel(mainpanel, -1)
        mainbox.Add(subtraction, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        mainpanel.SetSizer(mainbox)

 
        
if __name__ == "__main__":
    app = wx.App()
    e = DualTaskFrame(None, "Dual Task")
    app.MainLoop()
