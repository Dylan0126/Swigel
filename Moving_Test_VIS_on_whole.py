# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 10:13:06 2017

@author: SwigelUser
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

lag1 = pd.read_csv('//SWIGEL_LOCAL/Shared/SCM_Research/Fundemental_Factor_Research/Industrials_Sector/VIS_Dataset_2005_2017/VIS_lag1.csv',
                  parse_dates=['Date'])
lag1['Inter'] = lag1['ip_index']*lag1['ip_machinery']
lag1['Inter2'] = lag1['ip_index']*lag1['industrial_loans']

lag1['Trend'] = lag1.VIS > lag1.VIS.shift()
lag1['Trend'].iloc[0] = np.NaN
variable_to_use = ['ip_index','ip_machinery','industrial_loans','Inter','Inter2']


su = 0
sl = 0 
size = int(input('Enter Training Size:'))
window = int(input('Enter Moving Window:'))

for i in range(0,int(lag1.shape[0]/window)):
    su = size + window*i
    sl = window*i
    train = lag1[sl:su]
    test = lag1
    y_train = train['VIS']
    X_train = train[variable_to_use]
    y_test = test['VIS']
    X_test = test[variable_to_use]
    lr = LinearRegression()
    lr.fit(X_train,y_train)
    
    lag1_predict = lr.predict(X_test)
    pred_VIS = pd.DataFrame(lag1_predict)
    #get the predicted trend of test set 
    pred_VIS.columns = ['predVIS']
    pred_VIS['Trend'] = pred_VIS.predVIS > pred_VIS.predVIS.shift()
    pred_VIS['Trend'].iloc[0] = np.NaN
    #get the 
    test_trend = lag1['Trend']
    
    #Get a liast of the predicted trend and the actual trend
    Final = pred_VIS.Trend == test_trend
    #Get accuracy
    Accuracy = sum(Final)/(lag1.shape[0]-1)
    print ('Accuracy',(i+1), Accuracy)