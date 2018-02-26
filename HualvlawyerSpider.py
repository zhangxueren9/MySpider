#coding=utf-8
import sys
import time
import random
import requests
from lxml import etree

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 3.5.21022)Connection'},
           {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
           {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
           {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'},
           {'User-Agent':'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'},
           {'User-Agent':'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'},
           {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13'}]


a = []
num = 0
f = open('data_link.txt','r')
lines = f.readlines()
for line in lines:
    a.append(line)
f.close()


url_home = 'http://www.66law.cn'


def GetDate(url,headers,filename):
    global num
    try:
            html = requests.get(url,headers=headers).content.decode('utf-8','ignore')
            html = etree.HTML(html)
            #获取律师信息
            name = html.xpath('//div[@class="cont-box" and @style="z-index:2;"]/div/p/a/text()')
            adress = html.xpath('//div[@class="cont-box" and @style="z-index:2;"]/div/ul/li[1]/span/text()')
            phone = html.xpath('//div[@class="cont-box" and @style="z-index:2;"]/div/ul/li[2]/span/text()')

            #被公众采纳标志，律师信息提取规则
            if len(name) == 0:
                name = html.xpath('//div[@class="cont-box" and @style="z-index:4;"]/div/p/a/text()')
                adress = html.xpath('//div[@class="cont-box" and @style="z-index:4;"]/div/ul/li[1]/span/text()')
                phone = html.xpath('//div[@class="cont-box" and @style="z-index:4;"]/div/ul/li[2]/span/text()')


                if len(name) == 0:
                    num = num +1
                    if num <= 50:
                        return(url)
                    if num >50:
                        continue_do = input("请输入验证码，通过后请输入‘A’继续爬取：")

                        while True:
                            if continue_do == 'A':
                                break
                        num = 0
                        return(url)
            #将数据写入
            f = open(filename,'a+')
            print('正在写入数据')
            for i in range(len(name)):
                lawyer = name[i] + '*' + adress[i] + '*' + phone[i] + '\n'
                f.write(lawyer)
            f.close()
            num = 0
    except:
        pass



for i in range(len(a)):
    if i < 100000 and i > 200000:
        i = i + 1
        break
    url = url_home + a[i][0:-1]
    headers1 = random.choice(headers)
    print('正在处理数据%s' % url)
    GetDate(url, headers1,'hualvlawyerv2.0(100000-200000).txt')
    i = i + 1
    progress = i/len(a)*100
    print('+++++------已完成%d-%d/%d---+++++'%(progress,i,len(a)))

print('---结束---')
