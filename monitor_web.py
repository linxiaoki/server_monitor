import requests
from lxml import html
import json
import os
import time
from fake_useragent import UserAgent
import mailpy
import proxyip
from datetime import datetime,timedelta
import re

'''  0
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


#使用随机代理   ！！！未  若代理过期 
def use_proxy():
    ua = UserAgent(verify_ssl=False,use_cache_server=False)
    headers = {"User-Agent": ua.chrome}  #ua.random
    proxies_someone=proxyip.get_proxyip()
    #proxies={'http':'socks5://'+proxies_someone,'https':'socks5://'+proxies_someone}  # 没试过
    #proxies={'http':proxies_someone}
    proxies={"socket5":proxies_someone}
    url='https://mp.weixin.qq.com/s?timestamp=1550479045&src=3&ver=1&signature=S6Ck7Jdj-dGNBZ0ownV8JSDeqSbTJQY2NPdzwQPsxvllLYfc0Vd3hf-pPFNqHE4FrMRmEmWAZXWr3KySUXkmKycBz4VsoZ31fWa0cXkok5*Z9ozayE5DJb7i9EvE27ellav8LrC1nUKc90qsvSGlN**BCeDpWFrvbS1W1fQ466Y='
    response=requests.get(url,headers=headers)    # proxies=proxies
    mail_Test=mailpy.Email('kisaname@126.com')
    mail_Test.send_Email('笔记收藏',response.content)


def init_wechatsougou():
    url='https://weixin.sogou.com/weixin?query=%E5%88%98%E5%A4%87%E6%95%99%E6%8E%88'
    response=geturl(url)
    selector=html.fromstring(response.content)
    #url1  公众号前10篇网页  //*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a
    url1=selector.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/@href')[0]
    lastTitle=selector.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[2]/dd/a/text()')[0]
    d2={"name":"公众号刘备教授","lastTitle":lastTitle}
    print(url1)
    print(lastTitle)
    return d2


#时间判断
def timestamp2time(time1stamp):
    time1=datetime.fromtimestamp(time1stamp)
    time2=time1 + timedelta(hours=5.9)
    print(time1.timestamp())
    print(time2.timestamp())
    print(time2.timestamp()-time1.timestamp())  #21240.0

#判断时间戳是否过时  5.9小时  21240
def isoutdate(time1stamp):
    now=datetime.now()
    nowstamp=now.timestamp()
    if(nowstamp-time1stamp>21240):
        return True
    else:
        return False

def init():
    #剑来
    url='http://book.zongheng.com/showchapter/672340.html'
    response=geturl(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    d1={"name":"剑来","chapCount":len(chap),"lastTitle":lastTitle}
    
    '''
    #公众号
    url='https://weixin.sogou.com/weixin?query=%E5%88%98%E5%A4%87%E6%95%99%E6%8E%88'
    response=geturl(url)
    selector=html.fromstring(response.content)
    lastTitle=selector.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[2]/dd/a/text()')[0]
    d2={"name":"公众号刘备教授","lastTitle":lastTitle}
    '''
    #d0={"jianlai":d1,"weixinso_liubei":d2}
    d0={"jianlai":d1}
    with open(path+'/temp.json','w') as f:
        json.dump(d0,f)

def test_jianlai(d_tmp,chapCount):
    mail_JianLai=mailpy.Email('1358109029@qq.com','keename@sina.com','MEIYOUSINA')
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    print(d_tmp["jianlai"]["lastTitle"])
    if chapCount !=len(chap):
        d_tmp["jianlai"]["chapCount"]=len(chap)
        d_tmp["jianlai"]["lastTitle"]=lastTitle
        with open(path+'/temp.json','w') as f:
            json.dump(d_tmp,f)
        mail_JianLai.send_Email('剑来更新了',lastTitle)
        print('    今天更新了...')


def test_weixinso1(d2):
    pass


#def savenote(url):
    #send_Email(title,url,save@note.youdao.com)

if __name__=='__main__':
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 相对路径为/root
        path='/opt/git_py/server_monitor'
    if not os.path.isfile(path+"/temp.json"):
        init()


    with open(path+'/temp.json','r') as f:
        d_tmp=json.load(f)
        print(d_tmp)
    print('begin loop:')    #提示信息

    '''
    #先取出最新
    #不断比较
    #更新后保存
    #最新 变化
    use_proxy()
    #保存参数,避免不断存取，更新时需要更新
    args1=[d_tmp["jianlai"]["chapCount"],d_tmp["weixinso_liubei"]["lastTitle"]]
    while(False):
        test_jianlai(d_tmp,args1[0])   #  剑来
        test_weixinso1(d_tmp)  #公众号 刘备教授
        time.sleep(10)
        #print(time.time())
    '''