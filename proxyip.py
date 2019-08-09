#!/usr/bin/env python3 
import requests
from fake_useragent import UserAgent
import json
import random
import socks
from datetime import datetime
import os

path=''  #注意在 linux 系统中，运行脚本时的 . 目录时 /root

#pip install fake-useragent
def get_proxyip_file(proxytype='http'):
    # 代理
    if proxytype=='http':
        # &country=GB
        proxyurl='https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=100&country=all&ssl=all&anonymity=all'
    elif proxytype=='socket4':
                #https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=250&country=all
        proxyurl='https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=100&country=all'
    else:  #socket5
                 #https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=100&country=all
        proxyurl='https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=150&country=all'
    try:
        ua=UserAgent()    # verify_ssl=False   veriify_ssl  是否验证服务器的SSL证书
        headers={"User-Agent":ua.random}
        #print(socks.get_default_proxy())    #mail.py  使用全局代理 发送邮件 测试
        response=requests.get(proxyurl,headers=headers)
        return response.text
    except Exception:
        return None


#  未：增加排序
def get_proxyip(proxytype='http'):
    path=os.path.abspath('.')
    if path=='/root':   #自动运行脚本时 centos7相对路径为/root ,需要手动改路径
        path='/opt/git_py/server_monitor'
    path=path+'/ini'
    if(not os.path.exists(path)):
        os.mkdir(path)
    proxies_filename=path+"/proxy_list.txt"

    modified_timestamp=0
    if os.path.isfile(proxies_filename):  #（没文件 或者 时间长 ） 重新写入     （有文件 并且 时间 短）  直接读取
        modified_timestamp=os.path.getmtime(proxies_filename)
    now_timestamp=datetime.now().timestamp()

    if (modified_timestamp != 0) and (now_timestamp-modified_timestamp)<3600:
        with open('ini/proxy_list.txt','r') as f:
            proxy_list=f.read()
            proxy_list=proxy_list.split('\n\n')[:-1]
    else:
        proxy_list=get_proxyip_file(proxytype)
        if proxy_list is None:
            raise ValueError('invalid proxy value: None.(proxyip.py)')
        with open('ini/proxy_list.txt','w') as f:
            f.write(proxy_list)
        proxy_list=proxy_list.split('\r\n')[:-1] 
    return random.choice(proxy_list)

#读取文件 ini/proxy_list.txt, 访问一个网址，测试响应时间并排序  还是筛选？
def sort_proxy():
    #def choice_proxy():
    pass

if __name__=="__main__":
    get_proxyip()

    '''
    #for test proxyip: get http/socket4/socket5
    ua=UserAgent(verify_ssl=False)
    headers={"User-Agent":ua.chrome}
    #测试代理  最多10次  ····返回可用代理    ····返回错误
    json_proxy=get_proxyip_json()
    proxies_someone=random.choice(json_proxy)
    print('begin test:'+proxies_someone)
    #proxies={"http":proxies_someone}
    proxies={"socket5":proxies_someone}
    response=requests.get("http://www.baidu.com",headers=headers,proxies=proxies)
    print('complete')
    '''

    