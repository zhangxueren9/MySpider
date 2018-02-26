#coding=utf-8
import sys
import time
import random
import requests
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

def GetQuestionIndexlist(url,headers):
    try:
        html = requests.get(url,headers=headers).content.decode('utf-8','ignore')
        html = etree.HTML(html)

        yzm = html.xpath('//p[@class="input"]/img[@class="yzm-pic"]')
        if len(yzm) == 1:
            print(url)
            a = input('请输入验证码')
        #获取quesion数据
        category = html.xpath('//ul[@class="result-list"]/li/div/span[@class="rli-item item-classify"]/text()')
        title = html.xpath('//ul[@class="result-list"]/li/div/a/@title')
        question_link = html.xpath('//ul[@class="result-list"]/li/div/a/@href')
        ask_number = html.xpath('//ul[@class="result-list"]/li/div/span[@class="rli-item item-num"]/text()')
        create_date = html.xpath('//ul[@class="result-list"]/li/div/span[@class="rli-item time"]/text()')

        #反反爬虫策略,如果连续多个页面都没有获取到数据，说明网站采取了反爬虫策略，输入验证码后继续


        question_list = zip(title,category,question_link,ask_number,create_date)
        print(question_list)
        return(question_list)

    except:
        print('******页面信息获取失败 链接：%s'% url)
        WriteDate(url + '\n','FailedPageLinklist.txt')


def GetAnswers(url,headers):

    try:
        html = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')
        html = etree.HTML(html)

        yzm = html.xpath('//p[@class="input"]/img[@class="yzm-pic"]')
        if len(yzm) == 1:
            print(url)
            a = input('请输入验证码')
        #获取律师信息
        question_detail = html.xpath('//p[@class="question-text"]/text()')
        question_create_date = html.xpath('//span[@class="tip-item"][2]/text()')
        adress = html.xpath('//span[@class="tip-item"][3]/text()')
        category = html.xpath('//span[@class="tip-item"][4]/text()')
        answer = html.xpath('//div[@class="lawyer-answer"]/div[@class="answer-main"]'
                            '/div[@class="answer-text"]/text()[1]')
        lawyer = html.xpath('//div[@class="lawyer-answer"]/div[@class="lawyer-info"]/div[@class="info"]'
                            '/p/a[@class="info-name-link"]/text()')
        lawyer_link = html.xpath('//div[@class="lawyer-answer"]/div[@class="lawyer-info"]/div[@class="info"]'
                                 '/p/a[@class="info-name-link"]/@href')


        answers = zip(lawyer,lawyer_link,answer)
        question = zip([url],question_detail,question_create_date,adress,category)
        result = [answers,question]
        return(result)
    except:
        print('******页面信息获取失败 链接：%s' % url)
        WriteDate(url, 'FailedAnswerLinklist.txt')


def GetLawyer(url,headers):
    #try:
        html = requests.get(url, headers=headers).content.decode('gb2312', 'ignore')
        html = etree.HTML(html)

        yzm = html.xpath('//p[@class="input"]/img[@class="yzm-pic"]')
        if len(yzm) == 1:
            print(url)
            a = input('请输入验证码')
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
            lawyer_info = [type_value, lawyer_name, mobile_phone, law_office, law_adress, lawyer_license]
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

            lawyer_info = [type_value,lawyer_name,mobile_phone,email,law_office,law_adress,lawyer_license,office_phone]
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
            lawyer_info = [type_value,lawyer_name,mobile_phone,email,law_office,law_adress] + lawyer_license_info
            return(lawyer_info)

        # type3获取律师信息 http://jz_baixuelawyer.findlaw.cn/lawyer/onlinelawyer.html
        if type_value == 3:
            lawyer_name = u'律师姓名：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                                '/div[@class="inlawyer"][1]/text()[2]')[0]
            mobile_phone = u'业务手机：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                                 '/div[@class="inlawyer"][1]/text()[8]')[0]
            law_office = u'所属律所：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                               '/div[@class="inlawyer"][1]/text()[11]')[0]
            law_adress = u'所属地区：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                               '/div[@class="inlawyer"][1]/text()[13]')[0]
            office_phone = u'办公电话：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                      '/div[@class="inlawyer"][1]/text()[6]')[0]
            lawyer_license = u'执业证号：' + html.xpath('//div[@class="in_info_rg"]/div[@class="conts"]'
                                        '/div[@class="inlawyer"][1]/text()[4]')[0]
            lawyer_info = [type_value, lawyer_name, mobile_phone, law_office, law_adress, lawyer_license,office_phone]
            return (lawyer_info)

        # type4获取律师信息 http://jz_baixuelawyer.findlaw.cn/lawyer/onlinelawyer.html
        if type_value == 4:
            lawyer_name = u'律师姓名：' + html.xpath('//div[@class="left_top_one"]/h1/span/text()')[0]
            mobile_phone = u'业务手机：' + html.xpath('//div[@class="left_top_one"]/text()[2]')[0]
            #email = u'电子邮箱：' + html.xpath('//div[@class="main"]/table[@class="all_table"]/tbody/tr[9]/td[2]/text()')[0]
            law_office = html.xpath('//div[@class="left_top_two cl"]/text()[3]')[0]
            law_adress = u'所属地区：' + html.xpath('//div[@class="left_top_one"]/text()[1]')[0]
            office_phone = html.xpath('//div[@class="left_top_two cl"]/text()[4]')[0]
            lawyer_license =  html.xpath('//div[@class="left_top_two cl"]/text()[2]')[0]
            lawyer_info = [type_value, lawyer_name, mobile_phone, law_office, law_adress, lawyer_license,office_phone]
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
    with open(filename,'a+') as f:
        f.write(content)

def main():

    url = 'http://china.findlaw.cn/ask/d201801_t00_page40/'
    url2 = '/lawyer/onlinelawyer.html'
    question_list = GetQuestionIndexlist(url,random.choice(HEADERS))
    question_links = []
    for each in question_list:
        if each[3] == u'0个':
            break
        question_links.append(each[2])
    print(len(question_links))

    lawyer_urllist = []
    for each in  question_links:
        if not(each is None):
            lawyer_url = GetAnswers(each,random.choice(HEADERS))
            try:
                lawyer_urllist.append(lawyer_url[0][0][1])
            except:
                print(lawyer_url)

    print(len(lawyer_urllist))

    for each in lawyer_urllist:
        lawyer = GetLawyer(each + url2,random.choice(HEADERS))
        for m in lawyer:
            print(m)


num = 0
if __name__ == "__main__":
    main()