# 分析订单表客中的频繁项集和关联规则
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# 数据加载
temp = pd.read_csv('E://Python_proj//python_Homework//数据分析训练营-结营考试//ProjectB//订单表.csv',encoding='gbk')
order = temp[['客户ID','产品名称']]

# 将产品名称进行one-hot编码（离散特征有多少取值，就用多少维来表示这个特征）
df = order.groupby(['客户ID'])['产品名称'].agg([("temp",'-'.join)])
order_hot_encoded = df.drop('temp',1).join(df.temp.str.get_dummies('-'))
print(order_hot_encoded.head())

# 挖掘频繁项集，最小支持度为0.02
itemsets = apriori(order_hot_encoded,use_colnames=True, min_support=0.05)
# 按照支持度从大到小进行时候粗
itemsets = itemsets.sort_values(by="support" , ascending=False) 
print('-'*20, '频繁项集', '-'*20)
print(itemsets)
# 根据频繁项集计算关联规则，设置最小提升度为2
rules =  association_rules(itemsets, metric='lift', min_threshold=1.5)
# 按照提升度从大到小进行排序
rules = rules.sort_values(by="lift" , ascending=False) 
#rules.to_csv('./rules.csv')
print('-'*20, '关联规则', '-'*20)
print(rules)

