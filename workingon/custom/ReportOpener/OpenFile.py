
# coding: utf-8

# In[6]:

import pandas as pd
import os
import datetime
from pandas.tseries.offsets import BDay
yesterday = datetime.date.today() -  BDay(1)
yesterday = yesterday.strftime('%Y-%m-%d')
yesterday


mortlocation = "C:\\blp\\data\\mbex.txt"
tsylocation = "C:\\blp\\data\\tsy_bex"

SAVE_PATH= "H:\\Post June 11, 2010\\Calendars\\CM Fixed Income Reviews"

MTG_PATH = os.path.join(SAVE_PATH, "Best Ex Mortgage", "BloombergFiles", yesterday+".csv")
TSY_PATH = os.path.join(SAVE_PATH, "Best Ex Treasuries", "BloombergFiles", yesterday+".csv")
print(MTG_PATH, "\n", TSY_PATH)


# In[7]:

def OpenAndSave(openloc, saveloc):
    
    df = pd.read_csv(openloc, skiprows=2, sep="\t").reset_index()
    df = df.iloc[:,1:-1]
    
    df.to_csv(saveloc, sep="|", index=False)
    return df

OPEN_MORT = OpenAndSave(mortlocation, MTG_PATH)

OPEN_TSY = OpenAndSave(tsylocation, TSY_PATH)
    

