#coding=utf-8
import sys
import time
import random
import requests
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 3.5.21022)Connection'},
           {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
           {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
           {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'}]

def GetData(url,headers): 
    
    try:
        html = requests.get(url,headers=headers).content.decode('utf-8').replace(u'\xa0', u' ')
        html = etree.HTML(html)

        #提取数据：分类、问题标题、问题链接、提问者地区
        category = html.xpath('//div[ @class="wt_list"]/table//tr/td/a[1]/text()')
        title = html.xpath('//div[ @class="wt_list"]/table//tr/td/a[2]/text()')
        title_link = html.xpath('//div[ @class="wt_list"]/table//tr/td/a[2]/@href')
        address = html.xpath('//div[ @class="wt_list"]/table//tr/td/u/text()')
        #date = html.xpath('//div[ @class="wt_list"]/table//tr/td[4]/text()')

        #反反爬虫策略
        if len(title) == 0:
            print('警告：请点击链接并输入验证码！！！')
            print(url)
            input = raw_input('Please in A to continue')
            while True:
            	if input == 'A':
            		break

        #将获取的数据写入文件
        f = open('hualv_questions_v2.6.3.txt','a+')
        print('****正在写入数据****')
        for i in range(len(title)):
            f.write(title[i] + '*')
            f.write(category[i] + '*')
            f.write(title_link[i] + '*')
            f.write(address[i] + '*')
            f.write('\n')

    except:
        #如果没成功，记录url
        print('wrong')
        f = open('wrong_v1.txt','a')
        f.write(url +'\n')
        f.close()
#34619
Page = 34619

for page in range(Page):
    if page<32639:
        pass
    else:
        url = r'http://www.66law.cn/question/list_' + str(page+1) + r'_r3.aspx'
        print('****正在处理第%d页' % (page+1))
        GetData(url,random.choice(headers))

print('----end---')
