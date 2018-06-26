
import os
import wx
import wx.lib.agw.multidirdialog as MDD

from mtgMgr import dataMgr
from treasMgr import treasMgr
from bloombergBooks import books as books
from washSales import washMgr
import pandas as pd
from tia.bbg import LocalTerminal
import tia.bbg.datamgr as dm
import os
import fnmatch
from pandas import ExcelWriter
from lowPriceSec import executedOrderReport
from  wx import html2
import xlrd
import datetime as dt
import glob
 
 
# Define the tab content as classes:
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
        inputButton.Bind(wx.EVT_BUTTON, self.onDir)
        #---------------------File Output-------------------------------
        SaveLocText = wx.StaticText(self, label="Save Location")
        self.tc3 = wx.TextCtrl(self, value='H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews')

        outputButton = wx.Button(self, label="Browse...")
        outputButton.Bind(wx.EVT_BUTTON, self.onDirSave)
        
        #--------------------Radio Buttons x3----------------------------
        
        self.radio1 = wx.RadioButton(self, label = 'Mortgage Best Ex')
        self.radio2 = wx.RadioButton(self, label = 'Treasury Best Ex')
        self.radio3 = wx.RadioButton(self, label = 'Wash Sale Report Bloomberg')
        
        #------------------help and run ----------------------------------
        helpButton = wx.Button(self, label='Help')

        runButton = wx.Button(self, label="Run")
        runButton.Bind(wx.EVT_BUTTON, self.onOk)
        #------------------------------auto run----------------------------------
        runMtg = wx.Button(self, label="Run Mortgage Best Ex Previous Business Day")
        runMtg.Bind(wx.EVT_BUTTON, self.runPreviousBdayMtg)
        
        runTreas = wx.Button(self, label="Run Treasury Best Ex Previous Business Day")
        runTreas.Bind(wx.EVT_BUTTON, self.runPreviousBdayTreas)
        



        
        #5 x 5 grid sizer
        sizer = wx.GridBagSizer(5, 5)
        sizer.Add(dateText, pos=(2, 0), flag=wx.LEFT, border=10) #Date static text nested on left
        sizer.Add(self.tc1, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)#text box for entering date next to static text
        sizer.Add(fileLocText, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)#file input sizer static text
        sizer.Add(self.tc2, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)#tc2 input text box
        sizer.Add(inputButton, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)# file input button sizer
        sizer.Add(self.tc3, pos=(4, 1), span=(1, 3),flag=wx.TOP|wx.EXPAND, border=5)
        sizer.Add(SaveLocText, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(outputButton, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)#brow button save
        sizer.Add(self.radio1, pos=(6,1))#radio Mortgage bestex
        sizer.Add(self.radio2, pos=(6,2))#mtg best ex button
        sizer.Add(self.radio3, pos=(6,3))
        sizer.Add(helpButton, pos=(7, 0), flag=wx.LEFT, border=10)#help button
        sizer.Add(runButton, pos=(7, 3))
        sizer.Add(runMtg, pos=(2,4))# Run
        sizer.Add(runTreas, pos=(2,7))# Run
        self.SetSizer(sizer)


    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        if self.radio1.GetValue()==True:
            path1 = self.tc2.GetValue()
            os.chdir(path1)
        else:
            path1 = self.tc3.GetValue()
            os.chdir(path1)
        
        
        
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.tc2.SetValue(path)
    def onDirSave(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        
        #path1 = self.tc3.GetValue()
        #os.chdir(path1)
        if self.radio1.GetValue()==True:
        
            path1 = self.tc2.GetValue()
            os.chdir(path1)
        else:
            path1 = self.tc3.GetValue()
            os.chdir(path1)
        
        
        
        dlg = wx.DirDialog(self, "Choose a directory:",
                           defaultPath=path1,
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.tc3.SetValue(path)
            
    
    def onOk(self, event):
        
        if self.radio1.GetValue() == True:
            
            dlg = wx.MessageDialog(self, "Run Mortage Best Ex Rept?",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            
            if dlg.ShowModal() == wx.ID_OK:

        
                date = self.tc1.GetValue()
                bloomy = self.tc2.GetValue() + '\\'   
                save = self.tc3.GetValue()+ "\\"
        
                mtgMgr = dataMgr(date, bloomy, save)
                mtgMgr.save()
        
        elif self.radio2.GetValue() == True:
            dlg = wx.MessageDialog(self, "Run Treasury Best Ex Rept",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            
            if dlg.ShowModal() == wx.ID_OK:
                date = self.tc1.GetValue()
                bloomy = self.tc2.GetValue()+"\\"
                save = self.tc3.GetValue()+"\\"
                
                treasMgr1 = treasMgr(date, bloomy, save)
                treasMgr1.save()
                
        elif self.radio3.GetValue() == True:
            dlg = wx.MessageDialog(self, "Run Wash Report?",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
            
            if dlg.ShowModal() == wx.ID_OK:
                date = self.tc1.GetValue()
                bloomy = self.tc2.GetValue()+"\\"
                save = self.tc3.GetValue()+"\\"
                
                wash = washMgr(bloomy, save, date)
                wash.save()

        elif OSError:
            dlg = wx.MessageDialog(self, "File Location Incorrect",
                               style = wx.DD_DEFAULT_STYLE)
            
            dlg.ShowModal()
        
        else:
            dlg = wx.MessageDialog(self, "choose a report type",
                               style = wx.DD_DEFAULT_STYLE)
            
            dlg.ShowModal()    
            sizer = wx.GridBagSizer(5, 5)
    
    def runPreviousBdayMtg(self, event):
            
        dlg = wx.MessageDialog(self, "Run Mortage Best Ex Rept for previous business day?",
                       style=wx.DD_DEFAULT_STYLE
                       #| wx.DD_DIR_MUST_EXIST
                       #| wx.DD_CHANGE_DIR
                       )
        
        if dlg.ShowModal() == wx.ID_OK:

        
                date = self.tc1.GetValue()
                datetm = dt.datetime.strptime(date, '%Y-%m-%d')
                year = datetm.strftime('%Y')
                month = datetm.strftime('%B')
                bloomy = "H://Post June 11, 2010//Calendars//CM Fixed Income Reviews//Best Ex Mortgage//BloombergFiles"+"//"  
                save = "H://Post June 11, 2010//Calendars//CM Fixed Income Reviews//Best Ex Mortgage"+"//"+year+"//"+month+"//"
                mtg = dataMgr(date,bloomy, save)
                mtg.save()
    
    def runPreviousBdayTreas(self, event):
            
        dlg = wx.MessageDialog(self, "Run Mortage Best Ex Rept for previous business day?",
                       style=wx.DD_DEFAULT_STYLE
                       #| wx.DD_DIR_MUST_EXIST
                       #| wx.DD_CHANGE_DIR
                       )
        
        if dlg.ShowModal() == wx.ID_OK:
            date = self.tc1.GetValue()
            datetm = dt.datetime.strptime(date, '%Y-%m-%d')
            year = datetm.strftime('%Y')
            month = datetm.strftime('%B')
            bloomy = "H://Post June 11, 2010//Calendars//CM Fixed Income Reviews//Best Ex Treasuries//BloombergFiles"+"//"  
            save = "H://Post June 11, 2010//Calendars//CM Fixed Income Reviews//Best Ex Treasuries"+"//"+year+"//"+month+"//"
            treasMgr1 = treasMgr(date, bloomy, save)
            treasMgr1.save()

        
 
class TabTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        reportText = wx.StaticText(self, label="Low Price Securities Report: ")
        lowPriceButton = wx.Button(self, label="Run Low Price Securities Report")
        
        self.priceThreshold = wx.TextCtrl(self, value="3")
        self.priceThresholdText = wx.StaticText(self, label="Enter a security price threshold")
        
        self.advThreshold = wx.TextCtrl(self, value="0")
        self.advThresholdText = wx.StaticText(self, label="Enter a percent of adv threshold")
        
        lowPriceButton.Bind(wx.EVT_BUTTON, self.lowPrice)
        
        
        sizer = wx.GridBagSizer(1, 4)
        sizer.Add(reportText, pos=(1, 1), flag=wx.TOP|wx.RIGHT, border=5)# Low priced security Text
        sizer.Add(self.priceThresholdText,pos=(2,1),flag=wx.TOP|wx.RIGHT, border=5) 
        sizer.Add(self.priceThreshold, pos=(2,2), flag=wx.TOP|wx.RIGHT, border=5)#price threshold position
        sizer.Add(self.advThresholdText,pos=(2,3),flag=wx.TOP|wx.RIGHT, border=5)
        sizer.Add(self.advThreshold, pos=(2,4),flag=wx.TOP|wx.RIGHT, border=5) #adv threshold position
        sizer.Add(lowPriceButton, pos=(2, 5), flag=wx.TOP|wx.RIGHT, border=5)# file input button sizer
        self.SetSizer(sizer)

    def lowPrice(self, event):
        

            
        dlg = wx.MessageDialog(self, "Run Low Price Report Security Report?", style=wx.DD_DEFAULT_STYLE
                               #| wx.DD_DIR_MUST_EXIST
                               #| wx.DD_CHANGE_DIR
                               )
                
        if dlg.ShowModal() == wx.ID_OK:

            
            priceThresh = self.priceThreshold.GetValue()
            advThres = self.advThreshold.GetValue()
            
            save = "H:\Post June 11, 2010\Equity Low Priced Report\\" #the directory where the final output is saved

            directory = os.chdir("T:\CMI\MUNI\FidessaComplianceReportingBKCM") 
            all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)] 
            latest_subdir = max(all_subdirs, key=os.path.getmtime)
            reportdir = os.chdir('./'+latest_subdir)
            reportdir = os.getcwd()
            orderReports = glob.glob(reportdir + "\\EXECUTED_ORDER*"+"*2018-06-25")

            rpt = executedOrderReport(orderReports[0], save, int(priceThresh),int(advThres))
            #rpt.save()
        
 
class TabThree(wx.Panel):
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
 
class TabFour(wx.Panel):
   def __init__(self, parent):
        """
        wx.Frame.__init__(self, parent)
        
        self.start_button = wx.Button(self, -1, "Start")
        self.grid = wx.grid.Grid(self, -1)
        
        
        
        #-----------------------------------
        #open excel workbook and read items
        #------------------------------------
        #os.chdir("C://Users//XBBNQVM//Desktop//build//tests_panels//")
        filename ="C://Users//XBBNQVM//Desktop//build//tests_panels//test.xls")
        book = xlrd.open_workbook(filename, formatting_info=1)
        sheet = book.sheet_by_name(sheetname)
        rows, cols = sheet.nrows, sheet.ncols
        
        


        self.DoLayout()

        self.Bind(wx.EVT_BUTTON, self.OnStart, self.start_button)
    def DoLayout(self):

        xlrd_ver = xlrd.__VERSION__
        string_xlrd = "Version " + xlrd_ver
        
        if xlrd_ver <= "0.7.1":
            string_xlrd += ": hyperlink and rich-text functionalities will not work. xlrd 0.7.2 (SVN) is required for this."
        else:
            string_xlrd += ": hyperlink and rich-text functionalities will work!"

        if _hasWin32:
            string_pywin32 = "You have pywin32! XLSGrid cells should appear exactly as in Excel (WYSIWYG)."
        else:
            string_pywin32 = "You don't have pywin32. Cell string formatting will be severely limited."
            
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_right_sizer = wx.BoxSizer(wx.VERTICAL)
        top_center_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(self.start_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        label_1 = wx.StaticText(self, -1, "xlrd:")
        label_1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        top_center_sizer.Add(label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5)
        top_center_sizer.Add((0, 0), 1, wx.EXPAND, 0)
        label_2 = wx.StaticText(self, -1, "pywin32:")
        label_2.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        top_center_sizer.Add(label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5)
        top_sizer.Add(top_center_sizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        label_xlrd = wx.StaticText(self, -1, string_xlrd)
        top_right_sizer.Add(label_xlrd, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        top_right_sizer.Add((0, 0), 1, wx.EXPAND, 0)
        label_pywin32 = wx.StaticText(self, -1, string_pywin32)
        top_right_sizer.Add(label_pywin32, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        top_sizer.Add(top_right_sizer, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        main_sizer.Add(top_sizer, 0, wx.ALL|wx.EXPAND, 5)
        main_sizer.Add((0, 10))
        main_sizer.Add(self.grid, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(main_sizer)

        main_sizer.Layout()
    
    def OnStart(self, event):

        event.Skip()
        
        os.chdir("C://Users//XBBNQVM//Desktop//build//tests_panels//")
        filename = os.path.join(os.getcwd(), "test.xls")
        #filename = os.path.join(os.path.abspath(dataDir), "test.xls")
        
        if not os.path.isfile(filename):
            dlg = wx.MessageDialog(self, 'Error: the file "Example_1.xls" is not in the "data" directory',
                                   'XLSGridDemo Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        busy = wx.BusyInfo("Reading Excel file, please wait...")
        
        sheetname = "Example_2"
        book = xlrd.open_workbook(filename, formatting_info=1)

        sheet = book.sheet_by_name(sheetname)
        rows, cols = sheet.nrows, sheet.ncols

        comments, texts = XG.ReadExcelCOM(filename, sheetname, rows, cols)

        del busy

        self.grid.Show()
        self.grid.PopulateGrid(book, sheet, texts, comments)
        
        self.start_button.Enable(False)
        self.Layout()
    """
 
 
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="BNY COMPLIANCE MANAGER REPORT v0.2.1")
 
        # Create a panel and notebook (tabs holder)
        p = wx.Panel(self)
        nb = wx.Notebook(p)
 
        # Create the tab windows
        tab1 = TabOne(nb)
        tab2 = TabTwo(nb)
        tab3 = TabThree(nb)
        #tab4 = TabFour(nb)
 
        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "Fixed Income Reports")
        nb.AddPage(tab2, "Equity Reports")
        nb.AddPage(tab3, "TKG")
        #nb.AddPage(tab4, "Report Viewer")
 
        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
 
 
if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()