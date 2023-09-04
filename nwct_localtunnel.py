# -*- coding: UTF-8 -*-
# Version: v1.5
# Created by lstcml on 2022/08/08
# 建议定时60分钟：*/60 * * * *

'''
更新记录：
v1.5
1、自动获取公网IP，访问穿透域名时需输入；
2、默认开启微信推送；

v1.4
1、修复一些bug；

v1.3
1、修复一些bug；

v1.2
1、因需点击才能跳转，去除穿透校验；
2、强制设置前缀域名；
3、去除微信推送；

v1.1
1、自动安装必要模块；
2、支持自定义域名前缀；
'''

import os
import re
import sys
import requests
from time import sleep

def update():
    print("当前运行的脚本版本：" + str(version))
    sys.stdout.flush()
    try:
        r1 = requests.get("hhttps://github.com/a512154224/qinglongscripts/raw/main/nwct_localtunnel.py").text
        r2 = re.findall(re.compile("version = \d.\d"), r1)[0].split("=")[1].strip()
        if float(r2) > version:
            print("发现新版本：" + r2)
            print("正在自动更新脚本...")
            sys.stdout.flush()
            os.system("ql raw https://github.com/a512154224/qinglongscripts/raw/main/nwct_localtunnel.py &")
            os._exit()
    except:
        pass

# 判断是否包含中文
def other_character(str):
    match = re.compile(u'[\u4e00-\u9fa5]').search(str)
    if match:
        return False
    else:
        if str.isalnum():
            return True
        else:
            return False
            

# 获取穿透url
def get_url():
    try:
        with open('localtunnel.lstcml', encoding='utf-8') as f:
            _content = f.read()
            if 'your url is' in _content:
                print("获取穿透链接成功...")
                sys.stdout.flush()
                return _content.split(': ')[1].replace('\n','')
            else:
                return 'failed'
    except:
        return 'failed'

# 执行程序
def start_nwct():
    PublicIP = getPublicIP()
    os.system('kill -9 `ps -ef | grep "lt --port" | grep -v grep | awk \'{print $1}\'`')
    os.system('lt --port 5700 -s ' + subdomain + ' > localtunnel.lstcml &')
    print("正在启动内网穿透...")
    sleep(10)
    print("正在获取穿透链接...")
    qlurl = get_url()
    if 'failed' not in qlurl:
        content = f"启动内网穿透成功！\n青龙面板：{qlurl}\n当前设备公网IP为：{PublicIP}\n若访问出现安全检测界面，先输入以上公网IP后，再点击蓝色'Click to Continue'按钮！"
        print(content)
        sys.stdout.flush()
        if load_send():
            send("内网穿透通知", content)
    else:
        print('获取穿透链接失败，请重试！')


# 获取公网IP
def getPublicIP():
    PublicIP = requests.get('http://ip.42.pl/raw', timeout=30).text
    if not checkIP(PublicIP):
        PublicIP = requests.get('http://ipv4.icanhazip.com', timeout=30).text
    return PublicIP


def checkIP(ip):
    if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
        return True
    else:
        return False


# 推送
def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    sendNotifPath = cur_path + "/sendNotify.py"
    if not os.path.exists(sendNotifPath):
        res = requests.get("https://github.com/a512154224/qinglongscripts/raw/main/sendNotify.py")
        with open(sendNotifPath, "wb") as f:
            f.write(res.content)
        
    try:
        from sendNotify import send
        return True
    except:
        print("加载通知服务失败！")
        return False

if __name__ == '__main__':
    version = 1.5
    try:
        subdomain = os.environ['qlsubdomain']
    except:
        subdomain = ""
    try:
        check_update = os.environ['qlnwctupdate']
    except:
        check_update = "true"
    try:
        import requests
    except:
        os.system('pip3 install requests >/dev/null 2>&1')
 
    if check_update != "false":
        update()
    else:
        print("变量qlnwctupdate未设置，脚本自动更新未开启！")
        sys.stdout.flush()
    if os.system('lt --help >/dev/null 2>&1') !=0:
        os.system('npm install -g localtunnel >/dev/null 2>&1')
    if len(subdomain) < 1:
        print("变量qlsubdomain未设置！")
        sys.stdout.flush()
    else:
        if other_character(subdomain):
            start_nwct()
        else:
            print("变量qlsubdomain仅支持英文数字组合！")
    
