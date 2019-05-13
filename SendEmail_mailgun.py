import pandas as pd
import datetime
import requests
from lxml import etree
import os.path
import time
import logging
import sys

# def send_simple_message
# it is for sending plain-text email messages
'''
def send_simple_message(subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxbc5425db5f0e46be99aa28b2746769d1.mailgun.org/messages",
        auth=("api", "a97454c453feb1d0f9bdba318381c3e7-47317c98-3ea1f3d8"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxbc5425db5f0e46be99aa28b2746769d1.mailgun.org>",
              "to": "tairan <2730891246@qq.com>",
              "subject": subject,
              "text": text})
'''


# You can see a record of this email in your logs: https://app.mailgun.com/app/logs
# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10,000 emails/month for free.

# 快速上手 requests 库 http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
# Xpath教程
# https://zhuanlan.zhihu.com/p/25572729
# https://cuiqingcai.com/2621.html
# http://www.w3school.com.cn/xpath/

def send_complex_message(subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxbc5425db5f0e46be99aa28b2746769d1.mailgun.org/messages",
        auth=("api", "a97454c453feb1d0f9bdba318381c3e7-47317c98-3ea1f3d8"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxbc5425db5f0e46be99aa28b2746769d1.mailgun.org>",
              "to": "2730891246@qq.com",
              "subject": subject,
              "text": "Testing some Mailgun awesomness!",
              "html": text})

mydate = datetime.datetime.now().strftime("%Y%m%d")
url = "http://www.eastday.com/eastday/shouye/node670813/n847507/{0}/index_T1722.html".format(mydate)
r = requests.get(url)
text_to_send = ''

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/GetThemAll/Logs/'
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

try:
    r.raise_for_status()
    r.encoding = 'utf-8'
    s = etree.HTML(r.text)

    list_of_title = []
    list_of_images = []
    list_of_time = s.xpath('//p[@class="gray14"]/text()')
    list_of_body = s.xpath('//div[@class="cnt-inner"]/div/a/text()')

    total_num = len(list_of_time)

    for j in range(total_num):
        news_title = '//*[@id="maincnt"]/div[{0}]/div[3]/h2/a/text()'.format(j+1)
        news_link = '//*[@id="maincnt"]/div[{0}]/div[3]/h2/a/@href'.format(j+1)
        if ''.join(s.xpath(news_link)) != '':
            news_to_add = ''.join(s.xpath(news_title)) + ' ' + '<a href="' + ''.join(s.xpath(news_link)) + '">详细</a>'
        else:
            news_to_add = ''.join(s.xpath(news_title))
        list_of_title.append(news_to_add)
        image = '//*[@id="maincnt"]/div[{0}]/div[3]/div[@class="cnt-inner"]/div[@class="left pic1 mypic"]/img/@src'.format(j+1)
        list_of_images.append(''.join(s.xpath(image)))


    # weather
    text_to_send += '<html><head><title>直播上海</title></head><body>'
    text_to_send += ''.join(s.xpath('//*[@id="timebar"]/p[1]/text()'))
    text_to_send += '<br><br>'


    for i in range(total_num):
        text_to_send += ''.join(list_of_time[i])
        text_to_send += '<br>'
        text_to_send += ' ' + '<strong>' + list_of_title[i] + '</strong>'
        #text_to_send += ''.join(s.xpath('//*[@id="maincnt"]/div[{0}]/div[3]/h2/a/@href'.format(i+1)))
        text_to_send += '<br><br>'
        if list_of_images[i] != '':
            text_to_send += '<img src="' + list_of_images[i] + '" resize height="123" width="200">'
            text_to_send += '<br><br>'
        text_to_send += ''.join(list_of_body[i])
        text_to_send += '<br><br>'

    text_to_send += '</body></html>'

    subject = '直播上海 ' + ''.join(list_of_time[-1]) + ' --' + ''.join(list_of_time[0])[6:]
    # send_simple_message(subject,text_to_send)
    # print(text_to_send)
    send_complex_message(subject, text_to_send)

except Exception as exc:
    send_complex_message('东方网错误','unable to connect. {}'.format(exc))

sys.exit()

# For Testing....
# print(subject)
# print(text_to_send)

