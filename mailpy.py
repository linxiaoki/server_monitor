#!/usr/bin/env python3 
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart 
import smtplib
import sys
import proxyip
import socks
import socket

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
        print(self.from_addr)
        server=smtplib.SMTP_SSL('smtp.'+self.from_addr.split('@')[1],465)
        #server=smtplib.SMTP('smtp.'+self.from_addr.split('@')[1],587,timeout=120)
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

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))

if __name__=='__main__':
    #测试用   
    em1=Email('1358109029@qq.com');  #email 添加初始值
    msgtxt='剑来章节更新了，第四百七十五章'
    #msgtxt=sys.stdin.read()
    #em1.send_Test()
    _socket=socket.socket
    try:
        proxyhost,proxyip=proxyip.get_proxyip(proxytype='socket5').split(':')
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5,proxyhost,int(proxyip))
        #socks.wrapmodule(smtplib)   #局部更新代理
        socket.socket=socks.socksocket
        print(proxyhost+':'+proxyip)
        em1.send_Email('服务器通知剑来更新了',msgtxt)
    except Exception as e:
        try:
            em1.send_Fail(str(e))
        except Exception as e2:
            socket.socket=_socket
            em1=Email('1358109029@qq.com','keename@sina.com','MEIYOUSINA')
            em1.send_Fail("使用代理发送邮件错误")
