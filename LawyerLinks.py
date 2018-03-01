#coding=utf-8
import sys
import time
import random
import requests
import json
import codecs
from lxml import etree

lawyer_links = []
with codecs.open('Answerlist.json','r',encoding='utf-8') as f:
    for each in f.readlines():
        each = json.loads(each,encoding='utf-8')
        if len(each[0]) > 0:
            for each2 in each[0]:
                each2[0]
                lawyer_links.append(each2[0])
                #print(each2[0])

print(len(lawyer_links))
lawyer_links_clear = set(lawyer_links)

data = []
for each in lawyer_links_clear:
    count = lawyer_links.count(each)
    data.append([each,count])
data1 = []
for each in data:
    data1.append(each[1])

num = 0

f = codecs.open('lvshihuifutongji.txt','w',encoding='utf-8')
for each in data:
    content = each[0] + u'*' + str(each[1]) + '\n'
    f.write(content)
f.close()