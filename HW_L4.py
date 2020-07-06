import numpy as np
from efficient_apriori import apriori
import pandas as pd



#Header=None,第一行不是标题
dataset = pd.read_csv('E://Python_proj//python_Homework//L4//Market_Basket_Optimisation.csv',header=None)
print(dataset.shape)

#将数据放到transactions里
transactions = []
for i in range(dataset.shape[0]):
    temp = []
    for j in range(0,20):
        if str(dataset.values[i,j])!= 'nan':
            temp.append(str(dataset.values[i,j]))
    transactions.append(temp)

#print(transactions)

# 挖掘频繁项集和频繁规则
itemsets, rules = apriori(transactions,min_support=0.05, min_confidence=0.2)
print('频繁项集：',itemsets)
print('关联规则：',rules)