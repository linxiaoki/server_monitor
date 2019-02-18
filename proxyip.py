import requests
from fake_useragent import UserAgent
import json
import random

#pip install fake-useragent
def get_proxyip_json():
    # 代理
    #proxyurl='https://proxyscrape.com/api?request=getproxies&proxytype=http&timeout=50&country=GB&ssl=all&anonymity=all'
    #proxyurl='https://proxyscrape.com/api?request=getproxies&proxytype=socks4&timeout=50&country=all'
    proxyurl='https://proxyscrape.com/api?request=getproxies&proxytype=socks5&timeout=200&country=all'
    try:
        ua=UserAgent(verify_ssl=False)    #veriify_ssl  是否验证服务器的SSL证书
        headers={"User-Agent":ua.random}
        json_proxy=requests.get(proxyurl,headers=headers)
        return json_proxy.text.split('\r\n')[:-1]
    except:
        return None

#  未：增加排序
def get_proxyip():
    json_proxy=get_proxyip_json()
    return random.choice(json_proxy)

if __name__=="__main__":
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
