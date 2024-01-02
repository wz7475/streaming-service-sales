#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os

import pandas as pd
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import warnings
warnings.filterwarnings('ignore')

from statsmodels.tsa.stattools import adfuller
import pmdarima as pm

from config_file import data_path


# In[23]:


dir_with_plays = "plays_per_week"
artist_id = "0a1gHP0HAqALbEyxaD5Ngn"
df = pd.read_csv(os.path.join(data_path, dir_with_plays, f"{artist_id}.csv"), parse_dates=True)
df["data"] = df["year_week"] + "_1" # add day of week to date (1 - Monday)
df["data"] = pd.to_datetime(df["data"], format="%Y_%W_%w") # convert to datetime
df.drop("year_week", axis=1, inplace=True)
df.set_index(["data"], inplace=True)
df.head()


# In[25]:


plt.figure(figsize=(15,7))
plt.title("Number of plays per week")
plt.xlabel('Date')
plt.ylabel('Number of plays')
plt.plot(df)
plt.show()


# In[32]:


df["rolling_avg"] = df["count"].rolling(window=5).mean() # 5 weeks ~ 1 month
df["rolling_std"] = df["count"].rolling(window=5).std()

#Plot rolling statistics
plt.figure(figsize=(15,7))
plt.plot(df["count"], color='#379BDB', label='Original')
plt.plot(df["rolling_avg"], color='#D22A0D', label='Rolling Mean')
plt.plot(df["rolling_std"], color='#142039', label='Rolling Std')
plt.legend(loc='best')
plt.title('Rolling Mean & Standard Deviation')
plt.show(block=False)


# In[33]:


print('Results of Dickey Fuller Test:')
dftest = adfuller(df['count'], autolag='AIC')

dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
for key,value in dftest[4].items():
    dfoutput['Critical Value (%s)'%key] = value
    
print(dfoutput)

