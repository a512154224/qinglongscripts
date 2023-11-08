# -*- coding: UTF-8 -*-
# Version: v1.0
# Created by lstcml on 2023/11/08
# 建议定时10分钟：*/10 * * * *

'''
使用说明：
1、
2、打开https://manager.xiaomiqiu.com/login注册登录后获取authtoken
3、新增变量xmq_authtoken，值为你账户的authtoken，运行脚本
4、提示成功后，参考https://blog.xiaomiqiu.com/article/121在管理后台新增的隧道即可

更新记录：

v1.0
1、支持免费版与vip服务器；
'''


import os
import re
import sys
import json
import requests
from time import sleep
path = os.path.split(os.path.realpath(__file__))[0]
app_path = os.path.join(path, "xiaomiqiu")
conf_path = os.path.join(path, "xiaomiqiu.conf")
sendNotify_path = os.path.join(path, "sendNotify.py")

# 判断CPU架构
def check_os():
    r = os.popen('uname -m').read()
    if 'arm' in r or 'aarch64' in r:
        cpu = 'arm'
    elif 'x86' in r or 'x64' in r:
        cpu = '386'
    else:
        print('穿透失败：不支持当前架构！')
        return
    print('获取CPU架构：' + r.replace('\n', ''))
    download_app(cpu)

# 下载主程序
def download_app(cpu):
    if not os.path.exists("xiaomiqiu"):
        print("正在检测穿透程序.\n尝试下载穿透程序.")
        try:
            res = requests.get(f"https://github.com/a512154224/qinglongscripts/raw/main/xiaomiqiu_{cpu}")
            with open("xiaomiqiu", "wb") as f:
                f.write(res.content)
            print("穿透程序下载成功.")
            start_nwct()        
        except:
            print("穿透程序下载失败.\n请检查网络后重试.")
            os.system(f"rm -rf {app_path}")
    else:
        print("检测穿透程序存在")
        start_nwct()

# 进程守护
def process_daemon():
    print("正在检测穿透服务.")
    try:
        res = requests.get("http://127.0.0.1:4040/http/in").text
        if "小米球" in res or "xiaomiqiu" in res:
            return True
        else:
            return False
    except:
        return False


# 执行程序
def start_nwct():
    if not process_daemon():
        os.system("killall xiaomiqiu >/dev/null 2>&1")
        print("正在启动穿透服务.")
        os.system(f"{app_path} start-all &")
        sleep(5)
        if process_daemon():
            print("启动穿透服务成功.")
            # if load_send():
            #     send("内网穿透通知", "穿透服务启动成功.")
        else:
            print("启动穿透服务失败.")
    else:
        print("穿透服务已在运行.")


# 生成配置文件
def create_conf():
    content = f"server_addr: {xmqserver}\ntrust_host_root_certs: true\nauth_token: {authtoken}"
    with open(conf_path, "wb") as f:
            f.write(content.encode('utf-8'))

# # 推送
# def load_send():
#     global send
#     try:
#         if not os.path.exists(sendNotify_path):
#             print("尝试下载推送程序")
#             res = requests.get("https://github.com/a512154224/qinglongscripts/raw/main/sendNotify.py")
#             with open(sendNotify_path, "wb") as f:
#                 f.write(res.content)
#             print("下载推送程序成功")
#         from sendNotify import send
#         return True
#     except:
#         print("下载推送程序失败")
#         print("加载通知服务失败.")
#         print("推送并不影响穿透.")
#         return False


if __name__ == '__main__':
    try:
        authtoken = os.environ['xmq_authtoken']
    except:
        authtoken = ""
    try:
        token = os.environ['PUSH_PLUS_TOKEN']
    except:
        token = ""
    try:
        xmqserver = os.environ['xmq_server']
        print("当前使用vip服务器，免费用户移除xmq_server变量.")
    except:
        xmqserver = "ngrok2.xiaomiqiu.cn:5432"
        print("当前使用免费服务器，vip用户新增xmq_server变量.")
    if len(authtoken ) < 1:
        print("请新增变量xmq_authtoken.")
    else:
        create_conf()
        check_os()