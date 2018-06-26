
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from tia.bbg import datamgr as dm
import datetime
from pandas.tseries.offsets import BDay as bd
from tia.bbg import LocalTerminal


# In[2]:

class treasMgr(object):
    
    def __init__(self, rundate, location, saveLoc):

        self.rundate = rundate
        self.location = location
        self.saveLoc = saveLoc
    
    def frame(self):
        

        try:
            df = pd.read_csv(self.location+self.rundate+'.csv', delimiter='|')
            
            #return df
        except FileNotFoundError:
            newLoc = input()
            df = pd.read_csv(newLoc+'.csv', delimiter="|")
            #return df
        
        df = df[df['Master Account']!= 'TRADER']
        df = df[df['Parskeyeable Description'].astype(str)!='nan']
        
        df['As of Date'] = pd.to_datetime(df['As of Date'])
        df['Maturity Date'] = pd.to_datetime(df['Maturity Date'])
        df['Issue Date'] = pd.to_datetime(df['Issue Date'])
        df['tenor'] = (df['Maturity Date'] - df['Issue Date'])
        df['tenor'] =  df['tenor'].astype('timedelta64[Y]') + 1
        
        
        df['Days from Settle to Maturity'] = df['Days from Settle to Maturity'].str.replace(',','')
        df['Days from Settle to Maturity'] = df['Days from Settle to Maturity'].astype(float)
        df['Years_until_maturity'] = df['Days from Settle to Maturity']/365
        
        df = df[df['Master Account']!= 'TRADER']
        df = df[df['Parskeyeable Description'].astype(str)!='nan']
        df = df[~df['Master Account'].str.contains('-')]
        df = df[(df['Master Account'] != 'TRADER')&((df['Master Account'] != 'BNYMLLC'))].reset_index(drop=True)
        
        
        return df
    
    def secList(self):
        
        df = self.frame()
        unique = df['Parskeyeable Description'].unique()
        unique = [i for i in unique]
        return unique
    
    def bloomberg(self):
        
        securities = self.secList()
        df= self.frame()
        
        historical_data = LocalTerminal.get_historical(securities, ['PX_HIGH', 'PX_LOW'],
                                                       start=self.rundate, end=self.rundate, 
                                                        ignore_security_error=1).as_frame()
        historical_data = historical_data.transpose().reset_index()

        historical_bval = LocalTerminal.get_historical(securities, ['YLD_YTM_MID', 'YLD_CHG_NET_2D_NO_BP'],
                                                       start=self.rundate, end=self.rundate,
                                                       PRICING_SOURCE='BVAL', ignore_security_error=1).as_frame()
        
        historical_bval = historical_bval.transpose().reset_index()
        
        frames = [historical_data, historical_bval]
        frames = pd.concat(frames)
        
        hd = historical_data
        hb = historical_bval
        hdcols = ['bond', 'pcs', 'price']
        hd.columns = hdcols
        high = hd[hd['pcs'] =='PX_HIGH']
        high = high[['bond', 'price']]
        high.columns = ['bond', "PX_HIGH"]
        low = hd[hd['pcs'] =='PX_LOW']
        low = low[['bond', 'price']]
        low.columns = ['bond', "PX_LOW"]

        hbcols = ['bond', 'pcs', 'yield']
        hb.columns = hbcols
        bid = hb[hb['pcs'] =='YLD_YTM_MID']
        bid = bid[['bond', 'yield']]
        bid.columns = ['bond', "YLD_YTM_MID"]
        ask = hb[hb['pcs'] == 'YLD_CHG_NET_2D_NO_BP']
        ask = ask[['bond', 'yield']]
        ask.columns = ['bond', "YLD_CHG_NET_2D_NO_BP"]
        
        
        x = pd.merge(df, high, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        x = pd.merge(x, low, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        x = pd.merge(x, bid, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        x = pd.merge(x, ask, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        
        x['inside'] = np.where(x['Buy/Sell']=='B',
                            np.where(x['Trade price'] > x['PX_LOW'], 'inside', 'outside'),
                            np.where(x['Trade price'] < x['PX_HIGH'], 'inside', 'outside'))
        
        x['PX_HIGH_LOW_DIFF_BPS'] = np.where(x['Buy/Sell'] == 'B',
                                     x['Trade price'] - x['PX_LOW'],
                                     x['PX_HIGH'] - x['Trade price'])
        
        x['PX_HIGH_LOW_DIFF_%'] = np.where(x['Buy/Sell'] == 'B',
                                     ((x['Trade price']- x['PX_LOW'])/ x['PX_LOW'])*100,
                                     ((x['PX_HIGH'] - x['Trade price'])/ x['PX_HIGH'])*100)

        
        return x[['As of Date', 'Ticket Number', 'Security Description', 'Trader Name',
                  'Buy/Sell', 'TRADE FEED TRADE AMOUNT', 'Trade price',
                  'TBLT Ticket Type', 'Cusip Number', 'Parskeyeable Description',
                  'Security Type', 'Trader Login', 'Sales Login', 'Issue Date',
                  'Maturity Date', 'Principal', 'Counterparty',
                  'Master Account Long Name', 'Master Account', 'Yield',
                  'Int at Maturity', 'Days from Settle to Maturity',
                  'Accrued Number Of Days', 'Coupon', 'Inflation-Linked Indicator',
                  'Mid Modified Duration', 'tenor', 'Years_until_maturity', 'PX_HIGH', 'PX_LOW',
                  'YLD_YTM_MID', 'YLD_CHG_NET_2D_NO_BP', 'inside','PX_HIGH_LOW_DIFF_BPS', 'PX_HIGH_LOW_DIFF_%']]


    def save(self):
        frame = self.bloomberg()
        return frame.to_excel(self.saveLoc+self.rundate+'.xlsx')


# In[4]:



# In[ ]:

#$treasMgr1.frame()


# In[ ]:

#treasMgr1.secList()


# In[ ]:

#treasMgr1.bloomberg()


# In[5]:

#treasMgr1.save()


# In[ ]:




# In[ ]:



