#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 13:40:39 2018

@author: mickey
"""
import pandas as pd
import os
import glob


file_path='/Users/mickey/desktop/return_output3/'

os.chdir(file_path)
files=glob.glob("*.csv")

count=0
n=len(files)

for file in files:
    count +=1
    print (count,'/',n)
    
    return_=pd.read_csv('/Users/mickey/desktop/return_output3/'+file, index_col=None)
    try:
        feature=pd.read_csv('/Users/mickey/desktop/quandl_output3/'+file, index_col=None)
        result = pd.merge(return_, feature, how='inner', on=['rebalanceDates'])
        result.to_csv('/Users/mickey/desktop/quandl_final_product/'+file, index=False)
    except Exception:
        pass
       
        
        #del return_
        #del feature
        #del result

##################

file_path='/Users/mickey/desktop/quandl_final_product/'
os.chdir(file_path)
files=glob.glob("*.csv")
df_list=pd.DataFrame()
for file in files:
    a=pd.read_csv('/Users/mickey/desktop/quandl_final_product/'+file,index_col=None)
    df_list=df_list.append(a)
df_list.to_csv('/Users/mickey/desktop/final_quandl.csv')

    