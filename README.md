# 青龙脚本

## 介绍
一些青龙面板的有趣脚本


### nwct_nwt.py
名称：青龙外网访问

拉取：ql raw https://github.com/a512154224/qinglongscripts/raw/main/nwct_nwt.py

配置：无，手动运行一次任务，再查看任务日志和pushplus推送

定时：0 */2 * * *（建议2小时）


### nwct_xmq.py
名称：青龙外网访问

拉取：ql raw https://github.com/a512154224/qinglongscripts/raw/main/nwct_xmq.py

配置：使用方法参考脚本注释，变量qxmq_authtoken为域名前缀，建议首次手动运行一次任务，再查看任务日志

定时：*/10 * * * *（建议10分钟）


### nwct_localtunnel.py

名称：青龙外网访问

拉取：ql raw https://github.com/a512154224/qinglongscripts/raw/main/nwct_localtunnel.py

配置：变量qlsubdomain为域名前缀，建议首次手动运行一次任务，再查看任务日志

定时：*/50 * * * *（建议10分钟）


### nwct_cpolar.py
名称：青龙外网访问

拉取：ql raw https://github.com/a512154224/qinglongscripts/raw/main/nwct_cpolar.py

配置：使用方法参考脚本注释，变量qlnwct_authtoken为域名前缀，建议首次手动运行一次任务，再查看任务日志

定时：*/10 * * * *（建议10分钟）


### alist.py
名称：阿里云云盘的辅助脚本
拉取：ql raw https://github.com/a512154224/qinglongscripts/raw/main/alist.py

配置：暂无

定时：*/50 * * * *（随意，不要太频繁即可）
