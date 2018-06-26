
# coding: utf-8

# In[6]:

"""
requires the following libraries:

(1)pandas, 

(2) tia-bloomberg(converted to python 3 i have this saved on my local machine),
or a different data source to get average daily volumes.

"""


import pandas as pd
from tia.bbg import LocalTerminal
import tia.bbg.datamgr as dm
import os
import fnmatch
pd.options.display.max_columns = 99
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from pandas import ExcelWriter



# In[7]:

mgr = dm.BbgDataManager() #this is used to access the bloomberg api with python, used in getAdvs method in class


# In[8]:

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

        advs = LocalTerminal.get_reference_data(securities, 'VOLUME_AVG_30D', ignore_security_error=True).as_frame()
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
                                                  'BKCM_%_ADV':'max'
                                                 })
        dfs = [dfAggs,dfException]
        
        while True:
            try:
                writer = ExcelWriter(self.saveLoc+date+'.xlsx')
                break
            except PermissionError:
                print('suck it')
            for n, df in enumerate(dfs):
                df.to_excel(writer, 'sheet%s' %n)
                
            return writer.save()
        else:
            pass

        


# In[9]:

"""
#change the directory to the fidessa file directory
# create an array of the names of all the directories
#find the directory with the most recent "modification date"; this is where the most recent order file is stored
#move into the most recently created file directory
#find the file named EXECUTED_ORDER
#use this directory name for self.location
#create a variable for the save location
#
"""
save = "H://Post June 11, 2010//Equity Low Priced Report//" #the directory where the final output is saved

directory = os.chdir('T://CMI//MUNI//FidessaComplianceReportingBKCM') 
all_subdirs = [d for d in os.listdir('.') if os.path.isdir(d)] 
latest_subdir = max(all_subdirs, key=os.path.getmtime)
directory = os.chdir('T://CMI//MUNI//FidessaComplianceReportingBKCM//'+latest_subdir+'//')

for file in os.listdir('.'):
    
    if fnmatch.fnmatch(file, "EXECUTED_ORDER*"):
        directory = os.getcwd()+"\\"
        directory = directory + file

rpt = executedOrderReport(directory, save, 3,0)

rpt.exceptions()
#rpt.save()


# In[10]:

rpt.save()
