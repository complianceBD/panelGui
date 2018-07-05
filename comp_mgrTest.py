import os
import wx
import wx.lib.agw.multidirdialog as MDD
from TabOne import FixedIncomeTabMain
from TabTwo import EquityTabMain
from TabThree import TkgTabMain
from bnyCompliance.ReportOpener.OpenFile import OPEN_MORT, OPEN_TSY
#from TabFour import ReportGrid


       
class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        """Constructor"""
        
        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]
        wx.Frame.__init__(self, None, title="Comp Mgr", size = (1500,1000))
        

        nb = wx.Notebook(self)
        nb.SetBackgroundColour('#dee0e2')
        
        tab1 = FixedIncomeTabMain(nb)
        tab2 = EquityTabMain(nb)
        tab3 = TkgTabMain(nb)
        #tab4 = ReportGrid(nb)
        
        nb.AddPage(tab1, "Fixed Income Reports")
        nb.AddPage(tab2, "Equity Reports")
        nb.AddPage(tab3, "TKG")
        #nb.AddPage(tab4, "Report Viewer")
 
        
        #panel = TabOneMainPanel(self)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.SetTitle('Compliance Manager')
        
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()
        
     ############################################
        """Window close warning"""

     ###############################################
    def OnCloseWindow(self, e):

        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        ret = dial.ShowModal()

        if ret == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()

class MainApp(wx.App):
    """Class Main App."""
    def OnInit(self):
        """Init Main App."""
        self.frame = MainFrame(None)
        return True
 
if __name__ == "__main__":
    app = MainApp(0)
    app.MainLoop()
    
  