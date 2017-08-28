# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 12:24:58 2017

@author: SwigelUser
"""

import pandas as pd
import matplotlib.pyplot as plt

#Instruction to use : change the Dataset path here, make sure you are using '/' instead of '\'
lag1 = pd.read_csv('//SWIGEL_LOCAL/Shared/SCM_Research/Fundemental_Factor_Research/ConsumerStaples_Sector/VDC_dataset_2004_2017/VDC_lag1.csv')

#Change the variable names and fund name here. Then RUN!!!
variableList = ['ppi_commodities','food_consumption','household_furnish_operation','ip_food_beverage_tobacoo','cpi_all_items']
fundName = lag1['VDC']



for i in range(0,len(variableList)):
    plt.figure()
    graph = fundName.rolling(window=24).corr(other=lag1[variableList[i]])
    plt.title(variableList[i])
    plt.plot(graph)
    plt.axhline(y=0)
    plt.savefig(variableList[i])
