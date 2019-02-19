!#/usr/bin/env python3 
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

    #剑来
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    d1={"name":"剑来","chapCount":len(chap),"lastTitle":lastTitle}
    
    #公众号

    d2={"name":"公众号刘备教授","lastTitle":lastTitle}

    d0={"jianlai":d1,"weixinso_liubei":d2}
    with open(path+'/temp.txt','w') as f:
        json.dump(d0,f)

def test_jianlai(d_tmp,chapCount):
    mail_JianLai=mailpy.Email('1358109029@qq.com','keename@sina.com','MEIYOUSINA')
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    if chapCount !=len(chap):
        d_tmp["jianlai"]["chapCount"]=len(chap)
        d_tmp["jianlai"]["lastTitle"]=lastTitle
        with open(path+'/temp.txt','w') as f:
            json.dump(d_tmp,f)
        mail_JianLai.send_Email('剑来更新了',lastTitle)
        print('    今天更新了。')


def test_weixinso1(d2):
    pass

if __name__=='__main__':
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 相对路径为/root
        path='/opt/git_py/server_monitor'
    if not os.path.isfile(path+"/temp.txt"):
        init()
    with open(path+'/temp.txt','r') as f:
        d_tmp=json.load(f)
    print('begin loop:')    #提示信息
    #先取出最新
    #不断比较
    #更新后保存
    #最新 变化
    
    #保存参数,避免不断存取，更新时需要更新
    args1=[d_tmp["jianlai"]["chapCount"],d_tmp["weixinso_liubei"]["lastTitle"]]
    while(False):
        test_jianlai(d_tmp,args1[0])   #  剑来
        test_weixinso1(d_tmp)  #公众号 刘备教授
        time.sleep(10)
        #print(time.time())

