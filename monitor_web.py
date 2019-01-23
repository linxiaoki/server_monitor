import requests
from lxml import html
import json
import os
import mailpy

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

def init():  
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    d1={"name":"剑来","chapCount":len(chap),"lastTitle":lastTitle}
    with open('temp.txt','w') as f:
        json.dump(d1,f)

def test_jianlai():
    mail_JianLai=mailpy.Email('kisaname@sina.com')
    url='http://book.zongheng.com/showchapter/672340.html'
    response=requests.get(url)
    selector=html.fromstring(response.content)
    chap=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li')
    lastTitle=selector.xpath('/html/body/div[3]/div[2]/div[2]/div/ul[@class="chapter-list clearfix"]/li/a/text()')
    lastTitle=lastTitle[-1]
    with open('temp.txt','r') as f:
        d1=json.load(f)
    if d1["chapCount"]!=len(chap):
        d1["chapCOunt"]=len(chap)
        d1["lastTitle"]=lastTitle
        with open('temp.txt','w') as f:
            json.dump(d1,f)
        mail_JianLai.mailpy('剑来更新了',lastTitle)

if __name__=='__main__':
    if not os.path.isfile("temp.txt"):
        init()
    test_jianlai()