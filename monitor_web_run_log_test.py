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

path=''

def output(str1):
    with open(path+'/run_log_test','ab') as f:
        if(not isinstance(str1,str)):
            str1=str(str1)
        str1=str1+'\n'
        f.write(str1.encode('utf-8'))

def get_url(url,isuseproxy=False,proxies=None):
    output('          >>>>get_url->'+url)
    ua=UserAgent(verify_ssl=False,use_cache_server=False)
    headers={"User-Agent":ua.chrome}
    if isuseproxy==True:
        proxies=proxyip.get_proxyip()
    #proxies={'http':'socks5://'+proxies_someone,'https':'socks5://'+proxies_someone}  # 没试过
    #proxies={'socket5':proxies_someone}
    proxies={"http":proxies,"Connection":"close"}  # keep-alive:false  测试 
    output('          >>>>get_url->>>>>request 前')
    response=requests.get(url,headers=headers,proxies=proxies)
    output('          >>>>get_url->>>>>request 后')
    return response


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
    output('init 完成')

# 监测：剑来
def test_jianlai(d1,proxies):
    output('          test_jianlai 开始')
    mail_user=mailpy.Email(['1358109029@qq.com'],'keename@sina.com','MEIYOUSINA')
    #mail_user=mailpy.Email(['1358109029@qq.com','1225517060@qq.com'],'keename@sina.com','MEIYOUSINA')
    url='http://book.zongheng.com/showchapter/672340.html'
    #proxies={"http":proxies}
    #response=requests.get(url,proxies=proxies)
    output('          test_jianlai get_url 前')
    response=get_url(url,proxies=proxies)   # keep-alive   close!
    output('          test_jianlai get_url 后')
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    chapCount=d1["chapCount"]
    #print(chapCount)
    output('          test_jianlai chapCount 后>>>>>'+lastTitle)
    if chapCount < len(chap):
        d1["chapCount"]=len(chap)
        d1["lastTitle"]=lastTitle
        mail_user.send_Email('剑来更新了',lastTitle)
        output('    今天剑来更新:'+lastTitle+'('+datetime.now().strftime("%a, %b %d %H:%M")+')')
        output('          test_jianlai 有更新-end')
        return d1
    output('          test_jianlai 无更新-end')
    return None

def get_jlChapcount(proxies):
    url='http://book.zongheng.com/showchapter/672340.html'
    output('          get_jlChapcount get_url 前')
    response=get_url(url,proxies=proxies)   # keep-alive   close!
    output('          get_jlChapcount get_url 后')
    selector=html.fromstring(response.content)
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]+"  "+str(len(lastTitle))
    output('          get_jlChapcount ------end')
    return lastTitle


def loop_monitor_():
    try:
        output('    loop_monitor_->proxiesip.get 开始loop')
        proxies=proxyip.get_proxyip()
        output('    loop_monitor_->proxiesip.get-> get proxies: <<<'+proxies+'>>>>')
        with open(path+'/temp.json','r') as f:
            d_last=json.load(f)
        output('    loop_monitor_->proxiesip.get-> get proxies->更新 d_last complete')
    except Exception as e1:
        output('    loop_monitor_->proxiesip.get->catch error-> proxy 错误返回')
        return str(e1)
    output('    loop_monitor_->proxiesip.get-> get success Next loop')
    while True:
        try:
            output('    loop_monitor_->loop test_jianlai 前')
            d1=test_jianlai(d_last["jianlai"],proxies)
            output('    loop_monitor_->loop test_jianlai 后')
            if d1:
                d_tmp={"jianlai":d1}   #d_last={d1,d2....}
                d_last=d_tmp
                with open(path+'/temp.json','w') as f:
                    json.dump(d_last,f)
            output('    loop_monitor_->loop test_jianlai 后 休眠前')
            time.sleep(random.randint(15,30))
            output('    loop_monitor_->loop test_jianlai 后 休眠后')
        except Exception as e1:
            output('    loop_monitor->loop->catch error->test_jianlai 错误返回')
            return str(e1)

if __name__=='__main__':
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 centos7相对路径为/root
        path='/opt/git_py/server_monitor'
    if not os.path.isfile(path+"/temp.json"):
        init()

    output('begin loop:')
    #nowstamp=datetime.now().timestamp()
    mail_error=mailpy.Email(['1358109029@qq.com'],'keename@sina.com','MEIYOUSINA')
    errortimes=0
    output(datetime.now())
    while True:
        #errormsg=loop_monitor_(nowstamp)
        output('loop_monitor 前')
        errormsg=loop_monitor_()
        output('loop_monitor done 后')
        if not(errormsg):
            output('    错误次数：'+str(errortimes))
            output('运行结束'.center(20,'-'))
            break
        errortimes+=1
        output('    '+errormsg)
        #url='http://book.zongheng.com/showchapter/672340.html'
        #mail_error.send_Email("monitor_web 运行出错",errormsg)
