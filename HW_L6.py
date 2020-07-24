import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
import warnings
from itertools import product
from datetime import datetime, timedelta
import calendar


train = pd.read_csv("E://Python_proj//python_Homework//Data_Engine_with_Python-master (3)//Data_Engine_with_Python-master//L6//jetrail//train.csv")
#print(train.head())

train['DateTime'] = pd.to_datetime(train.Datetime,format='%d-%m-%Y %H:%M')
train.index = train.DateTime

train.drop(['Datetime','ID'],axis=1,inplace=True)
#train.to_csv("E://Python_proj//python_Homework//train_clean.csv")
#print(train.head())

#整理数据
def cleanData(train,period):
    period_train = train.resample(period).sum()
  
    period_train['ds'] = period_train.index
    period_train['y'] = period_train.Count
    period_train.drop(['Count'],axis=1,inplace=True)

    return period_train

#画原始数据

fig = plt.figure(figsize=[15, 7])
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.suptitle('交通流量', fontsize=20)
plt.subplot(221)
plt.plot(cleanData(train,'D').y, '-', label='按天')
plt.legend()
plt.subplot(222)
plt.plot(cleanData(train,'M').y, '-', label='按月')
plt.legend()
plt.subplot(223)
plt.plot(cleanData(train,'Q-DEC').y, '-', label='按季度')
plt.legend()
plt.subplot(224)
plt.plot(cleanData(train,'A-DEC').y, '-', label='按年')
plt.legend()
plt.show()



# 设置参数范围
def find_bestmodel(period_train):
    ps = range(0, 5)
    qs = range(0, 5)
    ds = range(1, 2)
    parameters = product(ps, ds, qs)
    parameters_list = list(parameters)
    # 寻找最优ARMA模型参数，即best_aic最小
    results = []
    best_aic = float("inf") # 正无穷
    for param in parameters_list:
        try:
            #model = ARIMA(df_month.Price,order=(param[0], param[1], param[2])).fit()
            # SARIMAX 包含季节趋势因素的ARIMA模型
            model = sm.tsa.statespace.SARIMAX(period_train.y,
                                    order=(param[0], param[1], param[2]),
                                    #seasonal_order=(4, 1, 2, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False).fit()

        except ValueError:
            print('参数错误:', param)
            continue
        aic = model.aic
        if aic < best_aic:
            best_model = model
            best_aic = aic
            best_param = param
        results.append([param, model.aic])
        # 输出最优模型
    #print('最优模型: ', best_model.summary())
    return  best_model


month_train = cleanData(train,'M')
# 设置future_month，需要预测的时间date_list
month_train2 = month_train[['y']]
#print(month_train2.head())
future_month = 3
last_month = pd.to_datetime(month_train.index[len(month_train)-1])
#print(last_month)

date_list = []
for i in range(future_month):
    # 计算下个月有多少天
    year = last_month.year
    month = last_month.month
    if month == 12:
        month = 1
        year = year+1
    else:
        month = month + 1
    next_month_days = calendar.monthrange(year, month)[1]
    #print(next_month_days)
    last_month = last_month + timedelta(days=next_month_days)
    date_list.append(last_month)
#print('date_list=', date_list)


future = pd.DataFrame(index=date_list, columns= month_train.columns)
month_train2 = pd.concat([month_train2, future])

# get_prediction得到的是区间，使用predicted_mean
month_train2['forecast'] = find_bestmodel(month_train).get_prediction(start=0, end=len(month_train2)).predicted_mean

#month_train2.to_csv("E://Python_proj//python_Homework//month_train2.csv")

#流量预测结果显示
plt.figure(figsize=(30,7))
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
month_train2.y.plot(label='实际交通流量')
month_train2.forecast.plot(color='r', ls='--', label='预测交通流量')
plt.legend()
plt.title('交通流量（月）')
plt.xlabel('时间')
plt.ylabel('交通流量')
plt.show()


