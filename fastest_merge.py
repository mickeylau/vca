#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:22:28 2018

@author: mickey
"""
import pandas as pd
import os
import glob

file_path='/Users/mickey/desktop/quandl_final_product/'
os.chdir(file_path)
files=glob.glob("*.csv")
df_list=pd.DataFrame()

def GetFile(fnombre):
    location = '/Users/mickey/desktop/quandl_final_product/' + fnombre
    df = pd.read_csv(location,index_col=None)
    return df

# list comprehension
df = [GetFile(file) for file in files]
dftot = pd.concat(df)

dftot.to_csv('/Users/mickey/desktop/final_quandl.csv', index=False)