# 使用KMeans进行聚类
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np

# 数据加载

data = pd.read_csv('E://Python_proj//python_Homework//数据分析训练营-结营考试//ProjectC//CarPrice_Assignment.csv',encoding = 'gbk')
train_x = data[['symboling','CarName','fueltype','aspiration','doornumber','carbody','drivewheel','enginelocation','wheelbase','carlength','carwidth','carheight','curbweight','enginetype','cylindernumber','enginesize','fuelsystem','boreratio','stroke','compressionratio','horsepower','peakrpm','citympg','highwaympg','price']]
print(train_x.head())

# LabelEncoder，字符转换为数字
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
train_x['fueltype'] = le.fit_transform(train_x['fueltype'])
train_x['aspiration'] = le.fit_transform(train_x['aspiration'])
train_x['doornumber'] = le.fit_transform(train_x['doornumber'])
train_x['carbody'] = le.fit_transform(train_x['carbody'])
train_x['drivewheel'] = le.fit_transform(train_x['drivewheel'])
train_x['enginelocation'] = le.fit_transform(train_x['enginelocation'])
train_x['enginetype'] = le.fit_transform(train_x['enginetype'])
train_x['cylindernumber'] = le.fit_transform(train_x['cylindernumber'])
train_x['fuelsystem'] = le.fit_transform(train_x['fuelsystem'])

print(train_x.head())
# 规范化到 [0,1] 空间
min_max_scaler = preprocessing.MinMaxScaler()
train_x = train_x.drop(columns=['CarName'], axis=1)
train_x = min_max_scaler.fit_transform(train_x)
#pd.DataFrame(train_x).to_csv('E://Python_proj//python_Homework//数据分析训练营-结营考试//train_x.csv',encoding = 'gbk',index=False)
#print(train_x)


### 使用KMeans聚类
kmeans = KMeans(n_clusters=50)
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u'聚类结果'},axis=1,inplace=True)
print(result.head())
# 将结果导出到CSV文件中
result.to_csv('E://Python_proj//python_Homework//数据分析训练营-结营考试//ProjectC//kMeans.csv',encoding = 'gbk',index=False)



# K-Means 手肘法：统计不同K取值的误差平方和
import matplotlib.pyplot as plt
sse = []
for k in range(1, 204):
	# kmeans算法
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, 204)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()


#使用层次聚类
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
model = AgglomerativeClustering(linkage='ward', n_clusters=3)
y = model.fit_predict(train_x)
print(y)

linkage_matrix = ward(train_x)
dendrogram(linkage_matrix)
plt.show()


