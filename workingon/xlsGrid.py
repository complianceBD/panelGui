import wx
import os
import xlrd
from wx.lib.agw import xlsgrid as XG

 
########################################################################
class MyFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "XLSGrid Demo", size=(1000, 800))

        filename = os.path.join(os.getcwd(), "demo.xls")
        sheetname = "Sheet1"

        book = xlrd.open_workbook(filename, formatting_info=1)

        sheet = book.sheet_by_name(sheetname)
        rows, cols = sheet.nrows, sheet.ncols

        comments, texts = XG.ReadExcelCOM(filename, sheetname, rows, cols)

        xls_grid = XG.XLSGrid(self)
        xls_grid.PopulateGrid(book, sheet, texts, comments)
 
#----------------------------------------------------------------------
# Run the program
app = wx.App(0)

frame = MyFrame()
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()