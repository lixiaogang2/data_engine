import requests

from bs4 import BeautifulSoup as bs

import pandas as pd


# 请求URL
def get_page(request_url):
    
    # 得到页面的内容

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

    html = requests.get(url = request_url, headers = headers, timeout = 10)

    content = html.text

    # 通过content创建BeautifulSoup对象

    soup = bs(content, 'html.parser')

    #返回soup

    return soup

#解析soup，返回dataframe
def analysis(soup):
    #查找class为tslb_b的div标签
    temp = soup.find('div',class_='search-result-list')
    #创建dataframe
    df = pd.DataFrame(columns=['name','price','img'])
    #查找temp中class为search-result-list-item的div标签
    car_list = temp.find_all('div',class_='search-result-list-item')
    #查找car列表里的car
    for car in car_list:
        #创建temp字典
        temp = {}
        #查找img标签
        temp['img'] = 'http:'+car.find('img').get('src')
        p_list = car.find_all('p')
        #temp字典赋值
        temp['name'], temp['price'] = p_list[0].text, p_list[1].text
        #把temp赋值给dataframe
        df = df.append(temp, ignore_index=True)
    #返回每一页的df
    return df

#创建一个用来放多页数据集合的dataframe
result = pd.DataFrame(columns=['name','price','img'])
#下载1页的数据
page_num = 1
#基础的URL，用来更新url
base_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
#翻页
for i in range(page_num):
    #拼接URL
    request_url = base_url+ '&page=' + str(i+1)
    #调用get_page,返回soup
    soup = get_page(request_url)
    #分析soup，返回每一页的数据
    df = analysis(soup)
    #把每一页数据合成
    result = result.append(df,ignore_index=True)
#分离price
result['price_L'], result['price_H'] = result['price'].str.split('-', 1).str
result['price_H'] = result['price_H'].str.replace('万','')
result = result.drop(columns=['price'], axis=1)
#保存
result.to_csv("E://Python_proj//python_Homework//car_result.csv",index=False,encoding = 'gbk')

