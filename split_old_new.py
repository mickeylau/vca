#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:13:22 2018

@author: mickey
"""

import pandas as pd

quandl=pd.read_csv('/Users/mickey/desktop/final_quandl.csv', index_col=None)

data_list=pd.read_csv('/Users/mickey/data_list.csv', index_col=None)

new_fea=data_list['list 1']

old_fea=data_list['list 2']

new_features=quandl[new_fea]

old_features=quandl[old_fea]

new_features.to_csv('/Users/mickey/desktop/new_features.csv', index=False)

old_features.to_csv('/Users/mickey/desktop/old_features.csv', index=False)