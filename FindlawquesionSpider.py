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


def GetQuestionIndexlist(url,headers,proxies='*'):
    #try:
    if proxies == '*':
        html = requests.get(url,headers=headers).content.decode('utf-8','ignore')
    else:
        try:
            html = requests.get(url,headers=headers,proxies=proxies).content.decode('utf-8','ignore')
        except:
            html = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')
    html = etree.HTML(html)

    yzm = html.xpath('//p[@class="input"]/img[@class="yzm-pic"]')
    print(yzm)
    if len(yzm) == 1:
        print(url)
        a = raw_input('请输入验证码')
    #获取quesion数据
    category = html.xpath('//ul[@class="result-list"]/li/div/span[@class="rli-item item-classify"]/text()')
    title = html.xpath('//ul[@class="result-list"]/li/div/a/@title')
    question_link = html.xpath('//ul[@class="result-list"]/li/div/a/@href')
    ask_number = html.xpath('//ul[@class="result-list"]/li/div/span[@class="rli-item item-num"]/text()')
    create_date = html.xpath('//ul[@class="result-list"]/li/div/span[@class="rli-item time"]/text()')

    if create_date != len(title):
        create = []
        for each in range(len(title)):
            create_date.append(' ')
    question_list = zip(title,category,question_link,ask_number,create_date)
    return(question_list)

    #except:
        #print('******页面信息获取失败 链接：%s'% url)
        #WriteDate(url + '\n','FailedPageLinklist.txt')


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
        WriteDate(url + '\n', 'FailedAnswerLinklist.txt')


def GetLawyer(url,headers):
    #try:
        html = requests.get(url, headers=headers).content.decode('gb2312', 'ignore')
        html = etree.HTML(html)

        yzm = html.xpath('//p[@class="input"]/img[@class="yzm-pic"]')
        if len(yzm) == 1:
            print(url)
            a = raw_input('请输入验证码')
            print(a)
        #判断律师页面类型（律师页面有三个不同的样式），根据不同的样式使用xpath规则
        type_value = 6
        for each in range(6):
            if len(html.xpath('//div[@class="left"]/div[@class="row"]/div[@class="desc-box"]/h4/text()')) == 1:
                type_value = 0
                break
            if len(html.xpath('//div[@class="aside-bd aside-contact"]/p[1]/text()')) == 1:
                type_value = 1
                break
            if len(html.xpath('//div[@class="col-w-8"]/div[@class="common-container"][1]')) == 1:
                type_value = 2
                break
            if len(html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]/div[@class="inlawyer"][1]')) == 1:
                type_value = 3
                break
            if len(html.xpath('//div[@class="left_top_one"]/h1/span/text()')) == 1:
                type_value = 4
                break
            if len(html.xpath('//div[@class="title"]/a[@href="/tdls.html"]')) == 1:
                type_value = 5
                break

        #type0获取律师信息 http://lawyershazi.findlaw.cn/lawyer/onlinelawyer.html
        if type_value == 0:
            print(url)
            lawyer_name = u'律师姓名：' + html.xpath('//div[@class="left"]/div[@class="row"]/div[@class="desc-box"]'
                                                '/h4/text()')[0]
            mobile_phone = u'业务手机：' + html.xpath('//div[@class="left"]/div[@class="row"]/div[@class="desc-box"]'
                                                 '/p[2]/text()')[0]
            law_office = u'执业机构：' + html.xpath('//div[@class="left"]/div[@class="row row2"]/p[2]/text()')[0]
            law_adress = u'联系地址：' + \
                         html.xpath('//div[@class="left"]/div[@class="row"]/div[@class="desc-box"]/p[1]/text()')[0] + \
                         u'##' + html.xpath('//div[@class="left"]/div[@class="row row2"]/p[3]/text()')[0]
            lawyer_license = u'执业证号：' + html.xpath('//div[@class="left"]/div[@class="row row2"]/p[1]/text()')[0]
            lawyer_info = [type_value,[type_value, lawyer_name, mobile_phone, law_office, law_adress, lawyer_license]]
            return (lawyer_info)

        #type1获取律师信息 http://guoqian.findlaw.cn/lawyer/onlinelawyer.html
        if type_value == 1:
            lawyer_name = u'律师姓名：' + html.xpath('//div[@class="aside-bd aside-contact"]/p[1]/text()')[0]
            mobile_phone = html.xpath('//div[@class="aside-bd aside-contact"]/p[4]/text()')[0]
            email = html.xpath('//div[@class="aside-bd aside-contact"]/p[5]/text()')[0]
            law_office = html.xpath('//div[@class="aside-bd aside-contact"]/p[6]/text()')[0]
            law_adress = html.xpath('//div[@class="aside-bd aside-contact"]/p[7]/text()')[0]
            lawyer_license = html.xpath('//div[@class="aside-bd aside-contact"]/p[2]/text()')[0]
            office_phone = html.xpath('//div[@class="aside-bd aside-contact"]/p[3]/text()')[0]

            lawyer_info = [type_value,[type_value,lawyer_name,mobile_phone,email,law_office,
                                       law_adress,lawyer_license,office_phone]]
            return(lawyer_info)

        #type2获取律师信息 http://wanggenyu.findlaw.cn/lawyer/onlinelawyer.html
        if type_value == 2:
            lawyer_name = html.xpath('//h2[@class="lawyer_name"]/text()')[0]
            mobile_phone = html.xpath('//div[@class="col-w-8"]/div[@class="common-container"][1]/'
                                      'div[@class="profile_text"]/p[1]/text()')[0]
            email = html.xpath('//div[@class="col-w-8"]/div[@class="common-container"][1]/'
                                      'div[@class="profile_text"]/p[2]/text()')[0]
            law_office = html.xpath('//div[@class="col-w-8"]/div[@class="common-container"][1]/'
                                  'div[@class="profile_text"]/p[3]/text()')[0]
            law_adress = html.xpath('//div[@class="col-w-8"]/div[@class="common-container"][1]/'
                                'div[@class="profile_text"]/p[4]/text()')[0]
            lawyer_license_info = html.xpath('//div[@class="col-w-8"]/div[@class="common-container"][2]'
                                             '/div[@class="profile_auth"]/div[@class="p_table"]'
                                             '/div[@class="table_item"]/span/text()')
            lawyer_info = [type_value,[type_value,lawyer_name,mobile_phone,email,law_office,law_adress]
                                       + lawyer_license_info]
            return(lawyer_info)

        # type3获取律师信息 http://jz_baixuelawyer.findlaw.cn/lawyer/onlinelawyer.html
        if type_value == 3:
            lawyer_name = u'律师姓名：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                                '/div[@class="inlawyer"][1]/text()[2]')[0]
            mobile_phone = u'业务手机：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                                 '/div[@class="inlawyer"][1]/text()[8]')[0]
            law_office = u'所属律所：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                               '/div[@class="inlawyer"][1]/text()[11]')[0]
            try:
                law_adress = u'所属地区：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                               '/div[@class="inlawyer"][1]/text()[13]')[0]
            except:
                law_adress = u'所属地区：' + u'未知'
            office_phone = u'办公电话：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                      '/div[@class="inlawyer"][1]/text()[6]')[0]
            lawyer_license = u'执业证号：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                        '/div[@class="inlawyer"][1]/text()[4]')[0]
            lawyer_info = [type_value,[type_value, lawyer_name, mobile_phone, law_office, law_adress,
                                       lawyer_license,office_phone]]
            return (lawyer_info)

        # type4获取律师信息 http://jz_baixuelawyer.findlaw.cn/lawyer/onlinelawyer.html
        if type_value == 4:
            lawyer_name = u'律师姓名：' + html.xpath('//div[@class="left_top_one"]/h1/span/text()')[0]
            mobile_phone = html.xpath('//div[@class="left_top_one"]/text()[2]')[0]
            #email = u'电子邮箱：' + html.xpath('//div[@class="main"]/table[@class="all_table"]/tbody/tr[9]/td[2]/text()')[0]
            law_office = html.xpath('//div[@class="left_top_two cl"]/text()[3]')[0]
            law_adress =  html.xpath('//div[@class="left_top_one"]/text()[1]')[0]
            office_phone = html.xpath('//div[@class="left_top_two cl"]/text()[4]')[0]
            lawyer_license = html.xpath('//div[@class="left_top_two cl"]/text()[2]')[0]
            lawyer_info = [type_value,[type_value, lawyer_name, mobile_phone, law_office, law_adress,
                                       lawyer_license,office_phone]]
            return (lawyer_info)

        # type5获取律师信息 http://zhangxiuqing.findlaw.cn/
        if type_value == 5:
            print(url)
            lawyer_name = html.xpath('//div[@class="right"]/p/a/span/text()')
            lawyer_num = len(lawyer_name)
            mobile_phone = []
            for each in range(lawyer_num):
                mobile_phone.append(html.xpath('//div[@class="right"]/p/span/text()')[each*3 + 1])
            lawyer_license = []
            for each in range(lawyer_num):
                lawyer_license.append(html.xpath('//div[@class="right"]/p/span/text()')[each*3 + 2])
            lawyer_linklist = html.xpath('//div[@class="right"]/p/a[@class="name"]/@href')

            tpye_values = []
            for each in lawyer_name:
                tpye_values.append(type_value)
            lawyers = zip(tpye_values,lawyer_name,mobile_phone,lawyer_license,lawyer_linklist)
            lawyer_info = [type_value] + lawyers
            return(lawyer_info)
        print('律师信息获取失败 %s'%url)
        return([])
'''
    except:
        print('******页面信息获取失败 链接：%s' % url)
        WriteDate(url, 'FailedLawyerlist.txt')
'''


def WriteDate(content,filename):
    with codecs.open(filename,'a+',encoding = "utf-8") as f:
        f.write(content)

def ReadDate(filename):
    result = []
    with codecs.open(filename,'r',encoding = "utf-8") as f:
        for line in f.readlines():
            result.append(line)
    return(result)

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
url_proxies = 'http://china.findlaw.cn/ask/question_43355287.html'
def main():
    """
    url2 = '/lawyer/onlinelawyer.html'
    Page = 3875
    TIME = [1,2.6,3,0.5,10.8,8.2,6.9]
    for i in range(Page):
        if i <2743:
            continue

        url = 'http://china.findlaw.cn/ask/d201801_t00_page' + str(i+1) +'/'
        print('****正在获取第%d页question数据******'%(i+1))
        question_list = GetQuestionIndexlist(url,random.choice(HEADERS))
        print('***获取到%d个咨询××××' % len(question_list))
        question_list_data = json.dumps(question_list,ensure_ascii = False) + u'\n'
        WriteDate(question_list_data,'Question_list_v1.0.txt')
        time.sleep(random.choice(TIME))

   """
num = 0
TIME = [5.8,2.7,3,1.5,3.9,6.1,2.6,2.9,3.9]
"""
question_list = ReadDate('Question_list_v1.0.txt')
question_list = set(question_list)

for each in question_list:
    each = json.loads(each,encoding = 'utf-8')
    for each2 in each:
        if len(each2) ==5:
            question_links.append(each2[2])
content = json.dumps(question_links,ensure_ascii = False)
WriteDate(content,'Qestion_link_listv3.0.json')
"""

with codecs.open('Qestion_link_listv3.0.json','r',encoding = 'utf-8') as f:
    question_links = f.read()
question_links = json.loads(question_links)

num2 = len(question_links)
count = 0
BEGINNUM = 7848
ENDNUM = num2
url_proxies = 'https://www.kuaidaili.com/free/intr/1/'
proxies_clear = []
#proxies_clear = GetProxies(url_proxies,random.choice(HEADERS))
proxies_clear = proxies_clear +  ['*','*','*']
print(proxies_clear)
for each in question_links:
    count += 1
    print(count)
    if count > BEGINNUM and count < ENDNUM:
        print('***正在获取咨询回复***')
        print(each)
        answer_list = GetAnswers(each,random.choice(HEADERS),random.choice(proxies_clear))
        content = json.dumps(answer_list,ensure_ascii=False) + '\n'
        WriteDate(content,'Answerlist_v3.1.json')
        num += 1
        percent = float(count)/num2*100
        print('已处理%d条数据，进度: %d' % (num,percent))
        time.sleep(random.choice(TIME))
        time.sleep(0.2)

"""
        question_links = []
        for each in question_list:
            if each[3] == u'0个':
                break
            question_links.append(each[2])

        lawyer_urllist = []
        for each in  question_links:
            if not(each is None):
                print('****正在获取律师回复信息*****')
                lawyer_url = GetAnswers(each,random.choice(HEADERS))
                lawyer_url_data = json.dumps(lawyer_url,ensure_ascii = False) + u'\n'
                WriteDate(lawyer_url_data,'QuestionsAndAnsers.txt')
                time.sleep(random.choice(TIME))
                try:
                    lawyer_urllist.append(lawyer_url[0][0][1])
                    print('****success****')
                except:
                    lawyer_url = json.dumps(lawyer_url,ensure_ascii = False)
                    print('something wrong' + lawyer_url)
        lawyer_urllist = set(lawyer_urllist)

        lawyers = []
        for each in lawyer_urllist:
            print('*****正在获取律师信息******')
            lawyer = GetLawyer(each + url2,random.choice(HEADERS))
            time.sleep(random.choice(TIME))
            lawyers.append(lawyer)
            content = json.dumps(lawyer,ensure_ascii=False) + '\n'
            WriteDate(content,'Lawyers_v1.0.txt')
            print('*****成功获取律师信息******')
"""
if __name__ == "__main__":
    main()