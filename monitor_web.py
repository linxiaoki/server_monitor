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

def geturl(url,isuseproxy=False):
    ua=UserAgent(verify_ssl=False,use_cache_server=False)
    headers={"User-Agent":ua.chrome}
    proxies=None
    if isuseproxy==True:
        proxies_someone=proxyip.get_proxyip()
        #proxies={'http':'socks5://'+proxies_someone,'https':'socks5://'+proxies_someone}  # 没试过
        #proxies={'socket5':proxies_someone}
        proxies={"http":proxies_someone}
    response=requests.get(url,headers=headers,proxies=proxies)
    return response

def init():
    #剑来
    url='http://book.zongheng.com/showchapter/672340.html'
    response=geturl(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    d1={"name":"剑来","chapCount":len(chap),"lastTitle":lastTitle}
    
    d0={"jianlai":d1}
    with open(path+'/temp.json','w') as f:
        json.dump(d0,f)

# 监测：剑来
def test_jianlai(d1):
    mail_user=mailpy.Email('1358109029@qq.com','keename@sina.com','MEIYOUSINA')
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    chapCount=d1["chapCount"]
    if chapCount !=len(chap):
        d1["chapCount"]=len(chap)
        d1["lastTitle"]=lastTitle
        mail_user.send_Email('剑来更新了',lastTitle)
        print('    今天剑来更新:'+lastTitle+'('+datetime.now().strftime("%a, %b %d %H:%M")+')')
        return d1
    return None


#def savenote(url):
    #send_Email(title,url,save@note.youdao.com)

#监测：汇总
def monitor_web(d_last):
    d1=test_jianlai(d_last["jianlai"])
    #d2=test_other(d_last["other"])
    if d1:
        d_last={"jianlai":d1}   #d_last={d1,d2....}
        return d_last
    return None
 

if __name__=='__main__':
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 centos7相对路径为/root
        path='/opt/git_py/server_monitor'
    if not os.path.isfile(path+"/temp.json"):
        init()

    with open(path+'/temp.json','r') as f:
        d_last=json.load(f)
    print('begin loop:')
    nowstamp=datetime.now().timestamp()
    while True:
        d_tmp=monitor_web(d_last)
        if d_tmp:       #实时更新
            d_last=d_tmp
            with open(path+'/temp.json','w') as f:
                json.dump(d_last,f)
        time.sleep(5)
        if(datetime.now().timestamp()-nowstamp>28800):
            print(datetime.now().strftime('%a, %b %d %H:%M'))
            break
