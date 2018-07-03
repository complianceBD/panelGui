import pandas as pd
from tia.bbg import LocalTerminal
import tia.bbg.datamgr as dm
import os
import fnmatch
pd.options.display.max_columns = 99
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from pandas import ExcelWriter
import datetime as dt
from pandas.tseries.offsets import BDay
import glob
t1 = dt.date.today() - BDay(1)
t1 =  t1.strftime('%Y%m%d')
t1


# In[2]:

mgr = dm.BbgDataManager() #this is used to access the bloomberg api with python, used in getAdvs method in class


# In[3]:

class executedOrderReport(object):
    
    def __init__(self,location, saveLoc,threshold, advThreshold, delimiter="|"):
        
        """
        takes 3 parameters
        location = where the raw fidessa file is
        saveLoc = where the output report will go
        """
        
        self.location = location
        self.delimiter = delimiter
        self.saveLoc = saveLoc
        self.threshold = threshold
        self.advThreshold = advThreshold
        
    def openReport(self):
        
        """
        run this to get a dataframe of the the report to view on jupyter notebook
        """
        
        rpt = pd.read_csv(self.location, self.delimiter)
        return rpt
    
    def getSymbols(self):
        
        """
        this makes new frame that filter only symbols that have an execution less than 2.00
        
        """
    
        rpt = self.openReport() #opens the raw file
        rpt = rpt.sort_values(by='NAME') #sorts by "name" which is the symbol
        frame = rpt[rpt.LOCAL_PRICE < self.threshold] #removes all executions > $2.00 usd
        symbols = frame.SYMBOL.unique() #makes an array of the unique symbosl in the new frame
        rpt = rpt[rpt.SYMBOL.astype(str).isin(symbols)]  #filters the original frame incase some executions are over 2.00 but have other under 2.00
        return rpt
    
    def symbolList(self):
        
        """
        creates an array of the symbols that have executions less than 2.00
        this array will be used to access to bloomberg api or any api if modified. 
        """
        
        frame = self.getSymbols()
        symbols = frame.SYMBOL.unique()
        symbols = [i+' US Equity' for i in symbols] #add " US Equity" to each symbol so bloombergy APi will respond
        return symbols
    
    def getAdvs(self):
        """
        takes the symobl list created and uses the bloomberg api to get the average daily volume
        
        """
        securities = self.symbolList()
        
        """
        uses bloomberg api to create a list of average daily volume associated with each security. 
        """

        advs = LocalTerminal.get_reference_data(securities, ['VOLUME_AVG_30D', 'PX_VOLUME_1D'],
                                                ignore_security_error=True).as_frame()
        advs['SYMBOL'] = [i.split(" ", 1)[0] for i in advs.index.tolist()]

        """
        
        merges the frames from getSybmols above, with the api data.
        then adds to the total volume using .transform to get the total volume in specific sybmol.
        Adds the BKCM total volume for each unique symbol in a new colum which is used for filtering
        in the excptions methos below. 
        
        """
        
        
        frame = self.getSymbols()
        frame = frame.merge(advs, on='SYMBOL', how='left')
        
        frame['BKCM_TOTAL_VOL'] = frame.groupby('SYMBOL')['VOLUME'].transform('sum')
        frame['BKCM_%_ADV'] = (frame['BKCM_TOTAL_VOL']/frame['VOLUME_AVG_30D'])*100
        frame['BKCM_%_OF_VOLUME_YESTERDAY'] = (frame['BKCM_TOTAL_VOL']/frame['PX_VOLUME_1D'])*100
        
        return frame
    
    def exceptions(self):
        
        """
        filters out out symols where our total execution volume was not > 9.99%
        """
        
        exceptions = self.getAdvs()
        
        exceptions = exceptions[exceptions['BKCM_%_ADV'] > self.advThreshold]
        return exceptions
    
    def save(self):
        
        """
        saves the file using the execution date from the dataframe as the file name.
        """
        
        
        
        date = self.openReport()
        date = date.iloc[0,11]
        date = str(date)
        
        
        dfException = self.exceptions()
        
        dfAggs = dfException.groupby('NAME').agg({'#':'count',
                                                  'VOLUME':['sum', 'min'],
                                                 'CUSIP':'unique',
                                                 'LOCAL_PRICE':['min','max','mean'],
                                                  'VOLUME_AVG_30D':'max',
                                                  'BKCM_%_ADV':'max',
                                                  'PX_VOLUME_1D':'max',
                                                  'BKCM_%_OF_VOLUME_YESTERDAY':'max'
                                                 })
        
        dfAggs.columns =  ['Total Executions',
                    'BKCM Total Volume',
                    'Minimum Execution Volume',
                    'Cusip',
                    'Lowest Execution Price',
                    'Max Exection Price',
                    'Avg Execution Price',
                    '30 day ADV',
                   'BKCM % of 30 day Adv',
                   'Yesterday Total Volume',
                   "BKCM % of Yesterday's Volume"]
        dfs = [dfAggs,dfException]
        writer = ExcelWriter(self.saveLoc+date+'.xlsx')
        
        for n, df in enumerate(dfs):
            df.to_excel(writer, 'sheet%s' %n)
            
        return writer.save()
    

        
def combineFiles(path="H://Post June 11, 2010//Equity Low Priced Report//",
                savePath = "H://Post June 11, 2010//Equity Low Priced Monthly//"):
    
    
    import glob
    
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()))
                   
                            
                   
    
    
    if len(files) < 21:
        files = files
    else:
        files = files[-21]
    
    frame1 = []
    
    indexFrame = pd.read_excel(path+files[0], 'Sheet1')
    frame1.append(indexFrame)
    
    for file in files[1:]:
        frame = pd.read_excel(path+file, 'sheet1')
        frame1.append(frame)



    final = pd.concat(frame1)
    final = final.sort_values(by=['ALTERNATE_SEC_ID', 'TRADE_DATE'])
    final = final.set_index(['SYMBOL', 'TRADE_DATE'])
    
    return final.to_excel(savePath+files[-1])

        
