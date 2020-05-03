'''
@author: kalarita
@Date: 2020-05-03 12:28:23
@LastEditors: kalarita
@LastEditTime: 2020-05-03 21:27:53
@FilePath: \undefinedc:\canlendarProject\DiaryCanlendar\getTodayinHis.py
@note:安装hanziconv,beautifulsoup4
'''

from urllib.parse import quote, unquote, urlencode
import requests
import datetime
import logging
import re
from bs4 import BeautifulSoup
from hanziconv import HanziConv

#获取数据
def getdata(url):
    """
    从url获取页面信息,使用bs4获取指定位置的信息,由于页面上的大事记和出生应该是固定的,
    所以以这两个为标志点获取
    """
    usefulstr = ""
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,"html.parser")
        soup.prettify()
        result = soup.getText()
        begin_index = result.find("大事记[编辑]")+7 #获取历史上的今天开始位置
        end_index = result.find("出生[编辑]")   #获取历史上的今天结束位置
        usefulstr = HanziConv.toSimplified(result[begin_index:end_index])   #将繁体中文简化
        usefulstr = re.sub(r'<ref>[\s\S]+?<ref>','',usefulstr)              #去掉里面所有的带有<ref>标签的内容,部分页面存在
        usefulstr = re.sub(r'\[来源请求\]','',usefulstr)                    #把带有[来源请求]的都给去掉
        usefulstr = re.sub(r'公元[\s\S]+?。','',usefulstr)                  #去掉公元前的内容
        print(usefulstr)    
    except:
        print("cannot connect to target website")
        logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
    return usefulstr

#数据处理
def managedata(data):
    managed_data = data.replace('\n', '').replace('\r', '').replace('\s', '').replace(' ','').strip()       #去除所有的空格以及换行符

    s = r'(\d{3,4}[\s\S]+?。)'#这是用来用年份进行分割的正则
    rms = r'\d{1,2}[\s\S]{2}\[编辑\]'

    managed_data = re.sub(rms,'',managed_data)
    print("这是去掉了小标题的数据")
    print(managed_data)
    managed_data =list(set(re.split(s,managed_data))) 
    tmp = [0]*len(managed_data)
    for i in range(0,len(managed_data)):
        tmp[i] = managed_data[i]                                            #进行深拷贝
    for i in range(0,len(managed_data)):
        if managed_data[i] != '':
            if managed_data[i][0].isdigit() == False or managed_data[i][5] != "：" and  managed_data[i][4] != "：" and managed_data[i][5] != ":":         #在这里判断一个元素是不是类似"1858年:"的格式,如果是则进行保留,如果不是直接删掉
                tmp[i] = ''
    tmp = list(set(tmp))                                                    #使用set方法进行去重,然后第一个元素直接pop出来,保留的就是只有语句的列表
    tmp.pop(0)
    tmp.sort()                                                              #直接利用自带的sort进行排序,除了三位数的年份会跑到最后面之外,其他暂时没有问题
    managed_data = tmp
    return managed_data

#格式化时间,获取当日url
def format_date():
    cmonth = int(datetime.date.today().strftime('%m'))   
    cday = int(datetime.date.today().strftime('%d'))
    datestr = str(cmonth+5) + "月" + str(cday) + "日"
    print(datestr)
    return datestr


def main():
    head_url = r'https://zh.wikipedia.org/wiki/'
    url = head_url + format_date()
    print(url)
    data = getdata(url)
    if data != "":
        managed_data = managedata(data)
        print(managed_data)
        print("获取的数据长度为"+str(len(managed_data)))
        with open("today.txt","w+") as f:
            for i in range(0,len(managed_data)):
                f.writelines(managed_data[i]+"\n")
if __name__ == "__main__":
    main()

