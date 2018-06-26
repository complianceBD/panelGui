import os
import wx
import wx.lib.agw.multidirdialog as MDD
from TabOne import FixedIncomeTabMain
from TabTwo import EquityTabMain
from TabThree import TkgTabMain


       
class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Comp Mgr", size = (1500,1000))
        

        nb = wx.Notebook(self)
        nb.SetBackgroundColour('#dee0e2')
        
        tab1 = FixedIncomeTabMain(nb)
        tab2 = EquityTabMain(nb)
        tab3 = TkgTabMain(nb)
        
        nb.AddPage(tab1, "Fixed Income Reports")
        nb.AddPage(tab2, "Equity Reports")
        nb.AddPage(tab3, "TKG")
 
        
        #panel = TabOneMainPanel(self)
        
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()
 
if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
    
  