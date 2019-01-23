#!/usr/bin/env python3
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart 
import smtplib
import sys
#手机收邮件   一个title会归于一个会话
class Email(object):
    def __init__(self,to_addr,from_addr='kisaname@126.com',pwd='MIMA123'):
        self.from_addr=from_addr
        self.password=pwd
        if(not isinstance(to_addr,list)):
            to_addr=[to_addr]
        self.to_addr=to_addr
        self.msg = MIMEMultipart()
        self.msg['From'] = format_addr('服务器通知 <%s>' % from_addr)
        self.msg['To'] = format_addr('管理员 <%s>' % to_addr)

    def server_start(self):
        pass

    def set_Toaddrs(self,to_addr):
        self.to_addr=to_addr
    def set_Fromaddr(self,from_addr,pwd):
        self.from_addr=from_addr
        self.password=pwd

    #用msg=self.msg  可以不用initMsg
    def initMsg(self):
        self.msg.__init__()
        self.msg = MIMEMultipart()
        self.msg['From'] = format_addr('服务器通知 <%s>' % self.from_addr)
        self.msg['To'] = format_addr('管理员 <%s>' % self.to_addr)

    def send_Email(self,title,txt=''):
        self.msg.attach(MIMEText(txt,'plain','utf-8'))
        self.msg['Subject']=Header(title)
        server=smtplib.SMTP('smtp.126.com',25)   #!!!!!!!!!!!!!!!!!!非固定
        #server.set_debuglevel(1)
        server.login(self.from_addr,self.password)
        server.sendmail(self.from_addr,self.to_addr,self.msg.as_string())
        self.initMsg()  
        server.quit()
        print('complete')

    def send_Fail(self,error_msg): 
        self.initMsg()
        msg=self.msg
        msg.attach(MIMEText(error_msg,'plain','utf-8'))
        self.send_Email('出现错误')
        self.initMsg()
        return

'''
    def send_Test(self,txt=''):  #msg=self.msg    self不更改
        self.msg.attach(MIMEText('绑定self的信息，看出现几次','plain','utf-8'))
        msg=self.msg
        msg.attach(MIMEText('没绑定self的信息','plain','utf-8'))
        msg['Subject']=Header('出现错误')
        server=smtplib.SMTP('smtp.126.com',25)   #!!!!!!!!!!!!!!!!!!非固定
        #server.set_debuglevel(1)
        server.login(self.from_addr,self.password)
        server.sendmail(self.from_addr,self.to_addr,msg.as_string())
        server.quit()
'''

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))

if __name__=='__main__':    
    #em1=Email('kisaname@126.com','MIMA123','kisaname@sina.com') 
    em1=Email('kisaname@sina.com');  #email 添加初始值
    msgtxt='Test for python'
    #msgtxt=sys.stdin.read()
    #em1.send_Test()
    try:
        em1.send_Email('email test',msgtxt)
    except Exception as e:
        em1.send_Fail(str(e))
