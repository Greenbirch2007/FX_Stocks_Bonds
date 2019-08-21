

# ! -*- coding:utf-8 -*-
# 增加index部位的手数
import time
import re
import pymysql
import requests
from lxml import etree
import time
import datetime
from math import floor

from selenium import webdriver




# 1.股票数据来自 雅虎日本
# 2.外汇数据来自  雅虎日本
# 3.债券数据来自 东京证券交易所（用10年期国债期货数据代替）


# 都假定做多
# 2019.8.18 日股重新开始(近半年的趋势，股指，国债下跌，日元升值)
Index_start = 20418  # 日经225指数
FX_start = 106.36     #美元日元 买价
Bond_start = 154.85  # 10年期国债期货





def get_index_PL():
    response = requests.get('https://stocks.finance.yahoo.co.jp/stocks/detail/?code=998407.O')
    html = response.text
    patt = re.compile('<td class="stoksPrice">(.*?)</td>',re.S)
    items = re.findall(patt,html)
    items_str = "".join(items[0].split(','))
    items_float = float(items_str)
    indexF_PL = (items_float-Index_start)/Index_start  * 100   # 百分比
    indexF_PL_2 = round(indexF_PL,2)
    indexF_PL_str = str(indexF_PL_2)
    big_list.append(indexF_PL_str)



def get_FX_PL():
    url = 'https://info.finance.yahoo.co.jp/fx/detail/?code=USDJPY=FX'
    headers = {'Useragent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
    response = requests.get(url, headers=headers)
    content = response.text
    patt = re.compile('<dd id="USDJPY_detail_ask">(.*?)<span class="large">(.*?)</span>(.*?)</dd></dl>',re.S)
    items = re.findall(patt, content)
    for nums in items:
        FX_f = "".join(nums)
        FX_PL = (float(FX_f)-FX_start)/FX_start  * 100 # 百分比
        FX__PL_4 = "%.4f"%FX_PL
        big_list.append(FX__PL_4)






def get_Bond_PL():
    try :
        driver = webdriver.Chrome()
        url = 'https://port.jpx.co.jp/jpx/template/quote.cgi?F=tmp/popchart&QCODE=601.555'
        driver.get(url)
        html = driver.page_source
        selector = etree.HTML(html)
        bond_num = selector.xpath('//*[@id="readArea"]/div[2]/div/table/tbody/tr[2]/td[6]/text()')
        Bond_f = bond_num[0][-6:]

        Bond_PL = (float(Bond_f)-Bond_start)/Bond_start    * 100 # 百分比
        Bond__PL_4 = "%.4f"%Bond_PL
        big_list.append(Bond__PL_4)
        driver.quit()
    except ValueError as e:
        pass








def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='FXSB',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    if len(big_list) == 3:
        cursor.executemany('insert into FXSB_Japan (Index_PL,FX_PL,Bond_PL) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    else:
        print('出列啦')



if __name__ == '__main__':
    while True:
        big_list = []
        get_index_PL()
        get_FX_PL()
        get_Bond_PL()
        l_tuple = tuple(big_list)
        content = []
        content.append(l_tuple)
        insertDB(content)
        time.sleep(10)
        print(datetime.datetime.now())
        time.sleep(5)




#
#
# create table FXSB_Japan(
# id int not null primary key auto_increment,
# Index_PL varchar(10),
# FX_PL varchar(10),
# Bond_PL varchar(10),
# LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# ) engine=InnoDB  charset=utf8;


# drop  table FXSB_Japan;

