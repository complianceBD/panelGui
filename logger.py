import wx
import os

# Following functions are the application
# ---------------------------------------

def availdays():
        # list out all the server logs files available for analysis
        # (this is used within the pulldown menu)
        days = []
        for option in os.listdir("."):
                if option.startswith("ac_201"):
                        days.append(option)
        return days

def analyse(filename):
        # When the "Analyse" button is pressed, this code is called.
        # It returns a summary report from the log file who's name is passed in
        count = 0
        ok = 0
        fail = 0
        for lyne in open(filename).xreadlines():
                fol = lyne.split(" ")
                try:
                        status = int(fol[8])
                        if status < 300:
                                ok += 1
                        else:
                                fail += 1
                except:
                        pass
                count += 1
        report = "\n"
        report += "total count %7d\n" % count
        report += "ok count    %7d\n" % ok
        report += "fail count  %7d\n" % fail
        return report

# Following class defines the GUI
# -------------------------------

class Form1(wx.Panel):

# look and feel of the window

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.topbit = wx.StaticText(self, -1,
                "Log file report for chosen day",wx.Point(20, 30))
        self.sampleList = availdays()
        self.bo=wx.ComboBox(self, 30, "", wx.Point(50, 60),
                wx.Size(125, -1), self.sampleList, wx.CB_DROPDOWN)
        self.button = wx.Button(self, 10, "Analyse", wx.Point(50, 100))
        self.leaver = wx.Button(self, 11, "Quit", wx.Point(50, 130))
        self.logger = wx.TextCtrl(self,5, "",wx.Point(230,20), wx.Size(200,140),\
                wx.TE_MULTILINE |  wx.TE_READONLY)
        wx.EVT_BUTTON(self, 10, self.OnClick)
        wx.EVT_BUTTON(self, 11, self.OnClick)
        wx.EVT_COMBOBOX(self, 30, self.EvtComboBox)
        parent.SetTitle("Analysis of web server log file")
        self.currentselectedfile = None

# Action when pulldown menu selection made

    def EvtComboBox(self, event):
        self.currentselectedfile = event.GetString()

    def OnClick(self,event):

# Action on quit button

        if event.GetId() == 11:
                frame.Destroy()

# Action on analyse button

        self.logger.Clear()
        if self.currentselectedfile:
                self.logger.WriteText("Results for " + self.currentselectedfile+"\n" )
                self.logger.WriteText(analyse(self.currentselectedfile))
        else:
                self.logger.WriteText("You haven't chosen a file yet!")

# Main application ...

# Set up all the stuff for a wxPython application
app = wx.PySimpleApp()

# Add a top level frame, 450 x 225 pixels
frame = wx.Frame(None, size=(450,225))

# Draw a panel as defined by the Form1 class into that frame
Form1(frame)

# Display the frame and panel within it
frame.Show(1)

# Wait for events and process each one you receive
app.MainLoop()