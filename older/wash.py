
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from bloombergBooks import books as books


# In[ ]:

class washMgr(object):
    
    def __init__(self, fileLocation, saveLocation,date):
                
        self.fileLocation = fileLocation
        self.saveLocation = saveLocation
        self.date = date
        
    def openFile(self):
        
        df = pd.read_csv(self.fileLocation+"\\"+self.date+".csv", delimiter = "|")
        cols = df.columns.tolist()
        cols = [i.replace(" ", "_").upper() for i in cols]
        df.columns = cols
        df = df.sort_values(by=['CUSIP_NUMBER', 'MASTER_ACCOUNT'])
        df = df[~df['SECURITY_TYPE'].isin(["Financial commodity option.", "Financial commodity future."])]
        df = df[(df['ISSUER'] != "US TREASURY N/B") & (df['ISSUER'] !='TREASURY BILL')]
        df = df[~df['COUNTERPARTY'].isin(books)]
        df = df[~df['MASTER_ACCOUNT'].isin(books)]
        df = df[(df['ALTERNATIVE_TRADING_SYSTEM_MP'].isnull())&(df['COUNTERPARTY']!= "DEALERWEB")]
        return df
        
    def grps(self):
        
        df = self.openFile()
        grp = df.groupby(['TRADE_DATE' ,'AMOUNT_(WHOLE_NUMBER)', 'CUSIP_NUMBER', 'COUNTERPARTY'])
        grpList = grp['BUY/SELL'].filter(lambda x: x.nunique() >=2).index.tolist()

        print(grpList)
        
        df = df[df.index.isin(grpList)]
        df = df.set_index(['AS_OF_DATE','COUNTERPARTY', 'CUSIP_NUMBER'])
        df['Notes'] = np.where(df['BENCHMARK']=='CT10', 'TBA - Ignore', 'Non-TBA')
        df = df[~df['Notes'].str.contains('TBA - Ignore')]
        
        return df
    def save(self):
        
        
        df = self.grps()
        return df.to_excel(self.saveLocation+'//'+self.date+'.xlsx')
        
        



# In[ ]:

#was1.openFile()


# In[ ]:

#was1.grps()


# In[ ]:

#was1.save()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



