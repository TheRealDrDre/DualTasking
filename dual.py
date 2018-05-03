#!/usr/bin/env python

## ---------------------------------------------------------------- ##
## Goal is to keep all the code into a single file that can be run
## as a script
## 

import wx
import types
import string
import time
import yaml

EASY = 1001
HARD = 1002
EMPTY_STRING = ""

CONDITIONS = {EASY : "easy", HARD : "hard",
              "easy" : EASY, "hard" : HARD}

class Trial:
    """An abstract representation of a trial"""
    def __init__(self, condition):
        self.condition = condition

class TypingTrial(Trial):
    """A typing task trial"""
    #def __init__(self, condition="easy", word=EMPTY_STRING):
    def __init__(self, **entries):
        self.__dict__.update(entries)
        #super(Trial, self).__init__(self, condition)
        #self.word = word


class SubtractionTrial(Trial):
    """A subtractiokn task trial"""
    def __init__(self, condition, number1, number2):
        super(Trial, self).__init__(self, condition)
        self.number1 = number1
        self.number2 = number2

class TrialManager:
    """An object that loads and manages a list of trials"""
    def __init__(self, fname="trials.yaml"):
        self.Load(fname)

    def Load(self, fname):
        """Loads a series of trials from a YAML file"""
        with open(fname, 'r') as stream:
            try:
                lst = yaml.load(stream)
                for j in lst:
                    tdic = j['typing']
                    z = TypingTrial(**tdic)
                    print(z)
            except yaml.YAMLError as exc:
                print(exc)
        
        
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
        if self.log is not None:
            for j in row[-1]:
                self.log.write("%s\t" % j)
            self.log.write("%s\n" % j)
            self.log.flush()

            
class ResponseEvent():
    """A Java-like event object that represents a subject's response"""
    def __init__(self, source, response, time=time.time(), correct=None, index=0):
        self.source = source        # The UI panel that generated it
        self.time = time            # The time at which it was generated
        self.response = response    # The subject's response
        self.correct = None         # What would have been the correct response
        self.index = index          # The index of the response

        
class DualTaskPanel(wx.Panel):
    """A Dual Task object"""
    def __init__(self, parent, id, condition = EASY):
        super(DualTaskPanel, self).__init__(parent=parent, id=id)
        self.task_name = None
        self.index = 0
        self.logger = None
        self.onset = time.time()
        self.condition = condition
        self.finished = False
        self.responseListeners = []
        self.monofont = wx.Font(16,
                                wx.FONTFAMILY_TELETYPE,  # Monospace
                                wx.FONTSTYLE_NORMAL,     # Not slanted
                                wx.FONTWEIGHT_BOLD)
        self.InitUI()
        self.logger = Logger(None)

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, b):
        if type(b) == bool:
            self._finished = b
        
    @property
    def active(self):
        """Returns whether a panel is currently active:"""
        return self._active


    @active.setter
    def active(self, status):
        """Activates or deactivates a panel"""
        if status == True or status == False:
            self._active = status
        
    def AddResponseListener(self, listener):
        """Adds an object to invoke when a response is made"""
        if not listener in self.responseListeners: 
            self.responseListeners.append(listener)
                

    def BroadcastResponse(self, response):
        """Invokes the ProcessResponse method of every listener"""
        for l in self.responseListeners:
            l.ProcessResponse(response)
        
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
        pass

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        if type(val) == int:
            self._index = val
        else:
            self._index = -1

    def ResponseCorrect(self, val):
        """Returns whether a response is correct"""
        return True

    def LogResponse(self, response):
        """Logs a response if the logger is enabled"""
        tme = time.time()
        rt = tme - self.onset 
        #diff = self.
        if self.logger is not None:
            data = [self.name,
                    CONDITIONS[self.condition],
                    response,
                    self.ResponseCorrect(response),
                    tme,
                    rt]
            self.logger.log(data)

            
class PointPanel(DualTaskPanel):
    def __init__(self, parent, id):
        self.pointthread = None
        super(PointPanel, self).__init__(parent = parent,
                                            id = id)
        self.points = 200

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, pnts):
        self._points = pnts
        self.Update()
        
    def InitUI(self):

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        vbox.Add((20, 20), wx.EXPAND | wx.ALL)
        text = wx.StaticText(self, -1, "Points:")
        text.SetFont(self.monofont)
        vbox.Add(text)
        points = wx.StaticText(self, -1, "---")
        points.SetFont(self.monofont)
        vbox.Add(points)

        self.ptext = points

    def SetUp(self):
        self.ptext.SetLabel("%d" % self.points)

        
class TypingTaskPanel(DualTaskPanel):
    """A panel for the Typing Task"""
    def __init__(self, parent, id, word = None, condition = EASY):
        #self.index = 0
        self.word = word
        self.condition = condition
        self.entry = None
        self.keys = None
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

    
    @property
    def correct_response(self):
        """Returns the correct response for a subtraction task"""
        if self.word is not None:
            return self.word[self.index]
        else:
            return None

            
    def InitUI(self):
        """Does the layout of the panel."""
        self.SetBackgroundColour("#FF5555")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hbox)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add((20, 20), wx.EXPAND)
        hbox.Add(vbox)
        hbox.Add((20, 20), wx.EXPAND)

        
        center = wx.Panel(self, -1)
        cbox = wx.BoxSizer(wx.VERTICAL)
        center.SetSizer(cbox)

        entry = wx.TextCtrl(center, -1)
        entry.SetFont(self.monofont)
        cbox.Add(entry, proportion=1, flag=wx.EXPAND | wx.ALL, border = 20)

        keyboard = wx.Panel(center, -1)
        keys = []
        ksizer = wx.GridSizer(6, 5, 5, 5)
        keyboard.SetSizer(ksizer)
        
        for letter in string.ascii_uppercase:
            b = wx.Button(keyboard, -1, letter)
            b.SetFont(self.monofont)
            ksizer.Add(b, 20)
            keys.append(b)

        cbox.Add(keyboard, 0, wx.EXPAND | wx.ALL, border = 20)


        vbox.Add((20, 20), wx.EXPAND)
        vbox.Add(center, wx.ALIGN_CENTRE)
        vbox.Add((20, 20), wx.EXPAND)
        
        # Save the internal components
        self.keys = keys
        self.entry = entry
        
        self.Bind(wx.EVT_BUTTON,  self.OnButton)

    @DualTaskPanel.active.setter
    def active(self, status):
        if self.entry is not None and self.keys is not None:
            if status == True:
                self.entry.Enable()
                for k in self.keys:
                    k.Enable()
                self.SetUp()
                self.onset = time.time()
            elif status == False:
                self.entry.Disable()
                self.entry.SetValue(EMPTY_STRING)
                for k in self.keys:
                    k.Disable()
        self._active = status

        
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
        tme = time.time()
        letter = event.GetEventObject().GetLabel()
        resp = ResponseEvent(self,
                             response=letter,
                             time=tme,
                             correct = self.correct_response,
                             index = self.index)
        self.BroadcastResponse(resp)
        self.index += 1



    
class SubtractionTaskPanel(DualTaskPanel):
    def __init__(self, parent, id,
                 numbers = ("1234567890", "0123456780"),
                 condition = EASY):
        self.SetNumbers(numbers)
        super(SubtractionTaskPanel, self).__init__(parent=parent, id=id,
                                                   condition=condition)

    @property
    def trial(self):
        return self._trial

    @trial.setter
    def trial(self, val):
        """Sets a new trial"""
        self.SetNumbers(val.number1, val.number2)

        
    @property
    def size(self):
        return len(self.number1)

    @DualTaskPanel.active.setter
    def active(self, status):
        if type(status) == bool:
            self._active = status
            if self.text1 is not None and \
            self.text2 is not None and \
            self.entry is not None:
                if status == False:
                    for t in self.text1:
                        t.Disable()
                        t.SetLabel("*")
                    for t in self.text2:
                        t.Disable()
                        t.SetLabel("*")
                    for k in self.keys:
                        k.Disable()
                    for t in self.text3:
                        t.Disable()
                        
                    self.entry.Disable()
                    self.entry.SetValue(EMPTY_STRING)

                if status == True:          
                    for d, t in zip(self.number1, self.text1):
                        t.Enable()
                        t.SetLabel(d)
                    for d, t in zip(self.number2, self.text2):
                        t.Enable()
                        t.SetLabel(d)
                    for t in self.text3:
                        t.Enable()
                    for k in self.keys:
                        k.Enable()
                        
                    self.entry.Enable()
                    self.SetUp()

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

    @property
    def correct_response(self):
        """Returns the correct response for a subtraction task"""
        if self.solution is not None:
            return self.solution[self.index]
        else:
            return None
        
    def InitUI(self):
        """Set up the panel UI"""
        self.SetBackgroundColour("#5555FF")
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(hbox)
        
        center = wx.Panel(self, -1)
        cvbox = wx.BoxSizer(wx.VERTICAL)
        center.SetSizer(cvbox)

        text1 = []   # Upper number
        text2 = []   # Lower number
        
        for j in range(self.size):
            text1.append(wx.StaticText(center,
                                       -1,
                                       self.number1[j],
                                       ))

        for j in range(self.size):
            text2.append(wx.StaticText(center,
                                       -1,
                                       self.number2[j]))

        #text1.append(wx.StaticText(center, -1, "-"))
        #text2.append(wx.StaticText(center, -1, "="))
            
        nsizer = wx.GridSizer(2, self.size, 0, 0)
        allt = text1 + text2

        ksizer = wx.GridSizer(2, 1, 0, 0)
        text3 = []
        for char in ["-", "="]:
            x = wx.StaticText(center, -1, char)
            x.SetFont(self.monofont)
            text3.append(x)
            ksizer.Add(x)
       
                   
        for t in allt:
            t.SetFont(self.monofont)
            nsizer.Add(t, 5)


        entry = wx.TextCtrl(center, -1, style=wx.TE_RIGHT)
        entry.SetFont(self.monofont)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(nsizer, 1, wx.ALIGN_RIGHT | wx.LEFT, border = 20)
        vbox1.Add(entry, proportion = 0, flag=wx.EXPAND | wx.BOTTOM, border = 20)
        
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(vbox1, 0, wx.ALIGN_RIGHT | wx.EXPAND, border=20)
        hbox1.Add(ksizer, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT, border=20)
        cvbox.Add(hbox1, 0, wx.ALIGN_RIGHT)
                
        keyboard = wx.Panel(center, -1)
        ksizer = wx.GridSizer(2, 5, 5, 5)
        keyboard.SetSizer(ksizer)
        keys = []
        
        for digit in string.digits:
            b = wx.Button(keyboard, -1, digit)
            b.SetFont(self.monofont)
            ksizer.Add(b, 20)
            keys.append(b)

        cvbox.Add(keyboard, 0, wx.EXPAND | wx.ALL, border = 20)

        vbox.Add((20, 20), wx.EXPAND)
        vbox.Add(center, wx.ALIGN_CENTER)
        vbox.Add((20, 20), wx.EXPAND)
        
        hbox.Add((20, 20), wx.EXPAND | wx.ALL)
        hbox.Add(vbox)
        hbox.Add((20, 20), wx.EXPAND | wx.ALL)
        
        # Save all the important elements in internal fields
        self.entry = entry
        self.text1 = text1
        self.text2 = text2
        self.text3 = text3
        self.keys = keys
        
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
        tme = time.time()
        digit = event.GetEventObject().GetLabel()
        resp = ResponseEvent(self,
                             response=digit,
                             time=tme,
                             correct = self.correct_response,
                             index = self.index)
        self.BroadcastResponse(resp)
        self.index += 1
        
        
class DualTaskFrame(wx.Frame):
    """The main experiment's window"""
    def __init__(self, parent, title):
        """The main panel"""
        super(DualTaskFrame, self).__init__(parent, title=title, size=(800,400))
        self.trials = TrialManager()
        self.InitUI()
        self.Centre()
        self.Show()

        
    def InitUI(self):
        "Does the layout"
        mainpanel = wx.Panel(self)
        mainbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        points = PointPanel(mainpanel, -1)
        typing = TypingTaskPanel(mainpanel, -1,
                                 word = "Dolicocephalus",
                                 condition = EASY)
        hbox.Add(typing, 1, wx.EXPAND | wx.LEFT, 10)
        typing.active = False
        typing.AddResponseListener(self)
        
        subtraction = SubtractionTaskPanel(mainpanel, -1)
        hbox.Add(subtraction, 1, wx.EXPAND | wx.RIGHT, 10)
        subtraction.active = True
        subtraction.AddResponseListener(self)

        #vbox.Add((20, 20), wx.EXPAND | wx.ALL)
        vbox.Add(points)
        vbox.Add(hbox)

        mainbox.Add((20, 20), wx.EXPAND | wx.ALL)
        mainbox.Add(vbox)
        mainbox.Add((20, 20), wx.EXPAND | wx.ALL)
        
        mainpanel.SetSizer(mainbox)

        self.typing = typing
        self.subtraction = subtraction
        self.points = points


    def ProcessResponse(self, event):
        source = event.source
        source.active = False
        if source == self.typing:
            self.subtraction.active = True
        elif source == self.subtraction:
            self.typing.active = True

            
if __name__ == "__main__":
    app = wx.App()
    e = DualTaskFrame(None, "Dual Task")
    app.MainLoop()
