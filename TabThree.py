import wx
from  wx import html2


class TkgHtmlPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds) 
        
        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]
        
        sizer = wx.BoxSizer() 
        
        self.browser = wx.html2.WebView.New(self, size=(screenWidth,screenHeight), style=wx.VSCROLL)
        
        #self.panel1 =  wx.Panel(self,size=(screenWidth,28), pos=(0,0), style=wx.SIMPLE_BORDER)
        #self.panel1.SetBackgroundColour('#FDDF99')
        

        #sizer.Add(self.browser, -1, wx.EXPAND, 8)
        #sizer.Add(self.panel1)
        sizer.Add(self.browser)
        self.SetSizer(sizer) 
        #self.SetSize((700, 700)) 

        
        self.browser.LoadURL("https://tkganalysis.com/") 
        #self.browser.LoadURL("https://sentinel.tkganalysis.com")
        #self.browser.LoadURL("https://tkganalysis.com/#/login")
        self.Show() 
 



class TkgTabMain(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        panel = TkgHtmlPanel(self)
        #panel2 = use for more reports
        
        sizer = wx.GridBagSizer(10,5)
        sizer.Add(panel, pos=(2,1))
        #sizer.Add(panel2, pos=(4,1)) us for more reports later
        self.SetSizer(sizer)