import datetime
import requests
from lxml import etree
import time
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# 发邮件的函数
def send_message_qq(title,content):
    mail_host = 'smtp.qq.com'  
    mail_user = '2730891246@qq.com'  
    mail_pass = 'wjfevevlekofdefb'   
    sender = '2730891246@qq.com'  
    receivers = ['tahuan@microsoft.com','taylorw@126.com']      
    message = MIMEMultipart()        
    message['Subject'] = title
    message['From'] = sender 
    message['To'] = receivers[0]    
    part1 = MIMEText(content,'html','utf-8')
    message.attach(part1)    
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)            
        smtpObj.login(mail_user,mail_pass) 
        smtpObj.sendmail(sender,receivers,message.as_string()) 
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误  

# 爬取新闻资料
mydate = datetime.datetime.now().strftime("%Y%m%d")
url = "http://www.eastday.com/eastday/shouye/node670813/n847507/{0}/index_T1722.html".format(mydate)
r = requests.get(url)
text_to_send = ''

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
except Exception as exc:
    text_to_send = str(exc)
    subject = '东方网错误'

if __name__ == '__main__':
    send_message_qq(subject,text_to_send) 
 