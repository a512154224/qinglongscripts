# -*- coding: UTF-8 -*-
# Version: v1.0
# Created by lstcml on 2023/09/28
# 因为隧道有效期为2小时，每次运行都会生成新的域名，建议定时2小时：0 */2 * * *


import os
import re
import sys
import requests
from time import sleep

'''
更新记录：

v1.1
1、修复穿透失败逻辑判断；

'''

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
        with open('nwt.lstcml', encoding='utf-8') as f:
            _content = f.read()
            if 'subdomain' in _content:
                print("获取穿透链接成功...")
                urls = re.findall(r'https?://\S+', _content)
                sys.stdout.flush()
                return urls
            else:
                print("获取穿透链接失败...")
                return ['failed']
    except:
        return ['failed']


# 执行程序
def start_nwct():
    os.system('killall ssh>/dev/null 2>&1&&chmod 700 /root/.ssh>/dev/null 2>&1&&chmod 600 /root/.ssh/config>/dev/null 2>&1&&chown root:root /root/.ssh/config>/dev/null 2>&1')
    os.system('nohup ssh -R 80:127.0.0.1:5700 -o StrictHostKeyChecking=no sh@sh3.neiwangyun.net > nwt.lstcml &')
    print("正在启动内网穿透...")
    sleep(10)
    print("正在获取穿透链接...")
    qlurls = get_url()
    if 'failed' not in qlurls:
        try:
            qlurl = f"{qlurls[0]}\n{qlurls[1]}"
        except:
            qlurl = f"{qlurls[0]}"
        content = f"启动内网穿透成功！\n青龙面板：\n{qlurl}\n"
        print(content)
        sys.stdout.flush()
        if load_send():
            send("内网穿透通知", content)
    else:
        print('启动内网穿透失败！')


def load_send():
    global send
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    sendNotifPath = cur_path + "/sendNotify.py"
    if not os.path.exists(sendNotifPath):
        res = requests.get("https://gitee.com/lstcml/scripts/raw/master/sendNotify.py")
        with open(sendNotifPath, "wb") as f:
            f.write(res.content)

    try:
        from sendNotify import send
        return True
    except:
        print("加载通知服务失败！")
        return False


if __name__ == '__main__':
    version = 1.0
    try:
        import requests
    except:
        os.system('pip3 install requests >/dev/null 2>&1')
    start_nwct()
