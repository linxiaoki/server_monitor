##### 更新：
    proxyip: 增加时间判断
    monitor_web.py    url 改为获取 ajax的json数据的网址
    增加配置目录  ./ini/temp.json   ./ini/proxy_list.txt
    
    未：
        使用装饰器 进行错误信息输出？  <<<init() 出错    装饰器 -> mail()>>>
        请求网址可以加装饰器吗？



##### 问题：
    输出找到为什么会停止：是因为请求的时候假死了？  需要timeout  + while true +try excepts
    mailpy.py  在 K-pc 电脑上运行错误：
            smtplib.SMTP_SSL 发送提示连接方一段时间后没有正确答复。。。
            smtplib.SMTP 正常运行


##### 代码
proxyip.py

    ```
        get_proxyip_json(proxytype = 'http'||'socket4'||'socket5')
            代理来源：https://api.proxyscrape.com/?request=getproxies&.........
            以json格式返回代理数据
        get_proxyip()
            >>>>path 需要手动设置
            获取文件修改时间，delTimeStamp > 1*60*60 
            有文件 并且 修改时间短  ->  直接读取  proxies.json
            文件不存在 或者 修改时间长  ->  重新写入 proxies.josn
    ```
    
monitor_web.py

    ```
        获取章节的网址更改：
            原url:  http://book.zongheng.com/showchapter/672340.html
            现url:  https://m.zongheng.com/h5/ajax/chapter/list?h5=1&bookId=672340&pageNum=1&chapterId=0&pageSize=20&asc=1
    ```
    


