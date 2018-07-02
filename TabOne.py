import wx
from bnyCompliance.bestex.mtg.manager import DataMgr
from bnyCompliance.bestex.treasury.treasMgr import treasMgr 
from bnyCompliance.FixedIncomeWash.wash import washMgr
from bnyCompliance.bloombergBooks.books import books
#from bnyCompliance.ReportOpener.excelcomm import openWorkBook
import win32com.client as win32
from bnyCompliance.ReportOpener.excelcomm import openWorkbook


import datetime
from pandas.tseries.offsets import BDay
import os

bday = datetime.date.today() - BDay(1)
MONTH = bday.strftime('%B') 
YEAR = bday.strftime('%Y')


BLOOMBERG_REPORT_PATH = {
                        'main' : 'H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews\\',
                        'mtgBloomberg' : 'Best Ex Mortgage\\BloombergFiles\\',
                        'treasuryBloomberg' : 'Best Ex Treasuries\\BloombergFiles\\',
                        }
                        
                        
MTG_BLOOMBERG = os.path.join(BLOOMBERG_REPORT_PATH['main'],BLOOMBERG_REPORT_PATH['mtgBloomberg'])
MTG_YESTERDAY = sorted(os.listdir(MTG_BLOOMBERG))[-1]

TREAS_BLOOMBERG = os.path.join(BLOOMBERG_REPORT_PATH['main'],BLOOMBERG_REPORT_PATH['treasuryBloomberg'])
TREAS_YESTERDAY = sorted(os.listdir(TREAS_BLOOMBERG))[-1]

WASH_DIR = os.path.join(BLOOMBERG_REPORT_PATH['main'],'wash')
WASH_LATEST = sorted(os.listdir(WASH_DIR))[-1]


class TabOneManual(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)

        
        
        #---------------------------------------------------------
        instructionText =  wx.StaticText(self, label="Use When Running the Report For Missed Days")
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        instructionText.SetFont(font)
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
        
        sizer = wx.GridBagSizer(7, 5)
        sizer.Add(instructionText, pos=(0,0), flag=wx.LEFT)
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


        self.SetSizer(sizer)

        
    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           defaultPath="H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews",
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
        dlg = wx.DirDialog(self, "Choose a directory:",
                           defaultPath="H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews",
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
                           style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:

        
                date = self.tc1.GetValue()
                bloomy = self.tc2.GetValue() + '\\'   
                save = self.tc3.GetValue()+ "\\"
        
                mtgMgr = DataMgr(date, bloomy, save)
                mtgMgr.save()
            
        elif self.radio2.GetValue() == True:
            dlg = wx.MessageDialog(self, "Run Treasury Best Ex Rept",
                           style=wx.DD_DEFAULT_STYLE)
            
            if dlg.ShowModal() == wx.ID_OK:
                date = self.tc1.GetValue()
                bloomy = self.tc2.GetValue()+"\\"
                save = self.tc3.GetValue()+"\\"
                
                treasMgr1 = treasMgr(date, bloomy, save)
                treasMgr1.save()
                
        elif self.radio3.GetValue() == True:
            dlg = wx.MessageDialog(self, "Run Wash Report?",
                           style=wx.DD_DEFAULT_STYLE)
            
            if dlg.ShowModal() == wx.ID_OK:
                date = self.tc1.GetValue()
                bloomy = self.tc2.GetValue()+"\\"
                save = self.tc3.GetValue()+"\\"
                
                wash = washMgr(bloomy, save, date)
                wash.save()
        
        else:
            dlg = wx.MessageDialog(self, "Chose a report type",
                               style = wx.DD_DEFAULT_STYLE)
                


class TabOneExcelOpen(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)

        
        
        #---------------------------------------------------------
        instructionText =  wx.StaticText(self, label="OPEN REPORTS IN EXCEL")
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        instructionText.SetFont(font)
        #--------------------MTG Best Ex Open Button---------------------------
     
        #File Lcoation 
        MortgageBestExText = wx.StaticText(self, label="Open Mortgage Best Ex in Excel (must run the report first): ")
        MtgBestExButton = wx.Button(self, label="Open Mortgage Best Ex in Excel")
        MtgBestExButton.Bind(wx.EVT_BUTTON, self.OpenFileMTG)
        
        #-------------------Treasury Best Ex Open Button-------------------------
        
        TreasuryBestExText = wx.StaticText(self, label="Open Treasury Best Ex in Excel (must run the report first): ")
        TreasuryBestExButton = wx.Button(self, label="Open Treasury Best Ex in Excel")
        TreasuryBestExButton.Bind(wx.EVT_BUTTON, self.OpenFileTSY)
        
        #-------------------Wash Open Button-------------------------
        
        WashButtonText = wx.StaticText(self, label="Open Wash Report in Excel (must run the report first): ")
        WashButton = wx.Button(self, label="Open Wash Report in Excel")
        WashButton.Bind(wx.EVT_BUTTON, self.OpenFileWASH)
       
        
        sizer = wx.GridBagSizer(7, 5)
        sizer.Add(instructionText, pos=(0,0), flag=wx.LEFT)
        
        sizer.Add(MortgageBestExText, pos=(2, 0), flag=wx.LEFT, border=10) #Date static text nested on left
        sizer.Add(MtgBestExButton, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)#mtgBestEx Button
        
        sizer.Add(TreasuryBestExText, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)#file input sizer static text
        sizer.Add(TreasuryBestExButton, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)#Treasury best ex button

        sizer.Add(WashButtonText, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(WashButton, pos=(4, 1), span=(1,3), flag=wx.TOP|wx.EXPAND, border=5)#brow button save

        self.SetSizer(sizer)
        
        
    def OpenFileMTG(self, event):
    
        
        dlg = wx.MessageDialog(self, "Open Report",
                       style=wx.DD_DEFAULT_STYLE)
            
            
        if dlg.ShowModal() == wx.ID_OK:
            try:
                PATH_TO_DIR = os.path.join(BLOOMBERG_REPORT_PATH['main'],'Best Ex Mortgage', YEAR, MONTH, MTG_YESTERDAY.replace(".csv", ".xlsx"))
                print(PATH_TO_DIR)
                excel = excel = win32.gencache.EnsureDispatch('Excel.Application')
                #openWorkbook(excel, "H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews\\Best Ex Mortgage\\2018"+"\\June\\"+"2018-06-29.xlsx")
                wb =  openWorkbook(excel, PATH_TO_DIR)
                ws = wb.Worksheets('Sheet1') 
                excel.Visible = True

            except Exception as e:
                print(e)

            finally:
                # RELEASES RESOURCES
                ws = None
                wb = None
                excel = None

    def OpenFileTSY(self, event):
    
        
        dlg = wx.MessageDialog(self, "Open Report",
                       style=wx.DD_DEFAULT_STYLE)
            
            
        if dlg.ShowModal() == wx.ID_OK:
            try:
                PATH_TO_DIR = os.path.join(BLOOMBERG_REPORT_PATH['main'],'Best Ex Treasuries', YEAR, MONTH, TREAS_YESTERDAY.replace(".csv", ".xlsx"))
                print(PATH_TO_DIR)
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                wb =  openWorkbook(excel, PATH_TO_DIR)
                ws = wb.Worksheets('Sheet1') 
                excel.Visible = True

            except Exception as e:
                print(e)

            finally:
                # RELEASES RESOURCES
                ws = None
                wb = None
                excel = None


    def OpenFileWASH(self, event):
    
        
        dlg = wx.MessageDialog(self, "Open Report",
                       style=wx.DD_DEFAULT_STYLE)
            
            
        if dlg.ShowModal() == wx.ID_OK:
            try:
                PATH_TO_DIR = os.path.join(BLOOMBERG_REPORT_PATH['main'], 'wash', WASH_LATEST)
                print(PATH_TO_DIR)
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                wb =  openWorkbook(excel, PATH_TO_DIR)
                ws = wb.Worksheets('Sheet1') 
                excel.Visible = True

            except Exception as e:
                print(e)

            finally:
                # RELEASES RESOURCES
                ws = None
                wb = None
                excel = None




class TabOneAutoRun(wx.Panel):
#------------------------------auto run----------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        #self.SetBackGroundColour("pink")
        blankPanel = wx.Panel(self)
        runMtg = wx.Button(self, label="Run Mortgage Best Ex Previous Business Day")
        runMtg.Bind(wx.EVT_BUTTON, self.runPreviousBdayMtg)
        
        runTreas = wx.Button(self, label="Run Treasury Best Ex Previous Business Day")
        #line = wx.StaticLine(self.panel, -1, style=wx.LI_HORIZONTAL)
        
        sizer = wx.GridBagSizer(20,20)
        sizer.Add(runMtg, pos=(0,1))
        sizer.Add(runTreas, pos=(0,10))

        self.SetSizer(sizer)
        runTreas.Bind(wx.EVT_BUTTON, self.runPreviousBdayTreas)
        
    def runPreviousBdayMtg(self, event):
            
        dlg = wx.MessageDialog(self, "Run Mortage Best Ex Report for previous business day?",
                       style=wx.DD_DEFAULT_STYLE
                       #| wx.DD_DIR_MUST_EXIST
                       #| wx.DD_CHANGE_DIR
                       )
        
        if dlg.ShowModal() == wx.ID_OK:

        
                date = MTG_YESTERDAY.replace('.csv','')
                year = YEAR
                month = MONTH
                bloomy = MTG_BLOOMBERG
                save = os.path.join(BLOOMBERG_REPORT_PATH['main'],'Best Ex Mortgage', YEAR, month+"\\")
                mtg = DataMgr(date,bloomy, save)
                mtg.save()
                
    def runPreviousBdayTreas(self, event):
            
        dlg = wx.MessageDialog(self, "Run Treasury Best Ex Report for previous business day?",
                       style=wx.DD_DEFAULT_STYLE
                       #| wx.DD_DIR_MUST_EXIST
                       #| wx.DD_CHANGE_DIR
                       )
        
        if dlg.ShowModal() == wx.ID_OK:

        
                date = TREAS_YESTERDAY.replace('.csv','')
                year = YEAR
                month = MONTH
                bloomy = TREAS_BLOOMBERG
                save = os.path.join(BLOOMBERG_REPORT_PATH['main'],'Best Ex Treasuries', YEAR, month+"\\")
                treas = treasMgr(date,bloomy, save)
                treas.save()



class FixedIncomeTabMain(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        panel = TabOneAutoRun(self)
        panel2 = TabOneManual(self)
        panel3 = TabOneExcelOpen(self)
        
        sizer = wx.GridBagSizer(10,5)
        sizer.Add(panel, pos=(2,1))
        sizer.Add(panel2, pos=(4,1))
        sizer.Add(panel3, pos=(6,1))
        self.SetSizer(sizer)
        #self.Show()
"""
if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
    """