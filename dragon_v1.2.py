#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:47:52 2018

@author: mickey
"""


def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as spstats
from sklearn.preprocessing import Imputer



train = pd.read_csv('/Users/mickey/Downloads/Dragon_181025/train.csv', encoding='utf-8') 

#for i in range(len(train)):
n=len(train)
na_percentage=[]

try:
    for i in range(147):
        column=train.columns[i]
        count=(n-train[column].count())/n
        if count>0.3:
            train=train.drop([column], axis=1)
        na_percentage.append(count)
except Exception:
    pass    


ww=len(train.columns)
predictor_data= train.iloc[:,0:ww]



"""replace outlier"""
for i in range(ww):
    qua_5=np.percentile(predictor_data.iloc[i], 5)
    qua_95=np.percentile(predictor_data.iloc[i], 95)
    for j in range(len(predictor_data.iloc[i])):  
        if predictor_data.iloc[i][j] >qua_95:
            predictor_data.iloc[i][j]=qua_95
        if predictor_data.iloc[i][j] <qua_5:
            predictor_data.iloc[i][j]=qua_5 



target=train['Target']

names=train.columns[0:ww]

"""handle NA"""



imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(predictor_data)
predictor_data = imp.transform(predictor_data)


"""split data"""
    
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
X_train, X_test, y_train, y_test = train_test_split(predictor_data, target, test_size=0.3, random_state=0)





#can consider L1惩罚项的逻辑回归作为基模型的特征选择

"""random forest classifier"""

"""
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(criterion = 'entropy', random_state=0)
tree.fit(X_train,y_train)
"""

from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(criterion='entropy', n_estimators=10,random_state=3,n_jobs=2)
forest.fit(X_train,y_train.values)

rank_01=pd.DataFrame()
rank_01['features']=names
rank_01['score']=forest.feature_importances_
#the score of the model is 0.41

temp = forest.feature_importances_.argsort()
rank_rf = np.empty_like(temp)
rank_rf[temp] = np.arange(len(forest.feature_importances_))

#print (sorted(zip(map(lambda x: round(x, 4), forest.feature_importances_),names ), reverse=True))


"""rf regressor"""

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
rf.fit(X_train, y_train.values.ravel()) #.values.ravel()

rank_02=pd.DataFrame()
rank_02['features']=names
rank_02['score']=rf.feature_importances_


#print(forest.score(X_test,y_test))
#the score is -0.31, so abanduned

"""logistics"""
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train.values.ravel())


#print(model.score(X_test, y_test.values.ravel()))
#score of model is 0.4

rank_03=pd.DataFrame()
rank_03['features']=names
coef=[]
for i in range(len(model.coef_[0])):
    coef.append(model.coef_[0][i])
rank_03['coef']=coef
abs_coef=[abs(number) for number in coef]
temp = np.array(abs_coef).argsort()
rank_logi_coef = np.empty_like(temp)
rank_logi_coef[temp] = np.arange(len(forest.feature_importances_))


#negative coef doesnt mean not important

#print('Intercept: \n', model.intercept_)

##########to make prediction##########
"""predicted= model.predict(X_test)"""
######################################

"""RFE: too slow"""

"""
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

#递归特征消除法，返回特征选择后的数据
#参数estimator为基模型
#参数n_features_to_select为选择的特征个数
rank_04=pd.DataFrame()
rfe = RFE(estimator=LogisticRegression(), n_features_to_select=2)
rfe = rfe.fit(X_train, y_train)

rfe2 = RFE(estimator=RandomForestClassifier(criterion='entropy', n_estimators=10,random_state=3,n_jobs=2), n_features_to_select=2)
rfe2 = rfe2.fit(X_train, y_train)
"""
"""
from sklearn.svm import SVR
rfe3 = RFE(estimator=SVR(kernel="linear"), n_features_to_select=2)
rfe3 = rfe3.fit(X_train, y_train)
"""


"""stability selection: see which feature is selected most"""

from sklearn.linear_model import RandomizedLasso
 
rlasso = RandomizedLasso(alpha=0.025)
rlasso.fit(X_train, y_train.values.ravel())

rlasso_score= rlasso.scores_

temp = rlasso.scores_.argsort()
ranks = np.empty_like(temp)
ranks[temp] = np.arange(len(rlasso.scores_))


#print (sorted(zip(map(lambda x: round(x, 4), rlasso.scores_), names), reverse=True))
    
    
    
rank_summary=pd.DataFrame()    
rank_summary['features']=names
#rank_summary['ranking_logi']=94-rfe.ranking_
#rank_summary['ranking_RF']=94-rfe2.ranking_
#rank_summary['ranking_svm']=94-rfe3.ranking_
rank_summary['ranking_stab_sel']=ranks
rank_summary['ranking_rf_importance']=rank_rf
rank_summary['ranking_logi_coef']=rank_logi_coef

### the higher the better
selected_feature=[]
for i in range(len(rank_summary)):
    temp=0
    for x in rank_summary.iloc[i][1:6]:
        if x>80:
            temp=temp+1
    if temp>=2:
        selected_feature.append(names[i])


#useful_features_data=RFE(estimator=LogisticRegression(), n_features_to_select=2).fit_transform(X_train, y_train.values.ravel())

rank_summary.to_csv("/Users/mickey/desktop/fea_rank_sum.csv",index=False)

############ Finish feature eng ################
"""end of feature selection"""



train = pd.read_csv('/Users/mickey/Downloads/Dragon_181025/train.csv', encoding='utf-8') 
test = pd.read_csv('//Users/mickey/Downloads/Dragon_181025/test.csv', encoding='utf-8') 
ID = test['ID']


n=len(train)
na_percentage=[]

try:
    for i in range(147):
        column=train.columns[i]
        count=(n-train[column].count())/n
        if count>0.3:
            train=train.drop([column], axis=1)
        na_percentage.append(count)
except Exception:
    pass    


ww=len(train.columns)
predictor_data= train.iloc[:,0:ww]

selected_feature.remove('Target')
predictor_data=predictor_data[selected_feature]

"""replace outlier"""
for i in range(147):
    qua_5=np.percentile(predictor_data.iloc[i], 5)
    qua_95=np.percentile(predictor_data.iloc[i], 95)
    for j in range(len(predictor_data.iloc[i])):  
        if predictor_data.iloc[i][j] >qua_95:
            predictor_data.iloc[i][j]=qua_95
        if predictor_data.iloc[i][j] <qua_5:
            predictor_data.iloc[i][j]=qua_5 



test=test[selected_feature]


target=train['Target']


imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(predictor_data)
predictor_data = imp.transform(predictor_data)
test=imp.transform(test)

X_train, X_test, y_train, y_test = train_test_split(predictor_data, target, test_size=0.3, random_state=0)


"""boost"""

from sklearn.ensemble import AdaBoostClassifier
model3 = AdaBoostClassifier(n_estimators = 100)
model3.fit(predictor_data, target)
boost_score=model3.score(predictor_data, target.ravel())
boost_predicted= model3.predict_proba(test)

"""logistics"""

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(predictor_data, target.ravel())
logi_score=model.score(predictor_data, target.ravel())
#score of model is 0.4
logi_predicted= model.predict_proba(test)


"""naive baye"""
from sklearn.naive_bayes import BernoulliNB
clf = BernoulliNB()
clf.fit(predictor_data, target)
nb_score=clf.score(predictor_data,target)
nb_predicted=clf.predict_proba(test)


"""neigh_predicted: not accurate"""
"""
from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier(n_neighbors=15, leaf_size=50)
neigh.fit(predictor_data, target)
neigh_score=neigh.score(predictor_data,target)
neigh_predicted=neigh.predict_proba(test)
"""


"""bag: too slow"""
"""
from sklearn import cross_validation, ensemble, preprocessing, metrics
bag = ensemble.BaggingClassifier(n_estimators = 100)
bag_fit = bag.fit(predictor_data, target)
bag_predicted = bag.predict_proba(test)

accuracy = metrics.accuracy_score(test, bag_predicted)
"""



"""tree：no test proba"""
"""
from sklearn import tree
clf = tree.DecisionTreeClassifier()

clf =tree.DecisionTreeRegressor()
clf = clf.fit(predictor_data, target)
tree_score=clf.score(predictor_data, target)
tree_predicted=clf.predict_proba(test)
"""

"""RF: absolutely not accurate"""
"""
forest = RandomForestClassifier(criterion='gini', n_estimators=5000,n_jobs=2)
forest.fit(predictor_data, target)
forest_score=forest.score(X_test,y_test)
forest_predicted= forest.predict_proba(test)
"""

"""SVM: too slow"""
"""
from sklearn import svm

model2 = svm.SVC(probability=True)
model2.fit(predictor_data, target)

svm_score=model.score(predictor_data, target.ravel())
svm_predicted= model2.predict_proba(test)

"""

#####################################
total_score=logi_score+boost_score+nb_score
#+neigh_score
#+forest_score

pred = logi_score*logi_predicted[:, 1]/total_score +boost_score*boost_predicted[:, 1]/total_score +nb_score*nb_predicted[:, 1]/total_score 
#+neigh_score*neigh_predicted[:, 1]/total_score 
#+forest_score*forest_predicted[:, 1]/total_score              # Get the probabilty of being 1. 
pred_df = pd.DataFrame(data={'Target': pred})


submissions = pd.DataFrame(ID).join(pred_df)
submissions.to_csv("/Users/mickey/desktop/dragon_test_submissions07.csv",index=False)