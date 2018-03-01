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

def GetAnswers(url,headers,proxies='*'):

    try:
        if proxies == '*':
            html = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')
        else:
            try:
                html = requests.get(url, headers=headers, proxies=proxies).content.decode('utf-8', 'ignore')
            except:
                html = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')
        html = etree.HTML(html)

        yzm = html.xpath('//p[@class="input"]/img[@class="yzm-pic"]')
        if len(yzm) == 1:
            print(url)
            a = raw_input('请输入验证码')
            print(a)
        #获取律师信息
        question_detail = html.xpath('//p[@class="question-text"]/text()')
        question_create_date = html.xpath('//span[@class="tip-item"][2]/text()')
        adress = html.xpath('//span[@class="tip-item"][3]/text()')
        category = html.xpath('//span[@class="tip-item"][4]/text()')
        answer = html.xpath('//div[@class="lawyer-answer"]/div[@class="answer-main"]'
                            '/div[@class="answer-text"]/text()[1]')
        lawyer = html.xpath('//div[@class="lawyer-answe r"]/div[@class="lawyer-info"]/div[@class="info"]'
                            '/p/a[@class="info-name-link"]/text()')
        lawyer_link = html.xpath('//div[@class="lawyer-answer"]/div[@class="lawyer-info"]/div[@class="info"]'
                                 '/p/a[@class="info-name-link"]/@href')
        answers = zip(lawyer_link,answer)
        question = zip([url],question_detail,question_create_date,adress,category)
        result = [answers,question]
        return(result)
    except:
        print('******页面信息获取失败 链接：%s' % url)
        #WriteDate(url + '\n', 'FailedAnswerLinklist.txt')

url = 'http://china.findlaw.cn/ask/question_42935646.html'
headers = random.choice(HEADERS)
proxies = {'http': 'http://202.109.237.35:80'}
print(GetAnswers(url,headers,proxies))