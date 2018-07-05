import wx
import glob
from bnyCompliance.equity.lowPriceSec import executedOrderReport, combineFiles
import os
import win32com.client as win32
from bnyCompliance.ReportOpener.excelcomm import openWorkbook
from bnyCompliance.Functions.OpenFile import OpenFileExcel



ReportDirs = {
    "LowPriceReportDir":"H:\\Post June 11, 2010\\Equity Low Priced Report"

}

class LowPriceSec(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        
        reportText = wx.StaticText(self, label="Low Price Securities Report: ")
        lowPriceButton = wx.Button(self, label="Run Low Price Securities Report")
        
        self.priceThreshold = wx.TextCtrl(self, value="3")
        self.priceThresholdText = wx.StaticText(self, label="Enter a security price threshold")
        
        self.advThreshold = wx.TextCtrl(self, value="0")
        self.advThresholdText = wx.StaticText(self, label="Enter a percent of adv threshold")
        
        lowPriceButton.Bind(wx.EVT_BUTTON, self.LowPrice)
        
        
        sizer = wx.GridBagSizer(1, 4)
        sizer.Add(reportText, pos=(1, 1), flag=wx.TOP|wx.RIGHT, border=5)# Low priced security Text
        sizer.Add(self.priceThresholdText,pos=(2,1),flag=wx.TOP|wx.RIGHT, border=5) 
        sizer.Add(self.priceThreshold, pos=(2,2), flag=wx.TOP|wx.RIGHT, border=5)#price threshold position
        sizer.Add(self.advThresholdText,pos=(2,3),flag=wx.TOP|wx.RIGHT, border=5)
        sizer.Add(self.advThreshold, pos=(2,4),flag=wx.TOP|wx.RIGHT, border=5) #adv threshold position
        sizer.Add(lowPriceButton, pos=(2, 5), flag=wx.TOP|wx.RIGHT, border=5)# file input button sizer
        self.SetSizer(sizer)
        
    
    def LowPrice(self, event):
        

        save = "H://Post June 11, 2010//Equity Low Priced Report//" #the directory where the final output is saved

        PATH_TO_FIDESSA = os.path.abspath('T://CMI//MUNI//FidessaComplianceReportingBKCM//')
        dir_list = [os.path.join(PATH_TO_FIDESSA, d) for d in os.listdir(PATH_TO_FIDESSA) if os.path.isdir(os.path.join(PATH_TO_FIDESSA, d))]
        latest_subdir = max(dir_list, key=os.path.getmtime)
        orderReports = glob.glob(latest_subdir + "\\EXECUTED_ORDER*")
        
        adv = self.advThreshold.GetValue()
        price = self.priceThreshold.GetValue()
        
        try:
            rpt = executedOrderReport(orderReports[0], save, int(price), int(adv))
            rpt.save()
        except Exception as e:
            
            print(e)
        finally:
            rpt = executedOrderReport(orderReports[-1], save,int(price), int(adv))
            rpt.save()

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
                PATH_TO_DIR = os.path.abspath(ReportDirs['LowPriceReportDir'])
                LIST_REPORTS = os.listdir(PATH_TO_DIR)[-1]
                PATH_TO_RPT = os.path.join(PATH_TO_DIR, LIST_REPORTS)
                print('The most recent report is: \n'+LIST_REPORTS)
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
    
        path=ReportDirs['LowPriceReportDir']
        OpenFileExcel(self,path)
        
        
        
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
    main()