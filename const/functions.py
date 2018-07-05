def OpenFileExcel(dir):
    """
    allows user to select the directory
    """
    
    with wx.FileDialog(self, "Open report file", wildcard="excel files (*.xlsx)|*.xlsx|(*.xls)|*.xlsx|(*.csv)|*.csv",
                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return 
        fileDialog.SetDirectory(dir)
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