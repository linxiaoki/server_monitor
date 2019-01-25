import requests
from lxml import html
import json
import os
import mailpy
import time

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
def init():
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    d1={"name":"剑来","chapCount":len(chap),"lastTitle":lastTitle}
    with open(path+'/temp.txt','w') as f:
        json.dump(d1,f)

def test_jianlai(d1):
    mail_JianLai=mailpy.Email('1358109029@qq.com','keename@sina.com','MEIYOUSINA')
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    if d1["chapCount"]!=len(chap):
        d1["chapCount"]=len(chap)
        d1["lastTitle"]=lastTitle
        with open(path+'/temp.txt','w') as f:
            json.dump(d1,f)
        mail_JianLai.send_Email('剑来更新了',lastTitle)

if __name__=='__main__':
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 相对路径为/root
        path='/opt/git_py/server_monitor'
    if not os.path.isfile(path+"/temp.txt"):
        init()
    with open(path+'/temp.txt','r') as f:
        d1=json.load(f)
    while(True):
        test_jianlai(d1)
        time.sleep(10)
        #print(time.time())
