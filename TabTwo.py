import wx
import glob
from bnyCompliance.equity.lowPriceSec import executedOrderReport
import os
import win32com.client as win32
from bnyCompliance.ReportOpener.excelcomm import openWorkbook
from bnyCompliance.Functions.OpenFile import OpenFileExcel
from bnyCompliance.equity.lowPriceSecLookBack import lowPriceSecBackDate, FormatSaveBackDate, BackDateCpty
import pandas as pd
import datetime
from tia.bbg import LocalTerminal


ReportDirs = {
    "LowPriceReportDir":"H:\\Post June 11, 2010\\Equity Low Priced Report"

}

class LowPriceSec(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        #----------------------- Text
        reportText = wx.StaticText(self, label="Low Price Securities Report: ")
        #------------- run low priced security report button
        lowPriceButton = wx.Button(self, label="Run Low Price Securities Report For Previous Day")
        self.priceThreshold = wx.TextCtrl(self, value="3") # price threshold input lable
        self.priceThresholdText = wx.StaticText(self, label="Enter a security price threshold") #price threshold text box parameter
        # ADV threshold textbox and parameter
        self.advThreshold = wx.TextCtrl(self, value="10")
        self.advThresholdText = wx.StaticText(self, label="Enter a percent of adv threshold")
        
        lowPriceButton.Bind(wx.EVT_BUTTON, self.LowPrice)

        ####--------------Back Date Report
        self.dateText = wx.StaticText(self, label="Date For Look - use YYYY-MM-DD Format:   ")
        self.dateCtrl = wx.TextCtrl(self)
        self.get_date = wx.Button(self, label="Select Date")
        self.runLookBack = wx.Button(self, label="Run Low Price Report for historical day")
        self.runLookBack.Bind(wx.EVT_BUTTON, self.BackDate)
        self.get_date.Bind(wx.EVT_BUTTON, self.calDlg)


        
        
        sizer = wx.GridBagSizer(1, 5)
        sizer.Add(reportText, pos=(1, 1), flag=wx.TOP|wx.RIGHT, border=5)# Low priced security Text
        sizer.Add(self.priceThresholdText,pos=(2,1),flag=wx.TOP|wx.RIGHT, border=5) 
        sizer.Add(self.priceThreshold, pos=(2,2), flag=wx.TOP|wx.RIGHT, border=5)#price threshold position
        sizer.Add(self.advThresholdText,pos=(2,3),flag=wx.TOP|wx.RIGHT, border=5)
        sizer.Add(self.advThreshold, pos=(2,4),flag=wx.TOP|wx.RIGHT, border=5) #adv threshold position
        sizer.Add(lowPriceButton, pos=(2, 5), flag=wx.TOP|wx.RIGHT, border=5)# file input button sizer
        sizer.Add(self.dateText, pos=(4,1), border=5)
        sizer.Add(self.dateCtrl, pos=(4,2))
        sizer.Add(self.runLookBack, pos=(4,5))
        sizer.Add(self.get_date, pos=(4,4))

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
            self.dateCtrl.SetValue(date)



    def LowPrice(self, event):

        i = 0
        while i < 1:
            wait = wx.BusyCursor()


            save = "H://Post June 11, 2010//Equity Low Priced Report//" #the directory where the final output is saved

            PATH_TO_FIDESSA = os.path.abspath('T://CMI//MUNI//FidessaComplianceReportingBKCM')
            dir_list = [os.path.join(PATH_TO_FIDESSA, d) for d in os.listdir(PATH_TO_FIDESSA) if os.path.isdir(os.path.join(PATH_TO_FIDESSA, d))]
            latest_subdir = max(dir_list, key=os.path.getmtime)
            orderReports = glob.glob(latest_subdir + "\\EXECUTED_ORDER*")
            cpty_reports = glob.glob(latest_subdir + "\\ALLOCATIONS.*")
            cpty_stepout = glob.glob(latest_subdir + "\\CPTY_ACCOUNT.*")
            glob.glob

            adv = self.advThreshold.GetValue()
            price = self.priceThreshold.GetValue()
            print(orderReports)
            price = int(price)
            adv = int(adv)

            try:
                rpt = executedOrderReport(orderReports[0], save, price, adv, cpty=cpty_reports[0], cpty_list=cpty_stepout[0])
                x = lambda x: (print(i +"\n") for i in x)
                x(orderReports)
                rpt.save()
                i=1
                return wx.MessageBox('Completed', 'Invalid directory', wx.OK | wx.ICON_EXCLAMATION),
            except PermissionError as e:
                print('someone using the file')
                i=1
            except IndexError:
                print('using second file')
                rpt = executedOrderReport(orderReports[-1], save,int(price), int(adv), cpty=cpty_reports[0],
                                          cpty_list=cpty_stepout[0])
                x = lambda x: (print(i + "\n") for i in x)
                x(orderReports)
                rpt.save()
                i=1
                wx.show

    def BackDate(self, event):
        i = 0
        try:
            while i < 1:
                wait = wx.BusyCursor() #run busy cursor until end
                date = self.dateCtrl.GetValue() #get the date input from the gui
                print(date)
                adv = self.advThreshold.GetValue() #get the adv string value from gui
                price = self.priceThreshold.GetValue() # get the price threshold from gui

                backdate = lowPriceSecBackDate(date, price, adv) #craate back date object
                backdate.formatDates() # get the dates and file dirs
                print(backdate.FILE_DIR, '\n', backdate.cpty_report,'\n', backdate.cpty_stepout)
                backDateCptyDf = pd.read_csv(backdate.cpty_report, sep="|")
                backDateAllocationDf  = pd.read_csv(backdate.cpty_stepout, sep="|")




                bkDateReport = executedOrderReport(backdate.FILE_DIR, backdate.SAVE, 3, 10) # use the low price sec class to get symbols dont run the regulat low price report
                syms = bkDateReport.getSymbols()
                syms = syms.SYMBOL.tolist()
                syms = [i + " US EQUITY" for i in syms]
                print('sybmols found are: ', syms)
                print("date is report will run for is: ", backdate.RUN_DATE)

                print('running advs')
                advs = LocalTerminal.get_historical(syms, 'PX_VOLUME', backdate.RUN_DATE, backdate.RUN_DATE).as_frame() #uses custom bloomberg api based on TIA_BBG github
                adv2 = LocalTerminal.get_reference_data(syms, 'VOLUME_AVG_30D', backdate.RUN_DATE,
                                                        backdate.RUN_DATE).as_frame()
                advs = advs.transpose().reset_index().set_index('level_0').iloc[:, -1:]
                advs.columns = ['PX_VOLUME_1D']
                adv2 = adv2.join(advs).reset_index()
                adv2.columns = ['SYMBOL', 'VOLUME_AVG_30D', 'PX_VOLUME_1D']
                adv2['SYMBOL'] = [i.split(" ", 1)[0] for i in adv2.SYMBOL.tolist()]



                exceptionFrame = bkDateReport.getSymbols()
                exceptionFrame = exceptionFrame.merge(adv2, on='SYMBOL', how='left')
                exceptionFrame['BKCM_TOTAL_VOL'] = exceptionFrame.groupby('SYMBOL')['VOLUME'].transform('sum')
                exceptionFrame['BKCM_%_ADV'] = (exceptionFrame['BKCM_TOTAL_VOL'] / exceptionFrame['VOLUME_AVG_30D']) * 100
                exceptionFrame['BKCM_%_OF_VOLUME_YESTERDAY'] = (exceptionFrame['BKCM_TOTAL_VOL'] / exceptionFrame['PX_VOLUME_1D']) * 100
                exceptionFrame = exceptionFrame[exceptionFrame['BKCM_%_ADV'] > 10]


                print('running backdate cpty')
                cpty = BackDateCpty(backDateAllocationDf, backDateCptyDf)
                cpty.merge()
                cpty = cpty.alloc
                exceptionFrame = pd.merge(exceptionFrame, cpty, left_on='PARENT_ORDER_ID', right_on='ORDER_ID', how='left')

                print("excpetion report found these counter parties :", exceptionFrame.COUNTERPARTY_CODE.tolist())

                print('saving')
                exception = FormatSaveBackDate(exceptionFrame, backdate.date2)
                i = 2
                return exception.save()
        except Exception as e:
            print(e)
            i = 2
            return




class TabTwoExcelOpen(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)

        
        
        #---------------------------------------------------------
        instructionText =  wx.StaticText(self, label="OPEN REPORTS IN EXCEL")
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        instructionText.SetFont(font)
        #--------------------MTG Best Ex Open Button---------------------------
     
        #File Lcoation 
        LowPricedSecText = wx.StaticText(self, label="Open 'Equity Low Priced Security Report': ")
        LowPriceSecOpenButton = wx.Button(self, label="Open Most Recent Priced Security Report")
        LowPriceSecOpenButton.Bind(wx.EVT_BUTTON, self.OpenFileLowPriceReport)
        
        self.LowPriceSecDirButton = wx.Button(self, label="Manually Chose Report To Open")
        self.LowPriceSecDirButton.Bind(wx.EVT_BUTTON, self.OpenFileLowPriceCustom)
       
        #--------------------Sizer----------------------------------------------
        sizer = wx.GridBagSizer(7, 10)
        sizer.Add(instructionText, pos=(0,0), flag=wx.LEFT)
        
        sizer.Add(LowPricedSecText, pos=(2, 0), flag=wx.LEFT, border=10) #open report text 
        sizer.Add(LowPriceSecOpenButton, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)#Open report for previous bday button
        sizer.Add(self.LowPriceSecDirButton, pos=(2,4), span=(2,5), flag=wx.RIGHT)
        self.SetSizer(sizer)
        
        
        
        #------------------------------- Opens most recent low price sec report in directory------------
        
    def OpenFileLowPriceReport(self, event):
    
        
        dlg = wx.MessageDialog(self, "Open Report",
                       style=wx.DD_DEFAULT_STYLE)
            
            
        if dlg.ShowModal() == wx.ID_OK:
            try:
                search_dir = os.path.abspath(ReportDirs['LowPriceReportDir'])
                files = sorted(os.listdir(search_dir))[-1]
                PATH_TO_RPT = os.path.join(search_dir, files)
                print('The most recent report is: \n'+PATH_TO_RPT)
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                wb =  openWorkbook(excel, PATH_TO_RPT)
                ws = wb.Worksheets('Sheet1') 
                excel.Visible = True

            except Exception as e:
                print(e)

            finally:
                # RELEASES RESOURCES
                ws = None
                wb = None
                excel = None


    
    def OpenFileLowPriceCustom(self, event):
    
        rpt_path = ReportDirs['LowPriceReportDir']
        print(rpt_path)
        OpenFileExcel(self, directory=rpt_path)
        
        
        
    """
    def OpenFileLowPriceCustom(self, event):
             #  allows user to select the directory
        
        with wx.FileDialog(self, "Open report file", wildcard="excel files (*.xlsx)|*.xlsx|(*.xls)|*.xlsx|(*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return 
            fileDialog.SetDirectory(ReportDirs['LowPriceReportDir'])
            pathname = fileDialog.GetPath()
            
            try:
                excel = win32.gencache.EnsureDispatch('Excel.Application')
                wb =  openWorkbook(excel, pathname)
                ws = wb.Worksheets('Sheet1') 
                excel.Visible = True
            except Exception as e:
                print(e)

            finally:
                # RELEASES RESOURCES
                ws = None
                wb = None
                excel = None
        """




class EquityTabMain(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        panel = LowPriceSec(self)
        panel2 = TabTwoExcelOpen(self)
        
        sizer = wx.GridBagSizer(10,5)
        sizer.Add(panel, pos=(2,1))
        sizer.Add(panel2, pos=(4,1))
        self.SetSizer(sizer)
        
        
def main():
    pass

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()