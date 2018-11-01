#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 14:59:59 2018

@author: mickey
"""

import pandas as pd

company_list_path = '/Users/mickey/Downloads/SHARADAR_SF1_ca92b2a8644552921117037fafddde6c.csv'
    #   Reading companyId and remove duplicates
df = pd.read_csv(company_list_path,header=0,index_col=None)
companylist = pd.unique(df['ticker']).tolist()
#
#     #   Output setting
length = len(companylist)
count = 0
import datetime
def get_date(s_date):
    try:
        return datetime.datetime.strptime(s_date, "%d/%m/%Y")
    except:
            try:
                return datetime.datetime.strptime(s_date, "%Y-%m-%d")
            except:
                print(s_date)
                pass
df = df[df['dimension'].isin(['MRT','ART'])]
df['datekey']=df['datekey'].apply(get_date)
df['calendardate']=df['calendardate'].apply(get_date)

date_list_path = "/Users/mickey/Desktop/rebalance_dates_list.csv"
rebalance_dates = pd.read_csv(date_list_path)
time_list = rebalance_dates['date'].tolist()
 


   
for company in companylist:
    list_ = []
    new = df[df['ticker']==company].copy()
    new_date=new['datekey']
    count += 1
    if new.shape[0] > 0:
        
        real_date=[]    
############
        for i in new_date:
            real_date.append(pd.to_datetime(str(i), format='%Y-%m-%d'))
        for eachdate in time_list:
            
            date_ = pd.to_datetime(str(eachdate), format='%d/%m/%Y')
            if date_ >= min(real_date) and date_<=max(real_date):
                new_df = new[new["datekey"] <= date_]
                new_df = new_df.sort_values(by=['calendardate','datekey'], ascending=True)
                new_df.insert(0, 'rebalanceDates', str(eachdate))
                new_df = pd.DataFrame(new_df.tail(1))
                list_.append(new_df)

            
    if len(list_)>0:
        frame = pd.concat(list_)
        frame = frame.reset_index()
        filename = "/Users/mickey/Desktop/quandl_output3/"+str(company)+".csv"
        frame.to_csv(filename,index=False)
    del list_
    print(count,'/',length)
    del new
del df

'''
if len(list_)>0:
    frame = pd.concat(list_)
    frame = frame.reset_index()
    filename = 'mickey.csv'
    frame.to_csv(filename)
del list_
'''


"""            
        for eachdate in time_list:    
            date = pd.to_datetime(str(eachdate), format='%Y%m%d')
            new_df = new[new["datekey"] <= date]
            new_df = new_df.sort_values(by=['calendardate','datekey'], ascending=True)
            new_df.insert(0, 'rebalanceDates', str(eachdate))
            new_df = pd.DataFrame(new_df.tail(1))
            list_.append(new_df)
            del new_df
"""            
            