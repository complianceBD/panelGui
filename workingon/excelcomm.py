import win32com.client as win32

def openWorkbook(xlapp, xlfile):
    try:        
        xlwb = xlapp.Workbooks(xlfile)            
    except Exception as e:
        try:
            xlwb = xlapp.Workbooks.Open(xlfile)
        except Exception as e:
            print(e)
            xlwb = None                    
    return(xlwb)

try:
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = openWorkbook(excel, "H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews\\Best Ex Mortgage\\2018"+"\\June\\"+"2018-06-29.xlsx")
    ws = wb.Worksheets('Sheet1') 
    excel.Visible = True

except Exception as e:
    print(e)

finally:
    # RELEASES RESOURCES
    ws = None
    wb = None
    excel = None