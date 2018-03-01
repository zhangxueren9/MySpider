#coding=utf-8
import sys
import time
import random
import requests
import json
import codecs
from lxml import etree

HEADERS = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; '
                          '.NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 3.5.21022)Connection'},
           {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 '
                         '(KHTML, like Gecko) Version/5.1 Safari/534.50'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
           {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) '
                         'Version/5.1 Safari/534.50'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
           {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'},
           {'User-Agent':'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 '
                         '(KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'},
           {'User-Agent':'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; '
                         'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'},
           {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 '
                          '(KHTML, like Gecko) Version/4.0 Safari/534.13'}]

url = 'http://china.findlaw.cn/ask/question_43355287.html'

def GetProxies(url,headers):
    html = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')
    html = etree.HTML(html)
    proxies = html.xpath(u'//td[@data-title="IP"]/text() | //td[@data-title="PORT"]/text() | //td[@data-title="类型"]/text()')
    print(len(proxies))
    result = []
    for i in range(0,len(proxies),3):

        a = {proxies[i+2].lower() : "http://" + proxies[i] + ":" + proxies[i+1]}
        #print(a)
        result.append(a)

    return (result)

num = 0
url = 'https://www.kuaidaili.com/free/intr/1/'
headers = random.choice(HEADERS)

proxies_all = GetProxies(url,headers)
print(len(proxies_all))
avaiable_proxies = []
for each in proxies_all:
    print('正在测试 %s 代理'%each)
    for i in range(1):
        proxies = each
        headers = random.choice(HEADERS)

        html = requests.get(url, headers=headers,proxies = proxies).content.decode('utf-8', 'ignore')
        html = etree.HTML(html)
    num += 1
    print('可用')
print(num)