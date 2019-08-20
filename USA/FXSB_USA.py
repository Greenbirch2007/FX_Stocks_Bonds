

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
from requests.exceptions import RequestException
from selenium import webdriver




# 1.股票数据来自 # 网页财经
# 2.外汇数据来自  # 东方财富
# 3.债券数据来自 雅虎　美国10年期国债收益率


# 都假定做多
# 2019.8.18 日股重新开始(近半年的趋势，股指，国债下跌，日元升值)
Index_start = 2900  # 东方财富
FX_start = 98     #东方财富
Bond_start = 1.6  #雅虎　美国10年期国债收益率



def get_index_PL():
    driver = webdriver.Chrome()

    try :
        url = 'http://quote.eastmoney.com/gb/zsSPX.html'
        driver.get(url)
        html = driver.page_source
        time.sleep(1)
        selector = etree.HTML(html)
        index_num = selector.xpath('//*[@id="arrowud"]/strong/text()')
        index_f = index_num[0]

        Index_PL = (float(index_f)-Index_start)/Index_start    * 100 # 百分比
        Index__PL_4 = "%.4f"%Index_PL
        big_list.append(Index__PL_4)
        driver.quit()

    except ValueError as e:
        pass






def get_FX_PL():
    driver = webdriver.Chrome()

    try :
        url = 'http://quote.eastmoney.com/globalfuture/UDI.html'
        driver.get(url)
        html = driver.page_source
        selector = etree.HTML(html)
        fx_num = selector.xpath('//*[@id="arrowud"]/strong/text()')
        fx_f = fx_num[0]

        FX_PL = (float(fx_f)-FX_start)/FX_start
        FX_PL_100 = FX_PL * 100 # 百分比
        FX__PL_4 = "%.4f"%FX_PL_100


        big_list.append(FX__PL_4)
        driver.quit()

    except ValueError as e:
        pass




def get_Bond_PL():
    driver = webdriver.Chrome()

    try :
        url = 'https://finance.yahoo.com/quote/%5ETNX/history?p=%5ETNX'
        driver.get(url)
        html = driver.page_source
        selector = etree.HTML(html)
        bond_num = selector.xpath('//*[@id="quote-header-info"]/div[3]/div/div/span[1]/text()')
        bond_f = bond_num[0]
        Bond_PL = (float(bond_f)-Bond_start)/Bond_start
        Bond_PL_100 = Bond_PL * 100 # 百分比
        Bond__PL_4 = "%.4f"%Bond_PL_100


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
        cursor.executemany('insert into FXSB_USA (Index_PL,FX_PL,Bond_PL) values (%s,%s,%s)', content)
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
        print(datetime.datetime.now())



#
#
# create table FXSB_USA(
# id int not null primary key auto_increment,
# Index_PL varchar(10),
# FX_PL varchar(10),
# Bond_PL varchar(10)
# ) engine=InnoDB  charset=utf8;


# drop  table FXSB_USA;

