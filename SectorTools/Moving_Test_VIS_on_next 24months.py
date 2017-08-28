# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 10:13:06 2017

@author: SwigelUser
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import itertools
import heapq
import time
start_time = time.time()

lag1 = pd.read_csv('//SWIGEL_LOCAL/Shared/SCM_Research/Fundemental_Factor_Research/Industrials_Sector/VIS_Dataset_2005_2017/VIS_lag1.csv',
                  parse_dates=['Date'])
#lag1['Inter'] = lag1['ip_index']*lag1['ip_machinery']
#lag1['Inter2'] = lag1['ip_index']*lag1['industrial_loans']

lag1['Trend'] = lag1.VIS > lag1.VIS.shift()
variable_to_use = list()

# Make a list of variable names to choose from
variable_list = lag1.columns[2:13].values.tolist()


su = 0
sl = 0 
size = 24#int(input('Enter Training Size:'))
window = 12#int(input('Enter Moving Window:'))
test_size = 24#int(input('Enter Test Size:'))
accuList = list()
result_list = list()


for V in itertools.combinations(variable_list, 4):
    variable_to_use = list(V)
    for i in range(0,int(lag1.shape[0]/window)-3):
        su = size + window*i
        sl = window*i
        train = lag1[sl:su]
        test = lag1[su:su+test_size]
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
        #get the 
        test_trend = lag1['Trend'].iloc[su:su+test_size]
        test_trend.index = range(0,test_size)
        
        
        #Get a liast of the predicted trend and the actual trend
        Final = pred_VIS.Trend == test_trend
        #Get accuracy
        Accuracy = sum(Final)/(test_size-1)
        accuList.append(Accuracy)
        M = np.mean(accuList)
    #Sample std
    D = np.std(accuList,ddof=1)
    result = (M,D, variable_to_use)
    result_list.append(result)
    #result_list.sort(reverse=True)
    #top_ten = result_list[:10]
      
heapq.heapify(result_list)
top_ten = heapq.nlargest(10, result_list)        
print(top_ten)
df = pd.DataFrame(top_ten)
df.to_csv('TestOnNext24_fourvariable.csv',index=False,header=None)
print("My program took", time.time() - start_time, "to run")