import wx
from wx.adv import CalendarCtrl as CalendarCtrl
from wx.lib.calendar import Calendar as wxcal
from bnyCompliance.bestex.mtg.manager import DataMgr
from bnyCompliance.bestex.treasury.treasMgr import treasMgr 
from bnyCompliance.FixedIncomeWash.wash import washMgr
from bnyCompliance.bloombergBooks.books import books
import win32com.client as win32
from bnyCompliance.ReportOpener.excelcomm import openWorkbook
from bnyCompliance.Functions.OpenFile import OpenFileExcel
from file_functions.FileCreateTime import creation_date, creation_month, creation_year
import webbrowser
import datetime as dt
import sys


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
                        'BLP' : os.path.abspath("C:\\blp\\data"),
                        }
                        
blp = BLOOMBERG_REPORT_PATH['BLP']                        
MTG_BLOOMBERG = os.path.join(BLOOMBERG_REPORT_PATH['main'],BLOOMBERG_REPORT_PATH['mtgBloomberg'])
MTG_YESTERDAY = sorted(os.listdir(MTG_BLOOMBERG))[-1]

MTG_BLP = os.path.join(blp,'mbex')
TSY_BLP = os.path.join(blp, 'tsy_bex')

TREAS_BLOOMBERG = os.path.join(BLOOMBERG_REPORT_PATH['main'],BLOOMBERG_REPORT_PATH['treasuryBloomberg'])
TREAS_YESTERDAY = sorted(os.listdir(TREAS_BLOOMBERG))[-1]

WASH_DIR = os.path.join(BLOOMBERG_REPORT_PATH['main'],'wash')
WASH_LATEST = sorted(os.listdir(WASH_DIR))[-1]

class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)



def GetMonthList():

    monthlist = []

    for i in range(13):
        name = wx.lib.calendar.Month[i]

        if name != None:
            monthlist.append(name)

    return monthlist


class TabOneManual(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)

        
        
        #---------------------------------------------------------
        self.instructionText =  wx.StaticText(self, label="Use When Running the Report For Missed Days")
        self.font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.instructionText.SetFont(self.font)
        #--------------------Date input---------------------------
        self.dateText = wx.StaticText(self, label="Date use YYYY-MM-DD Format:   ")
        self.tc1 = wx.TextCtrl(self)
        self.get_date = wx.Button(self, label="Select Date")
        self.get_date.Bind(wx.EVT_BUTTON, self.calDlg)


        #--------------------end date input ----------------------
        
        #---------------------File Input Browser-------------------------------
        #File Lcoation 
        self.fileLocText = wx.StaticText(self, label="File Location")
        self.tc2 = wx.TextCtrl(self, value='H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews\\Best Ex Mortgage\\BloombergFiles')
        self.inputButton = wx.Button(self, label="Browse...")
        self.inputButton.Bind(wx.EVT_BUTTON, self.onDir)
        #---------------------File Output-------------------------------
        self.SaveLocText = wx.StaticText(self, label="Save Location")
        self.tc3 = wx.TextCtrl(self, value='H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews')

        self.outputButton = wx.Button(self, label="Browse...")
        self.outputButton.Bind(wx.EVT_BUTTON, self.onDirSave)
        
        #--------------------Radio Buttons x3----------------------------
        
        self.radio1 = wx.RadioButton(self, label = 'Mortgage Best Ex')
        self.radio2 = wx.RadioButton(self, label = 'Treasury Best Ex')
        self.radio3 = wx.RadioButton(self, label = 'Wash Sale Report Bloomberg')
        
        #------------------help and run ----------------------------------
        self.helpButton = wx.Button(self, label='Help')

        self.runButton = wx.Button(self,4, label="Run")
        self.runButton.Bind(wx.EVT_BUTTON, self.onOk)
        
        sizer = wx.GridBagSizer(7, 5)
        sizer.Add(self.instructionText, pos=(0,0), flag=wx.LEFT)
        sizer.Add(self.dateText, pos=(2, 0), flag=wx.LEFT, border=10) #Date static text nested on left
        sizer.Add(self.tc1, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)#text box for entering date next to static text
        sizer.Add(self.get_date, pos=(2, 4), span=(1, 3))
        sizer.Add(self.fileLocText, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)#file input sizer static text
        sizer.Add(self.tc2, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)#tc2 input text box
        sizer.Add(self.inputButton, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)# file input button sizer
        sizer.Add(self.tc3, pos=(4, 1), span=(1, 3),flag=wx.TOP|wx.EXPAND, border=5)
        sizer.Add(self.SaveLocText, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(self.outputButton, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)#brow button save
        sizer.Add(self.radio1, pos=(6,1))#radio Mortgage bestex
        sizer.Add(self.radio2, pos=(6,2))#mtg best ex button
        sizer.Add(self.radio3, pos=(6,3))
        sizer.Add(self.helpButton, pos=(7, 0), flag=wx.LEFT, border=10)#help button
        sizer.Add(self.runButton, pos=(7, 3))


        self.SetSizer(sizer)

    def calDlg(self, event):
        dlg = wx.lib.calendar.CalenDlg(self)
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.result
            day = result[1]
            month = result[2]
            year = result[3]
            new_date = str(year) + '-' + str(month) + '-' + str(day)
            date = datetime.datetime.strptime(new_date, '%Y-%B-%d')
            date = date.strftime('%Y-%m-%d')
            self.tc1.SetValue(date)
        else:
            self.tc2.SetValue('null')

        
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
                i = 0
                while i < 1:
                    wait = wx.BusyCursor()


                    date = self.tc1.GetValue()
                    bloomy = self.tc2.GetValue() + '\\'
                    save = self.tc3.GetValue()+ "\\"

                    mtgMgr = DataMgr(date, bloomy, save)
                    mtgMgr.save()
                    i=1
                    wx.MessageBox('Completed', 'Invalid directory', wx.OK | wx.ICON_EXCLAMATION)
                    return

        elif self.radio2.GetValue() == True:
            dlg = wx.MessageDialog(self, "Run Treasury Best Ex Rept",
                           style=wx.DD_DEFAULT_STYLE)

            if dlg.ShowModal() == wx.ID_OK:
                i = 0
                while i < 1:
                    wait = wx.BusyCursor()
                    date = self.tc1.GetValue()
                    bloomy = self.tc2.GetValue()+"\\"
                    save = self.tc3.GetValue()+"\\"

                    treasMgr1 = treasMgr(date, bloomy, save)
                    treasMgr1.save()
                    i =1
                    wx.MessageBox('Completed', 'Invalid directory', wx.OK | wx.ICON_EXCLAMATION)

        elif self.radio3.GetValue() == True:
            dlg = wx.MessageDialog(self, "Run Wash Report?",
                           style=wx.DD_DEFAULT_STYLE)

            if dlg.ShowModal() == wx.ID_OK:
                i = 0
                while i < 1:
                    wait = wx.BusyCursor()
                    date = self.tc1.GetValue()
                    bloomy = 'C:\\BLP\\DATA\\WASH'
                    save = self.tc3.GetValue()+"\\"

                    wash = washMgr(bloomy, save, date)
                    wash.save()
                    i=1
                    wx.MessageBox('Completed', 'Invalid directory', wx.OK | wx.ICON_EXCLAMATION)


        else:
            dlg = wx.MessageDialog(self, "Chose a report type",
                               style = wx.DD_DEFAULT_STYLE)
                


class TabOneExcelOpen(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)

        
        
        #---------------------------------------------------------
        self.instructionText =  wx.StaticText(self, label="OPEN REPORTS IN EXCEL")
        self.font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.instructionText.SetFont(self.font)

        #--------------------------------------------------
        self.SelectFileText = wx.StaticText(self, label="Manually Select File to Open:")
        self.SelectFileButton = wx.Button(self, label="Manually Select Report")
        self.SelectFileButton.Bind(wx.EVT_BUTTON, self.ManualOpenMTG)

        #--------------------MTG Best Ex Open Button---------------------------
     
        #File Lcoation 
        self.MortgageBestExText = wx.StaticText(self, label="Open Mortgage Best Ex in Excel (must run the report first): ")
        self.MtgBestExButton = wx.Button(self, label="Open Mortgage Best Ex in Excel")
        self.MtgBestExButton.Bind(wx.EVT_BUTTON, self.OpenFileMTG)

        
        #-------------------Treasury Best Ex Open Button-------------------------
        
        self.TreasuryBestExText = wx.StaticText(self, label="Open Treasury Best Ex in Excel (must run the report first): ")
        self.TreasuryBestExButton = wx.Button(self, label="Open Treasury Best Ex in Excel")
        self.TreasuryBestExButton.Bind(wx.EVT_BUTTON, self.OpenFileTSY)
        
        #-------------------Wash Open Button-------------------------
        
        self.WashButtonText = wx.StaticText(self, label="Open Wash Report in Excel (must run the report first): ")
        self.WashButton = wx.Button(self, label="Open Wash Report in Excel")
        self.WashButton.Bind(wx.EVT_BUTTON, self.OpenFileWASH)

        # -------------------Open Calendars Open Button-------------------------

        self.CalendarText = wx.StaticText(self, label="Open BNY Calendar (must run the report first): ")
        self.CalendarBtn = wx.Button(self, label="Open BNY Calendar")
        self.CalendarBtn.Bind(wx.EVT_BUTTON, self.OpenCalendar)

        
        sizer = wx.GridBagSizer(7, 5)
        sizer.Add(self.instructionText, pos=(0,0), flag=wx.LEFT)

        sizer.Add(self.SelectFileText, pos=(1,0), flag=wx.LEFT, border=10)
        sizer.Add(self.SelectFileButton, pos=(1,1), span=(1,3), flag=wx.RIGHT|wx.EXPAND)

        sizer.Add(self.MortgageBestExText, pos=(2, 0), flag=wx.LEFT, border=10) #Date static text nested on left
        sizer.Add(self.MtgBestExButton, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)#mtgBestEx Button

        
        sizer.Add(self.TreasuryBestExText, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)#file input sizer static text
        sizer.Add(self.TreasuryBestExButton, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)#Treasury best ex button

        sizer.Add(self.WashButtonText, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)
        sizer.Add(self.WashButton, pos=(4, 1), span=(1,3), flag=wx.TOP|wx.EXPAND, border=5)#brow button save

        sizer.Add(self.CalendarText, pos=(5, 0), flag=wx.TOP | wx.LEFT, border=10)
        sizer.Add(self.CalendarBtn, pos=(5, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)  # brow button save

        self.SetSizer(sizer)
        
        
    def OpenFileMTG(self, event):
    
        
        dlg = wx.MessageDialog(self, "Open Report",
                       style=wx.DD_DEFAULT_STYLE)
            
            
        if dlg.ShowModal() == wx.ID_OK:
            try:

                PATH_TO_DIR = os.path.join(BLOOMBERG_REPORT_PATH['main'],'Best Ex Mortgage', YEAR, MONTH, MTG_YESTERDAY.replace(".csv", ".xlsx"))
                print(PATH_TO_DIR)
                excel = win32.gencache.EnsureDispatch('Excel.Application')
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
    
    def ManualOpenMTG(self, event):
        
        filePath = os.path.join(BLOOMBERG_REPORT_PATH['main'])
        OpenFileExcel(self, directory=filePath)

        

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

    def OpenFileWASH(self, event):

        dlg = wx.MessageDialog(self, "Open Report",
                               style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            try:
                PATH_TO_DIR = os.path.join(BLOOMBERG_REPORT_PATH['main'], 'wash', WASH_LATEST)
                print(PATH_TO_DIR)
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                wb = openWorkbook(excel, PATH_TO_DIR)
                ws = wb.Worksheets('Sheet1')
                excel.Visible = True

            except Exception as e:
                print(e)

            finally:
                # RELEASES RESOURCES
                ws = None
                wb = None
                excel = None

    def OpenCalendar(self, event):

        filePath = os.path.join('H:\\Post June 11, 2010\\Calendars')
        OpenFileExcel(self, directory=filePath)



class TabOneAutoRun(wx.Panel):
#------------------------------auto run----------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        #self.SetBackGroundColour("pink")
        blankPanel = wx.Panel(self)

# ------------- run the previous days mtg report -----------

        runMtg = wx.Button(self,1, label="Run Mortgage Best Ex Previous Business Day")
        runMtg.Bind(wx.EVT_BUTTON, self.runPreviousBdayMtg)
#------------- open tkg site in IE -----------
        self.open_tkg = wx.Button(self,2, label='load tkg')
        self.open_tkg.Bind(wx.EVT_BUTTON, self.open_tkg_web)

# ------------- run the previous days tsy report -----------

        runTreas = wx.Button(self,3, label="Run Treasury Best Ex Previous Business Day")
        #line = wx.StaticLine(self.panel, -1, style=wx.LI_HORIZONTAL)

        sizer = wx.GridBagSizer(20,20)
        sizer.Add(runMtg, pos=(0,1))
        sizer.Add(self.open_tkg, pos=(0,5))
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
            i = 0
            while i < 1:
                wait = wx.BusyCursor()

        
                date = creation_date(MTG_BLP)
                year = creation_year(MTG_BLP)
                month = creation_month(MTG_BLP)
                blp_loc = MTG_BLP
                save = os.path.join(BLOOMBERG_REPORT_PATH['main'],'Best Ex Mortgage', year, month+"\\")
                mtg = DataMgr(date,blp_loc, save)
                mtg.save()
                i = 1
                wx.MessageBox('Completed', 'Invalid directory', wx.OK | wx.ICON_EXCLAMATION)

                return
                
    def runPreviousBdayTreas(self, event):
            
        dlg = wx.MessageDialog(self, "Run Treasury Best Ex Report for previous business day?",
                       style=wx.DD_DEFAULT_STYLE
                       #| wx.DD_DIR_MUST_EXIST
                       #| wx.DD_CHANGE_DIR
                       )
        
        if dlg.ShowModal() == wx.ID_OK:

            i = 0
            while i < 1:
                wait = wx.BusyCursor()

                date = creation_date(MTG_BLP)
                year = creation_year(MTG_BLP)
                month = creation_month(MTG_BLP)
                bloomy = TSY_BLP
                save = os.path.join(BLOOMBERG_REPORT_PATH['main'],'Best Ex Treasuries', year, month+"\\")
                treas = treasMgr(date,bloomy, save)
                treas.save()
                i = 1

                wx.MessageBox('Completed', 'Invalid directory', wx.OK | wx.ICON_EXCLAMATION)

    def open_tkg_web(self, event):


        dlg = wx.MessageDialog(self, "Open TKG Fair Price Webview?",
                               style=wx.DD_DEFAULT_STYLE
                               # | wx.DD_DIR_MUST_EXIST
                               # | wx.DD_CHANGE_DIR
                               )

        if dlg.ShowModal() == wx.ID_OK:

            ie = webbrowser.get(webbrowser.iexplore)
            ie.open('https://sentinel.tkganalysis.com/#/login')







class FixedIncomeTabMain(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        panel = TabOneAutoRun(self)
        panel2 = TabOneManual(self)
        panel3 = TabOneExcelOpen(self)
        #panel4 = TestPanel(self)

        self.logger = wx.TextCtrl(self,5, "",wx.Point(230,20), wx.Size(700,140),
                                  wx.TE_MULTILINE |  wx.TE_READONLY)
        
        sizer = wx.GridBagSizer(10,5)
        sizer.Add(panel, pos=(2,1))
        sizer.Add(panel2, pos=(4,1))
        sizer.Add(panel3, pos=(6,1))


        sizer.Add(self.logger, pos=(9,1))
        self.SetSizer(sizer)
        #self.Show()
        redir = RedirectText(self.logger)
        sys.stdout = redir

    """
    def OnButtonClick(self, event):
        
        #action on button

        self.logger.clear()
        if self.
    """
def main():
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()

