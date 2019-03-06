#!/usr/bin/env python3 
import requests
from lxml import html
import json
import os
import time
from fake_useragent import UserAgent
import mailpy
import proxyip
from datetime import datetime
import random

'''  
class Jianlai(object):
    def __init__(self,name,chapCount):
        self.name=name
        self.chapCount=chapCount
def Jianlai2dict(obj):
    return {
        'name': obj.name,
        'chapCount': obj.chapCount
    }
'''

path=''
# isuseproxy=True  则随机生成代理
def get_url(url,isuseproxy=False,proxies=None):
    ua=UserAgent(verify_ssl=False,use_cache_server=False)
    headers={"User-Agent":ua.chrome}
    if isuseproxy==True:
        proxies=proxyip.get_proxyip()
    #proxies={'http':'socks5://'+proxies_someone,'https':'socks5://'+proxies_someone}  # 没试过
    #proxies={'socket5':proxies_someone}
    proxies={"http":proxies,"Connection":"close"}  # keep-alive:false  测试 
    response=requests.get(url,headers=headers,proxies=proxies)
    return response

def output1(prstr):
    time1=('     '+datetime.now().strftime('%a, %b %d %H:%M'))
    with open('/opt/git_py/server_monitor/result.txt','a') as f:
        f.write(prstr+time1+'\n')

def init():
    #剑来
    url='http://book.zongheng.com/showchapter/672340.html'
    response=get_url(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    d1={"name":"剑来","chapCount":len(chap),"lastTitle":lastTitle}
    d0={"jianlai":d1}
    with open(path+'/temp.json','w') as f:
        json.dump(d0,f)

# 监测：剑来
def test_jianlai(d1,proxies):
    mail_user=mailpy.Email('1358109029@qq.com','keename@sina.com','MEIYOUSINA')
    url='http://book.zongheng.com/showchapter/672340.html'
    #proxies={"http":proxies}
    #response=requests.get(url,proxies=proxies)
    response=get_url(url,proxies=proxies)   # keep-alive   close!
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    chapCount=d1["chapCount"]
    if chapCount < len(chap):
        d1["chapCount"]=len(chap)
        d1["lastTitle"]=lastTitle
        mail_user.send_Email('剑来更新了',lastTitle)
        output1('    今天剑来更新:'+lastTitle+'('+datetime.now().strftime("%a, %b %d %H:%M")+')')
        return d1
    return None

#def savenote(url):
    #send_Email(title,url,save@note.youdao.com)

# Loop
def loop_monitor(nowstamp):
    output1('    begin loop_monitor')
    proxies=proxyip.get_proxyip()
    output1('    '+proxies)
    with open(path+'/temp.json','r') as f:
        d_last=json.load(f)
    while True:
        try:
            if(datetime.now().timestamp()-nowstamp>28000):
                output1(datetime.now().strftime('%a, %b %d %H:%M'))
                return None
            deltime=(datetime.now().timestamp()-nowstamp)%3600
            if(deltime<16):
                output1("         我在运行中哦")
            output1('       begin test_jianlai')
            d1=test_jianlai(d_last["jianlai"],proxies)
            if d1:
                d_tmp={"jianlai":d1}   #d_last={d1,d2....}
                d_last=d_tmp
                with open(path+'/temp.json','w') as f:
                    json.dump(d_last,f)
            output1('        time.sleep')
            time.sleep(random.randint(9,15))
        except Exception as e1:
            output1('       loop_monitor->loop->catch error')
            return str(e1)

if __name__=='__main__':
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 centos7相对路径为/root
        path='/opt/git_py/server_monitor'
    if not os.path.isfile(path+"/temp.json"):
        init()

    output1('begin loop:')
    nowstamp=datetime.now().timestamp()
    mail_error=mailpy.Email('1358109029@qq.com','keename@sina.com','MEIYOUSINA')
    errortimes=0
    while True:
        errormsg=loop_monitor(nowstamp)
        output1('loop_monitor done')
        if not(errormsg):
            output1('    错误次数：'+str(errortimes))
            output1('运行结束'.center(20,'-'))
            break
        errortimes+=1
        output1('    '+errormsg)
        #url='http://book.zongheng.com/showchapter/672340.html'
        #mail_error.send_Email("monitor_web 运行出错",errormsg)
