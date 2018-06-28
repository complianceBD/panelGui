import wx




class ReportMain(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        TopPanel = OpenClosePanel(self)
        GridPanel = ReportGrid(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(TopPanel, wx.TOP)
        sizer.Add(GridPanel, wx.BOTTOM|wx.EXPAND)
        self.SetSizer(sizer)
        #self.Show()