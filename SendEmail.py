import datetime
import requests
from lxml import etree
import os.path
import time
import logging

# 调用Mailgun发送HTML格式的邮件
# You can see a record of this email in your logs: https://app.mailgun.com/app/logs
# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10,000 emails/month for free.
# 请替换你在Mailgun注册时获取的domain name和API key，以及注册的邮件地址

def send_complex_message(subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/<Your Domain>/messages",
        auth=("api", "<Your API key>"),
        data={"from": "Mailgun Sandbox <postmaster@Your Domain>",
              "to": "<Your registered recipient>",
              "cc": "<Your registered recipient>",
              "subject": subject,
              "text": "Testing some Mailgun awesomness!",
              "html": text})

# 获取东方网新闻链接，并访问
mydate = datetime.datetime.now().strftime("%Y%m%d")
url = "http://www.eastday.com/eastday/shouye/node670813/n847507/{0}/index_T1722.html".format(mydate)
r = requests.get(url)
text_to_send = ''

# 设置logging
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
        news_title = '//*[@id="maincnt"]/div[{0}]/div[3]/h2/a/text()'.format(j+1)   # 新闻标题
        news_link = '//*[@id="maincnt"]/div[{0}]/div[3]/h2/a/@href'.format(j+1)     # 新闻详情的链接。注：某些新闻没有详情链接，所以要进行判断
        if ''.join(s.xpath(news_link)) != '':
            news_to_add = ''.join(s.xpath(news_title)) + ' ' + '<a href="' + ''.join(s.xpath(news_link)) + '">详细</a>'
        else:
            news_to_add = ''.join(s.xpath(news_title))
        list_of_title.append(news_to_add)
        image = '//*[@id="maincnt"]/div[{0}]/div[3]/div[@class="cnt-inner"]/div[@class="left pic1 mypic"]/img/@src'.format(j+1)
        list_of_images.append(''.join(s.xpath(image)))


    # 天气预报
    text_to_send += '<html><head><title>直播上海</title></head><body>'
    text_to_send += ''.join(s.xpath('//*[@id="timebar"]/p[1]/text()'))
    text_to_send += '<br><br>'


    for i in range(total_num):
        text_to_send += ''.join(list_of_time[i])  # 新闻发布时间
        text_to_send += '<br>'
        text_to_send += ' ' + '<strong>' + list_of_title[i] + '</strong>' # 新闻标题及链接        
        text_to_send += '<br><br>'
        if list_of_images[i] != '':
            text_to_send += '<img src="' + list_of_images[i] + '" resize height="123" width="200">'  # 新闻配图。注：某些新闻没有详情配图，所以要进行判断
            text_to_send += '<br><br>'
        text_to_send += ''.join(list_of_body[i])   #新闻简介
        text_to_send += '<br><br>'

    text_to_send += '</body></html>'

except Exception as exc:
    logger.error('unable to connect. ', exc_info=True)


subject = '直播上海 ' + ''.join(list_of_time[-1]) + ' --' + ''.join(list_of_time[0])[6:]  # 标题格式为：直播上海 年-月-日 起始时间 -- 结束时间 

send_complex_message(subject, text_to_send)  # 发邮件，通过计划任务，可实现每隔一定时间自动发邮件


