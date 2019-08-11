#!/bin/sh
# 获取 monitor_web.py 进程ID
monitorID=$(ps -ef|grep monitor_web.py|grep -v 'sh'|grep -v 'log'|grep -v 'grep'|awk '{print $2}')
#count=$(ps -ef|grep monitor|grep -v 'sh'|grep -v 'log'|grep -v 'grep'|wc -l)
#echo $count     #如果没有   #echo count -eq 0    #echo ($count = 0)
if [ -z $monitorID ]; then
    #echo 'run monitor_web.py'
    /usr/bin/python /opt/git_py/server_monitor/monitor_web.py > /opt/git_py/server_monitor/RUN-LOG 2>&1
    #/usr/bin/python /opt/git_py/server_monitor/monitor_web.py 
else
    #count > 1 怎么搞  删除多个进程
    #杀进程
    #echo '有进程'
    #echo $monitorID  #echo 是什么命令
    kill $monitorID
    /usr/bin/python /opt/git_py/server_monitor/monitor_web.py > /opt/git_py/server_monitor/RUN-LOG 2>&1
fi

