import wx

class LowPriceSec(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        
        reportText = wx.StaticText(self, label="Low Price Securities Report: ")
        lowPriceButton = wx.Button(self, label="Run Low Price Securities Report")
        
        self.priceThreshold = wx.TextCtrl(self, value="3")
        self.priceThresholdText = wx.StaticText(self, label="Enter a security price threshold")
        
        self.advThreshold = wx.TextCtrl(self, value="0")
        self.advThresholdText = wx.StaticText(self, label="Enter a percent of adv threshold")
        
        #lowPriceButton.Bind(wx.EVT_BUTTON, self.lowPrice)
        
        
        sizer = wx.GridBagSizer(1, 4)
        sizer.Add(reportText, pos=(1, 1), flag=wx.TOP|wx.RIGHT, border=5)# Low priced security Text
        sizer.Add(self.priceThresholdText,pos=(2,1),flag=wx.TOP|wx.RIGHT, border=5) 
        sizer.Add(self.priceThreshold, pos=(2,2), flag=wx.TOP|wx.RIGHT, border=5)#price threshold position
        sizer.Add(self.advThresholdText,pos=(2,3),flag=wx.TOP|wx.RIGHT, border=5)
        sizer.Add(self.advThreshold, pos=(2,4),flag=wx.TOP|wx.RIGHT, border=5) #adv threshold position
        sizer.Add(lowPriceButton, pos=(2, 5), flag=wx.TOP|wx.RIGHT, border=5)# file input button sizer
        self.SetSizer(sizer)
        
class EquityTabMain(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        panel = LowPriceSec(self)
        #panel2 = use for more reports
        
        sizer = wx.GridBagSizer(10,5)
        sizer.Add(panel, pos=(2,1))
        #sizer.Add(panel2, pos=(4,1)) us for more reports later
        self.SetSizer(sizer)