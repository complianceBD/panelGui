
import pandas as pd
import numpy as np
from tia.bbg import datamgr as dm
import datetime
from pandas.tseries.offsets import BDay as bd
from tia.bbg import LocalTerminal


class dataMgr(object):
    
    #rundate = input()
    
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
        
        
        return df

        
    def secList(self):
        
        df = self.frame()
        unique = df['Parskeyeable Description'].unique()
        unique = [i for i in unique]
        return unique

        
    def bloomberg(self):
        
        securities = self.secList()
        df= self.frame()
        
        historical_data = LocalTerminal.get_historical(securities, ['PX_HIGH', 'PX_LOW'], start=self.rundate
        ,end=self.rundate).as_frame()

        historical_bval = LocalTerminal.get_historical(securities, ['PX_ASK', 'PX_BID'], start=self.rundate
        , end=self.rundate,PRICING_SOURCE='BVAL').as_frame()

        historical_bval = historical_bval.transpose().reset_index()
        historical_data = historical_data.transpose().reset_index()
        frames = [historical_bval, historical_data]
        frames = pd.concat(frames)
    
        
        #"""Making frames to concat"""
        hd=historical_data
        hb=historical_bval
        hdcols = ['bond', 'pcs', 'price']
        hd.columns = hdcols
        high = hd[hd['pcs'] =='PX_HIGH']
        high = high[['bond', 'price']]
        high.columns = ['bond', "PX_HIGH"]
        low = hd[hd['pcs'] =='PX_LOW']
        low = low[['bond', 'price']]
        low.columns = ['bond', "PX_LOW"]

        hbcols = ['bond', 'pcs', 'price']
        hb.columns = hbcols
        bid = hb[hb['pcs'] =='PX_BID']
        bid = bid[['bond', 'price']]
        bid.columns = ['bond', "PX_BID"]
        ask = hb[hb['pcs'] == 'PX_ASK']
        ask = ask[['bond', 'price']]
        ask.columns = ['bond', "PX_ASK"]        
    
        
        
        x = pd.merge(df, high, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        x = pd.merge(x, low, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        x = pd.merge(x, bid, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        x = pd.merge(x, ask, left_on = 'Parskeyeable Description', right_on = 'bond', how='inner')
        x = x[['As of Date', 'Ticket Number', 'Security Description', 'Trader Name',
            'Buy/Sell', 'TRADE FEED TRADE AMOUNT', 'Trade price',
           'TBLT Ticket Type', 'Cusip Number', 'Benchmark Cusip or Bloomberg',
           'Parskeyeable Description', 'Security Type', 'Trader Login',
           'Sales Login', 'Par Amount', 'Issue Date', 'Principal',
           'Market Sector Description', 'Identifier', 'Counterparty',
           'Master Account Long Name', 'Master Account',
           'Benchmark','Z-Spread','Benchmark Price','Factor', 'PX_ASK', 'PX_BID', 'PX_HIGH', 'PX_LOW']]
    
    
        bestEx = x
        bestEx['inside'] = np.where(bestEx['Buy/Sell']=='B',
                            np.where(bestEx['Trade price'] > bestEx['PX_LOW'], 'inside', 'outside'),
                            np.where(bestEx['Trade price'] < bestEx['PX_HIGH'], 'inside', 'outside'))



        bestEx['insideBidAsk'] = np.where(bestEx['PX_HIGH'].astype(str) == 'nan', #if this is true look for Buy sell code
                                          np.where(bestEx['Buy/Sell']=='B',
                                                   np.where(bestEx['Trade price'] > bestEx['PX_BID'], 'inside', 'outside'),
                                                   np.where(bestEx['Trade price'] < bestEx['PX_ASK'], 'inside', 'outside')),
                                          bestEx['inside'])
        
        bestEx['PX_HIGH_LOW_DIFF_%'] = np.where(bestEx['Buy/Sell'] == 'B',
                                     ((bestEx['Trade price']-bestEx['PX_LOW'])/bestEx['PX_LOW'])*100,
                                     ((bestEx['Trade price']-bestEx['PX_HIGH'])/bestEx['PX_HIGH'])*100)
        
        bestEx['PX_BID_ASK_DIFF_%'] = np.where(bestEx['Buy/Sell'] == 'B',
                                     ((bestEx['Trade price']- bestEx['PX_BID'])/bestEx['PX_BID'])*100,
                                     ((bestEx['Trade price']-bestEx['PX_ASK'])/bestEx['PX_ASK'])*100)
        
        return bestEx
    
    
    def save(self):
        frame = self.bloomberg()
        return frame.to_excel(self.saveLoc+self.rundate+'.xlsx')

