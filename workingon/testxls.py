import wx
import xlrd
from wx.lib.agw import xlsgrid as XG

from wx import grid as gridlib
 
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")
 
        panel = wx.Panel(self, wx.ID_ANY)
 
        filename = "C:\\Users\\XBBNQVM\\Desktop\\compmgr_new\\demo.xls"
        book = xlrd.open_workbook(filename, formatting_info=1)
        sheetname = "Sheet1"
        sheet = book.sheet_by_name(sheetname)
        rows, cols = sheet.nrows, sheet.ncols
        comments, texts = XG.ReadExcelCOM(filename, sheetname, rows, cols)
        
        mygrid = gridlib.Grid(panel)
        mygrid.CreateGrid(rows, cols)
        
 
        xlsGrid = XG.XLSGrid(mygrid)
        xlsGrid.PopulateGrid(book, sheet, texts, comments)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND, 5)
        panel.SetSizer(sizer)
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm().Show()
    app.MainLoop()