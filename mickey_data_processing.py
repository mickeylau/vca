#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 10:24:56 2018

@author: mickey
"""

import os
import glob
import pandas as pd

import time
import datetime
import re

full_trade_id=pd.read_csv('/Users/mickey/desktop/tradingItemId.csv', encoding='utf-8')
map_ = pd.read_csv('/Users/mickey/map.csv', encoding='utf-8')       
pricing_date=full_trade_id['pricingDate']

temp_date_list=[]
for date_ in pricing_date:
    try:  
        temp_date_list.append(time.mktime(datetime.datetime.strptime(str(date_), str("%Y-%m-%d %H:%M:%S.%f")).timetuple()))
    except Exception:
        temp_date_list.append("N/A")

full_trade_id['timestamp']=temp_date_list


tradinglist = pd.unique(full_trade_id['tradingItemId']).tolist()


length = len(tradinglist)
count = 0

start_date=[]
end_date=[]
trading_id=[]
time_diff=[]
for company in tradinglist:
    trading_id.append(company)
    new =full_trade_id[full_trade_id['tradingItemId']==company].copy()
    try:
        start_date.append(min(new['timestamp']))
        end_date.append(max(new['timestamp']))  
        time_diff.append(min(new['timestamp']-max(new['timestamp'])))        
    except Exception:
        start_date.append("N/A")
        end_date.append("N/A")
        time_diff.append("N/A")
summary_df=pd.DataFrame()
summary_df['start_date']=start_date
summary_df['end_date']=end_date
summary_df['tradingItemId2']=trading_id
summary_df['time_diff']=time_diff
for i in range(len(summary_df)):
    if start_date[i]=='N/A':
        summary_df=summary_df.drop(summary_df.index[i])

company_id_=[]
unrecorded_company=[]
for i in range(len(summary_df)):
    elm=summary_df['tradingItemId2'].iloc[i]
    the_list=map_['tradingItemId']
    index=the_list[the_list==elm].index.values
    try:
        index=int(index)
        company_id_.append(map_['companyId'].iloc[index])
    except Exception:
        unrecorded_company.append(index)
        company_id_.append('N/A')
    
summary_df['company_id']=company_id_    
    
########### summary_df cleaned ###############
        
map_ = pd.read_csv('/Users/mickey/map.csv', encoding='utf-8')         
companylist=pd.unique(map_['companyId']).tolist()
yes=0
win_trading_id_list=[]
company_id_list=[]
for company in companylist:
    new=[]
    new =map_[map_['companyId']==company].copy() 
    
    """sort by end date"""
    a=summary_df['tradingItemId2']
    new_end_date=[]
    drop_list=[]
    for i in range(len(new)):
        temp_trading_id=new['tradingItemId'].iloc[i]
        index=a[a==temp_trading_id].index.values
        try: 
            index=int(index)
            end_date=end=summary_df['end_date'].iloc[index]
            new_end_date.append(end_date)
        except Exception:            
            drop_list.append(i)
            pass
    new=new.drop(new.index[drop_list])
    new['end_date']=new_end_date
    new=new.sort_values('end_date',ascending=False)
    new=new.reset_index(drop=True)
               
    
    
    try:
        temp_trading_id=new['tradingItemId'].loc[0]
        a=summary_df['tradingItemId2']
        index=a[a==temp_trading_id].index.values
        index=int(index)   
        start=summary_df['start_date'].loc[index]
        end=summary_df['end_date'].loc[index]
        win_trading_id=str(new['tradingItemId'].loc[0])
        
        for i in range(len(new)-1):
            if len(new)-1 !=0:
                temp_trading_id=new['tradingItemId'].loc[i+1]
                index=a[a==temp_trading_id].index.values
                try: 
                    index=int(index)
                    cha_start=summary_df['start_date'].loc[index]
                    cha_end=summary_df['end_date'].loc[index]
                    
                    if cha_end>=end and cha_start<start:
                        start=cha_start
                        end=cha_end
                        win_trading_id=str(int(new['tradingItemId'].iloc[i+1]))
                    elif cha_start>start and cha_start<end and cha_end>end:
                        end=cha_end
                        win_trading_id=str(int(new['tradingItemId'].iloc[i+1]))
                    elif cha_start<start and cha_end>start and cha_end<end:
                        start=cha_start
                        win_trading_id=str(win_trading_id)
                    elif (cha_start>end):
                        win_trading_id=str(win_trading_id)+'_'+str(int(new['tradingItemId'].iloc[i+1]))
                        end=cha_end      
                    elif  cha_end<start:
                        win_trading_id=str(int(new['tradingItemId'].iloc[i+1]))+'_'+str(win_trading_id)
                        start=cha_start      
                    else: 
                        pass
                except Exception:
                    pass
            else:
                pass
        win_trading_id_list.append(win_trading_id)
        company_id_list.append(company)
    except Exception:
        pass
    
mapping_output=pd.DataFrame()
mapping_output['company_id_list']=company_id_list 
mapping_output['win_trading_id_list']=win_trading_id_list

mapping_output.to_csv("/Users/mickey/desktop/mapping_output3.csv",index=False)    
    
###################################################################################################################################################################################################################################################################################################################################################


import os
import glob
import pandas as pd
import time
import datetime
import re

import datetime
import dateutil.relativedelta
import dateutil as dt
from datetime import datetime

full_trade_id=pd.read_csv('/Users/mickey/desktop/tradingItemID.csv', encoding='utf-8')

pricing_date=full_trade_id['pricingDate']

today_date_list=[]
one_month_return_date=[]
three_month_return_date=[]
six_month_return_date=[]
twelve_month_return_date=[]

for date_ in pricing_date:
    try:
        today = datetime.strptime(date_, "%Y-%m-%d %H:%M:%S.%f")
        one_month_date=datetime.strptime(date_, "%Y-%m-%d %H:%M:%S.%f")- dt.relativedelta.relativedelta(months=1)
        three_month_date=datetime.strptime(date_, "%Y-%m-%d %H:%M:%S.%f")- dt.relativedelta.relativedelta(months=3)
        six_month_date=datetime.strptime(date_, "%Y-%m-%d %H:%M:%S.%f")- dt.relativedelta.relativedelta(months=6)
        twelve_month_date=datetime.strptime(date_, "%Y-%m-%d %H:%M:%S.%f")- dt.relativedelta.relativedelta(months=12)
        
        
        today_date=today.strftime('%m-%d-%Y')
        one_month_date=one_month_date.strftime('%m-%d-%Y')
        three_month_date=three_month_date.strftime('%m-%d-%Y')
        six_month_date=six_month_date.strftime('%m-%d-%Y')
        twelve_month_date=twelve_month_date.strftime('%m-%d-%Y')
        
        
        today_date_list.append(today_date)
        one_month_return_date.append(one_month_date)
        three_month_return_date.append(three_month_date)
        six_month_return_date.append(six_month_date)
        twelve_month_return_date.append(twelve_month_date)
        
        
    except Exception:
        today_date_list.append("N/A")
        one_month_return_date.append("N/A")
        three_month_return_date.append("N/A")
        six_month_return_date.append("N/A")
        twelve_month_return_date.append("N/A")


full_trade_id['today_date']=today_date_list
full_trade_id['one_month_return_date']= one_month_return_date
full_trade_id['three_month_return_date']= three_month_return_date
full_trade_id['six_month_return_date']= six_month_return_date
full_trade_id['twelve_month_return_date']= twelve_month_return_date

full_trade_id.to_csv('/Users/mickey/desktop/full_trade_id.csv',index=False)
################################################################################3
import bisect
import time 
import datetime

tradinglist = pd.unique(full_trade_id['tradingItemId']).tolist()
for trader in tradinglist:
    new =full_trade_id[full_trade_id['tradingItemId']==trader].copy()
    count=0
    
    today_return=[]
    for i in range(len(new)):#write csv
        if count==0:
            today_return.append(0)
        else:
            try:
                today_return.append(new['divAdjPrice'].iloc[i]/new['divAdjPrice'].iloc[i-1]-1)
            except Exception:
                today_return.append("N/A")
        count+=1
    datelist=new['today_date'] 
    
    today_ts=[]
    for elm in datelist:
        today_ts.append(time.mktime(datetime.datetime.strptime(elm, "%m-%d-%Y").timetuple()))
    
    count=0
    one_month_return=[]
    three_month_return=[] 
    six_month_return=[]
    twelve_month_return=[]
    for i in range(len(new)):
        try:
            s=new['one_month_return_date'].iloc[i]
            s=time.mktime(datetime.datetime.strptime(s, "%m-%d-%Y").timetuple())
            index = bisect.bisect(today_ts, s )-1
            
            if index!=-1:           
                
                past_price=new['divAdjPrice'].iloc[index]
                if count==0:
                    one_month_return.append(0)
                else:
                
                    one_month_return.append(new['divAdjPrice'].iloc[i]/past_price-1)
                
            else:
                one_month_return.append("")
        except Exception:
            one_month_return.append("N/A")
            
         
        try:
            s=new['three_month_return_date'].iloc[i]
            s=time.mktime(datetime.datetime.strptime(s, "%m-%d-%Y").timetuple())
            index = bisect.bisect(today_ts, s )-1
            
            if index!=-1:           
                
                past_price=new['divAdjPrice'].iloc[index]
                if count==0:
                    three_month_return.append(0)
                else:
                
                    three_month_return.append(new['divAdjPrice'].iloc[i]/past_price-1)
                
            else:
                three_month_return.append("")
        except Exception:
            three_month_return.append("N/A")    
            
            
        try:
            s=new['six_month_return_date'].iloc[i]
            s=time.mktime(datetime.datetime.strptime(s, "%m-%d-%Y").timetuple())
            index = bisect.bisect(today_ts, s )-1
            
            if index!=-1:           
                
                past_price=new['divAdjPrice'].iloc[index]
                if count==0:
                    six_month_return.append(0)
                else:
                
                    six_month_return.append(new['divAdjPrice'].iloc[i]/past_price-1)
                
            else:
                six_month_return.append("")
        except Exception:
            six_month_return.append("N/A")    
            
        
        try:
            s=new['twelve_month_return_date'].iloc[i]
            s=time.mktime(datetime.datetime.strptime(s, "%m-%d-%Y").timetuple())
            index = bisect.bisect(today_ts, s )-1
            
            if index!=-1:           
                
                past_price=new['divAdjPrice'].iloc[index]
                if count==0:
                    twelve_month_return.append(0)
                else:
                
                    twelve_month_return.append(new['divAdjPrice'].iloc[i]/past_price-1)
                
            else:
                twelve_month_return.append("")
        except Exception:
            twelve_month_return.append("N/A")    
            
        count+=1
    new['today_return']=today_return    
    new['one_month_return']=one_month_return
    new['three_month_return']=three_month_return
    new['six_month_return']=six_month_return
    new['twelve_month_return']=twelve_month_return
    try:
        filename='/Users/mickey/desktop/totalreturn_output/'+str(int(trader))+'.csv'
    except Exception:
        filename='/Users/mickey/desktop/totalreturn_output/'+str(trader)+'.csv'
    new.to_csv(filename,index=False)
    
    
 ################################################################################################################################################################################################################################################################################################################################################
import time
import datetime
import bisect

reba_date_df=pd.read_csv('/Users/mickey/desktop/rebalance_dates_list.csv')
reba_date_list=reba_date_df.iloc[:,0]
reba_date_ts=[]
for elm in reba_date_list:
    reba_date_ts.append(time.mktime(datetime.datetime.strptime(elm, "%d/%m/%Y").timetuple()))

import os
import glob
indir="/Users/mickey/desktop/totalreturn_output/"
os.chdir(indir)
fileList=glob.glob("*.csv")

for filename in fileList:
    temp_csv=pd.read_csv(filename)
    pricing_date=temp_csv['pricingDate'][:]
    
    pricing_date_ts=[]
    for elm in pricing_date:
        pricing_date_ts.append(time.mktime(datetime.datetime.strptime(elm, "%Y-%m-%d %H:%M:%S.%f").timetuple()))
    
    
    real_reba_date=[]    
    for i in range(len(pricing_date)):
        s=pricing_date_ts[i]    
        index = bisect.bisect(reba_date_ts, s)-1
                
        if index>=-1:                           
            real_reba_date.append(reba_date_list[index+1])
            
    temp_csv['rebalance_date']=real_reba_date
    temp_csv.to_csv('/Users/mickey/desktop/totalreturn_output2/'+filename, index=False)
    
  ############################################################################################################################################################################################################################################################################################################################################
map_output=pd.read_csv('/Users/mickey/desktop/mapping_output3.csv')

a=map_output['win_trading_id_list']
list_1=[]
#real_map_output=[]
elm_list=[]
for elm in a:
    #real_map_output.append(elm)
    chars = set(elm)
    if '_' in chars:
        list_1.append(elm.split('_'))
        elm_list.append(str(elm))
    else:
        pass
    
for i in range(len(list_1)):
    lala=pd.DataFrame()
    for j in range(len(list_1[i])):
        temp=list_1[i][j]
        temp=pd.read_csv('/Users/mickey/desktop/totalreturn_output2/'+temp+'.csv')
        lala=lala.append(temp)
    file_name=elm_list[i]
    lala.to_csv('/Users/mickey/desktop/totalreturn_output2/'+file_name+'.csv',index=False)
    
#############################################################################################################################################################################################################################################################################################################################################

indir="/Users/mickey/desktop/Annual/"
os.chdir(indir)
folderList=[x[0] for x in os.walk(indir)]

i=0
for filename in folderList:
    gg=pd.DataFrame()
    folder_path=filename   
    os.chdir(folder_path)
    fileList=glob.glob("*.csv")
    for elm in fileList:
        temp=pd.read_csv(elm)
        temp_row=temp.iloc[-1, :]       
        gg=gg.append(temp_row)
    gg.to_csv('/Users/mickey/desktop/last_row/'+str(i)+'.csv')
    i+=1
    
#############################################################################################################################################################################################################################################################################################################################################

folder_path='/Users/mickey/Desktop/last_row/'
os.chdir(folder_path)
fileList=glob.glob("*.csv")

i=0
dfList=pd.DataFrame()

for filename in fileList:
    temp=folder_path+filename
    temp_df=pd.read_csv(temp)
    dfList=dfList.append(temp_df)
    i+=1
    print(i)
dfList.to_csv('/Users/mickey/Desktop/merged_all_company_info.csv')  

import pandas as pd

full_company_info=pd.read_csv('/Users/mickey/Desktop/merged_all_company_info.csv')
map_=pd.read_csv('/Users/mickey/Desktop/mapping_output3.csv')
the_list=map_['company_id_list']

companylist = pd.unique(full_company_info['companyId']).tolist()


for i in range(len(companylist)):
    companylist[i]=int(companylist[i])

final_result=pd.DataFrame()

for company in companylist:
    new_company =full_company_info[full_company_info['companyId']==company].copy()
    index=the_list[the_list==company].index.values
    
    try:
        index=int(index) #might hav error
    
        rebalance_date_list=[]
        for i in range(len(new_company['rebalanceDates'])):
            temp=str(new_company['rebalanceDates'].iloc[i])
            if temp[4]=='0':
                rebalance_date_list.append(temp[6:8]+'/'+temp[5:6]+'/'+temp[:4])
            else:
                rebalance_date_list.append(temp[6:8]+'/'+temp[4:6]+'/'+temp[:4])
        new_company['rebalance_date']=rebalance_date_list
        new_company=new_company.reset_index()    
        ###
        
        trading_id=map_['win_trading_id_list'][index]
        trading_df=pd.read_csv('/Users/mickey/Desktop/totalreturn_output2/'+str(trading_id)+'.csv')
        
        unique_date_list = pd.unique(trading_df['rebalance_date']).tolist()
        useful_trading_df=pd.DataFrame()
        for date in unique_date_list:
            new_trading_df =trading_df[trading_df['rebalance_date']==date].copy()
            useful_row=new_trading_df.iloc[-1]
            useful_trading_df=useful_trading_df.append(useful_row)
            
        
        result = pd.merge(new_company, useful_trading_df, on='rebalance_date')
        
        result.to_csv('/Users/mickey/Desktop/final_result/'+str(company)+'.csv')
        final_result=final_result.append(result)
    except Exception:
        pass
    
    
final_result.to_csv('/Users/mickey/desktop/final_result.csv')
