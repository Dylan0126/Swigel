# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 17:06:40 2017

@author: SwigelUser
"""

import pandas as pd

df = pd.read_csv('C:/Users/SwigelUser/realDonaldTrump_tweets.csv')
df['date'] = pd.to_datetime(df['created_at']).dt.date
df1 = df.groupby('date',as_index = False).count()
df2 = df1.sort_values('date',ascending=False)
df2 = df2[['date','text']]
df2.to_csv('Frequency.csv')