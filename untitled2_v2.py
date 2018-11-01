#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:34:18 2018

@author: mickey
"""

"""to handle the return"""

import pandas as pd
df = pd.read_csv("/Users/mickey/Downloads/SHARADAR_SEP_f71ea197447e1ef92407e7e92a63000c_2.csv",header=0,index_col=None)
companylist = pd.unique(df['ticker']).tolist()
length = len(companylist)
count = 0
df_list=pd.DataFrame()
for company in companylist:
    df_list=[]
    list_ = []
    new = df[df['ticker']==company].copy()
    new=new.sort_values(by=['date'], ascending=True)
    div=new['dividends'].tolist()
    close=new['close'].tolist()
    div_inv=div[::-1]
    close_inv=close[::-1]
    temp=[]
    adj_close=[]    
    for i in range(len(div_inv)):
        if div_inv[i]==0 or close_inv[i]==0:
            temp.append(1)
        elif div_inv[i] != 0:
            temp.append(1/(1+div_inv[i]/close_inv[i]))
    factor=[temp[0]]
    if len(div_inv)>1:
        for i in range(1,len(div_inv)):
            factor.append(factor[i-1]*temp[i])
    factor=factor[::-1]
    del factor[0]
    factor.append(1)
    for i in range(len(close)):
        adj_close.append(close[i]*factor[i])        
    temp_df=pd.DataFrame()
    temp_df['ticker']=new['ticker']
    temp_df['date']=new['date']
    temp_df['adj_close']=adj_close    
    date_list_path = "/Users/mickey/Desktop/rebalance_dates_list.csv"
    rebalance_dates = pd.read_csv(date_list_path)
    time_list = rebalance_dates['date'].tolist()
    real_date=[]
    temp_date=temp_df['date'].tolist()    
    for i in range(len(temp_df)):
        real_date.append(pd.to_datetime(str(temp_date[i]), format='%Y-%m-%d'))        
    temp_df['date']=real_date   
    count += 1
    if temp_df.shape[0] > 0:
        for eachdate in time_list:            
            date_ = pd.to_datetime(str(eachdate), format='%d/%m/%Y')
            if date_ >= min(real_date) and date_<=max(real_date):       
                new_df = temp_df[temp_df["date"] <= date_]
                new_df = new_df.sort_values(by=['date'], ascending=True)
                new_df.insert(0, 'rebalanceDates', str(eachdate))
                new_df = pd.DataFrame(new_df.tail(1))               
                df_list.append(new_df)
    del new    
    print(count,'/',length)    
    if len(df_list)>0:
        frame=pd.DataFrame()
        frame = pd.concat(df_list)
        frame = frame.reset_index()
        adj_close=frame['adj_close'].tolist()
        return_=[]
        for i in range(len(frame)-1):
            try:
                return_.append((adj_close[i+1]-adj_close[i])/adj_close[i])
            except Exception:
                return_.append('N/A')                
        return_.append('N/A')
        frame['return']=return_
        filename = "/Users/mickey/Desktop/return_output3/"+str(company)+".csv"
        frame.to_csv(filename,index=False)
    del df_list
    
    
             
    