import os
import wx
import wx.lib.agw.multidirdialog as MDD
class TabOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #--------------------Date input---------------------------
        dateText = wx.StaticText(self, label="Date use YYYY-MM-DD Format:   ")
        self.tc1 = wx.TextCtrl(self)
        #--------------------end date input ----------------------
        
        #---------------------File Input Browser-------------------------------
        #File Lcoation 
        fileLocText = wx.StaticText(self, label="File Location")
        self.tc2 = wx.TextCtrl(self, value='H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews\\Best Ex Mortgage\\BloombergFiles')
        inputButton = wx.Button(self, label="Browse...")
        #inputButton.Bind(wx.EVT_BUTTON, self.onDir)
        #---------------------File Output-------------------------------
        SaveLocText = wx.StaticText(self, label="Save Location")
        self.tc3 = wx.TextCtrl(self, value='H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews')

        outputButton = wx.Button(self, label="Browse...")
        #outputButton.Bind(wx.EVT_BUTTON, self.onDirSave)
        
        #--------------------Radio Buttons x3----------------------------
        
        self.radio1 = wx.RadioButton(self, label = 'Mortgage Best Ex')
        self.radio2 = wx.RadioButton(self, label = 'Treasury Best Ex')
        self.radio3 = wx.RadioButton(self, label = 'Wash Sale Report Bloomberg')
        
        #------------------help and run ----------------------------------
        helpButton = wx.Button(self, label='Help')

        runButton = wx.Button(self, label="Run")
        #runButton.Bind(wx.EVT_BUTTON, self.onOk)
        #------------------------------auto run----------------------------------
        runMtg = wx.Button(self, label="Run Mortgage Best Ex Previous Business Day")
        #runMtg.Bind(wx.EVT_BUTTON, self.runPreviousBdayMtg)
        
        runTreas = wx.Button(self, label="Run Treasury Best Ex Previous Business Day")
        #runTreas.Bind(wx.EVT_BUTTON, self.runPreviousBdayTreas)


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="BNY COMPLIANCE MANAGER REPORT v0.2.1")
 
        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)
 
        # Create the tab windows
        tab1 = TabOne(nb)
        #tab2 = TabTwo(nb)
       # tab3 = TabThree(nb)
        #tab4 = TabFour(nb)
 
        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "Fixed Income Reports")
        #nb.AddPage(tab2, "Equity Reports")
        #nb.AddPage(tab3, "TKG")
        #nb.AddPage(tab4, "Report Viewer")
 
        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
 
 
if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()