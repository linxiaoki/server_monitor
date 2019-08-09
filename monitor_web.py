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
import random,hashlib,string

#原url:  http://book.zongheng.com/showchapter/672340.html
#现url:  url="https://m.zongheng.com/h5/ajax/chapter/list"
#        data={'h5':1,'bookId':672340,'pageNum':1,'pageSize':20,'chapterId':0,'asc':1}


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
#'''

path=''

#把每一次print 都写入文件 
def output(str1):
    #txt+=(str1+'\n')
    #添加时间，在某个时间点输出？
    with open(path+'/run_log_test','ab') as f:
        if(not isinstance(str1,str)):
            str1=str(str1)
        str1=str1+'\n'
        f.write(str1.encode('utf-8'))
#print=output


# 获取  请求json需要的参数：随机的Herders,Cookies,代理proxies
def getRandomHeader(isUseProxy=True):
    #随机获取字符串计算MD5值作为ZHID,返回 cookies
    def getRamdomCookies():
        zhid=''.join([random.choice(string.ascii_letters+string.digits) for i in range(20)])
        md5=hashlib.md5()
        md5.update((zhid).encode('utf-8'))
        zhid=md5.hexdigest().upper()
        return {'ZHID':zhid}
    
    ua=UserAgent(verify_ssl=False,use_cache_server=False)
    headers={"User-Agent":ua.chrome,"Referer":"https://m.zongheng.com/h5/chapter/list?bookid=672340"}
    cookies=getRamdomCookies()
    proxies=None
    if isUseProxy==True:
        proxies=proxyip.get_proxyip()
        proxies={"http":proxies,"Connection":"close"}  # keep-alive:false  测试
    return {'headers':headers,'cookies':cookies,'proxies':proxies}


# isuseproxy=True  则随机生成代理  或者 直接接受代理参数 proxies
def get_url(url,isUseProxy=False,proxies=None,cookies=None,headers=None):
    if isUseProxy==True:
        proxies=proxyip.get_proxyip()
        print('init->get_url->proxy:'+proxies)
        proxies={"http":proxies,"Connection":"close"}  # keep-alive:false  测试 
    #proxies={'http':'socks5://'+proxies_someone,'https':'socks5://'+proxies_someone}  # 没试过
    #proxies={'socket5':proxies_someone}
    response=requests.get(url,headers=headers,proxies=proxies,cookies=cookies)
    return response


def init():
    #剑来
    url="https://m.zongheng.com/h5/ajax/chapter/list?h5=1&bookId=672340&pageNum=1&chapterId=0&pageSize=20&asc=1"
    #url='http://book.zongheng.com/showchapter/672340.html'
    #response=get_url(url,isuseproxy=True)  #测试 但是出错不能循环
    kwargs=getRandomHeader(isUseProxy=False)
    response=get_url(url,**kwargs)  #isUseProxy=True
    chaplist=json.loads(response.content.decode('utf-8'))
    chapterName=chaplist['chapterlist']['chapters'][0]['chapterName']
    chapterCount=chaplist['chapterlist']['chapterCount']
    d1={"name":"剑来","chapCount":chapterCount,"lastTitle":chapterName}
    d0={"jianlai":d1}
    with open(path+'/temp.json','w') as f:
        json.dump(d0,f)


# 监测：剑来
def test_jianlai(d1,request_kwargs):
    mail_user=mailpy.Email(['1358109029@qq.com'],'keename@sina.com','MEIYOUSINA')
    #mail_user=mailpy.Email(['1358109029@qq.com','1225517060@qq.com'],'keename@sina.com','MEIYOUSINA')

    url="https://m.zongheng.com/h5/ajax/chapter/list?h5=1&bookId=672340&pageNum=1&chapterId=0&pageSize=20&asc=1"
    response=get_url(url,**request_kwargs)   # keep-alive   close!
    chaplist=json.loads(response.content.decode('utf-8'))
    chapterName=chaplist['chapterlist']['chapters'][0]['chapterName']
    chapterCount=chaplist['chapterlist']['chapterCount']

    if chapterCount > d1["chapCount"] :
        d1["chapCount"]=chapterCount
        d1["lastTitle"]=chapterName
        mail_user.send_Email('剑来更新了',chapterName)
        print('    今天剑来更新:'+chapterName+'('+datetime.now().strftime("%a, %b %d %H:%M")+')')
        return d1
    return None


# 保存笔记到有道云
#def savenote(url):
    #send_Email(title,url,save@note.youdao.com)


def loop_monitor():
    try:
        request_kwargs=getRandomHeader()
        with open(path+'/temp.json','r') as f:
            d_last=json.load(f)
    except Exception as e1:
        print('    loop_monitor->loop->catch error-> getRandomHeader')
        return str(e1)
    while True:
        try:
            print('test jianlai')
            d1=test_jianlai(d_last["jianlai"],request_kwargs)
            if d1:
                d_tmp={"jianlai":d1}   #d_last={d1,d2....}
                d_last=d_tmp
                with open(path+'/temp.json','w') as f:
                    json.dump(d_last,f)
            time.sleep(random.randint(9,15))
        except Exception as e1:
            print('    loop_monitor->loop->catch error->test_jianlai')
            return str(e1)

if __name__=='__main__':
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 centos7相对路径为/root ,需要手动改路径
        path='/opt/git_py/server_monitor'
    
    path=path+'/ini' #配置文件
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.isfile(path+"/temp.json"):
        init()

    print('begin loop:')
    #nowstamp=datetime.now().timestamp()
    mail_error=mailpy.Email(['1358109029@qq.com'],'keename@sina.com','MEIYOUSINA')
    errortimes=0
    print(datetime.now())
    while True:
        #errormsg=loop_monitor_(nowstamp)
        errormsg=loop_monitor()
        print('循环监测时发现错误，重新开始循环')
        if not(errormsg):
            print('    错误次数：'+str(errortimes))
            print('运行结束'.center(20,'-'))
            break
        errortimes+=1
        print('    '+errormsg)
        #url='http://book.zongheng.com/showchapter/672340.html'
        #mail_error.send_Email("monitor_web 运行出错",errormsg)
