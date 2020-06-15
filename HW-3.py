# 对汽车投诉信息进行分析
import pandas as pd

result = pd.read_csv('E://Python_proj//python_Homework//Data_Engine_with_Python-master//L1//car_data_analyze//car_complain.csv')
#print(result)
# 将genres进行one-hot编码（离散特征有多少取值，就用多少维来表示这个特征）
result = result.drop('problem', 1).join(result.problem.str.get_dummies(','))
#print(result.columns)


df= result.groupby(['brand'])['id'].agg(['count']).sort_values('count', ascending=False)
df2= result.groupby(['car_model'])['id'].agg(['count']).sort_values('count', ascending=False)
df3= result.groupby(['brand'])['car_model'].agg(['nunique'])
df4 = df.merge(df3, left_index=True, right_index=True, how='left')
df4['mean']=df4['count']/df4['nunique']
df4= df4.sort_values('mean', ascending=False).drop({'count','nunique'},1)

print(df)
print(df2)
print(df4)

