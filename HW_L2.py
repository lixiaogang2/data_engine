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
    temp = soup.find('div',class_='tslb_b')
    #创建dataframe
    df = pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
    #查找temp中所有的tr标签
    tr_list = temp.find_all('tr')
    #查找tr列表里的tr
    for tr in tr_list:
        #创建temp字典
        temp = {}
        #查找td标签的列表，find和find_all区别？
        td_list = tr.find_all('td')
        #第一个tr中没有td，要做判断
        if len(td_list)>0:
            #id, brand, car_model, type, desc, problem, datetime, status = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text,td_list[6].text, td_list[7].text
            #temp字典赋值
            temp['id'], temp['brand'], temp['car_model'], temp['type'], temp['desc'], temp['problem'], temp['datetime'], temp['status'] = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text,td_list[6].text, td_list[7].text
            #把temp赋值给dataframe
            df = df.append(temp, ignore_index=True)
    #返回每一页的df
    return df

#创建一个用来放多页数据集合的dataframe
result = pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
#下载20页的数据
page_num = 20
#基础的URL，用来更新url
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
#翻页
for i in range(page_num):
    #拼接URL
    request_url = base_url+ str(i+1)+'.shtml'
    #调用get_page,返回soup
    soup = get_page(request_url)
    #分析soup，返回每一页的数据
    df = analysis(soup)
    #把每一页数据合成
    result = result.append(df,ignore_index=True)

print(result)

