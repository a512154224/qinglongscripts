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
import requests
from time import sleep

def check_os():
    global url
    print('正在检测设备架构.')
    cpu_arch = os.popen('uname -m').read()
    if 'arm' in cpu_arch or 'aarch64' in cpu_arch:
        url = "http://note.youdao.com/yws/api/personal/file/WEB59a6cc544058b069c139957f720ad471?method=download&inline=true&shareKey=06b9e878c8991524296fda31791826fa"
        download_app('arm')
    elif 'x86' in cpu_arch or 'x64' in cpu_arch:
        url = "http://note.youdao.com/yws/api/personal/file/WEB2631b2592aaa8a72e4649c9b96653208?method=download&inline=true&shareKey=f66ac55dba68dbe929028ff6c231758d"
        download_app('386')
    else:
        print('暂不支持当前架构.')

def download_app(cpu):
    print('当前架构支持穿透.')
    if not os.path.exists("xiaomiqiu"):
        print("正在检测穿透程序.\n尝试下载穿透程序.")
        try:
            app_url = f"https://github.com/a512154224/qinglongscripts/raw/main/xiaomiqiu_{cpu}"
            res = requests.get(app_url, timeout=300)
            with open("xiaomiqiu", "wb") as f:
                f.write(res.content)
            print("穿透程序下载成功.")
            start_nwct()
        except:
            print("穿透程序下载失败.\n切换下载地址重试.")
            try:
                res = requests.get(url, timeout=300)
                with open("xiaomiqiu", "wb") as f:
                    f.write(res.content)
                print("穿透程序下载成功.")
                start_nwct()
            except:
                print("穿透程序下载失败.\n请检查网络后重试.")
                os.system(f"rm -rf {app_path}")
    else:
        print("检测穿透程序存在.")
        start_nwct()

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

def start_nwct():
    if not process_daemon():
        os.system("killall xiaomiqiu >/dev/null 2>&1")
        print("正在启动穿透服务.")
        os.system(f"{app_path} start-all &")
        sleep(5)
        if process_daemon():
            print("启动穿透服务成功.")
        else:
            print("启动穿透服务失败.")
    else:
        print("穿透服务已在运行.")

def create_conf(xmqserver, authtoken):
    conf_path = os.path.join(path, "xiaomiqiu.conf")
    content = f"server_addr: {xmqserver}\ntrust_host_root_certs: true\nauth_token: {authtoken}"
    with open(conf_path, "wb") as f:
        f.write(content.encode('utf-8'))

if __name__ == '__main__':
    authtoken = os.environ.get('xmq_authtoken', "")
    xmqserver = os.environ.get('xmq_server', "ngrok2.xiaomiqiu.cn:5432")
    path = os.path.split(os.path.realpath(__file__))[0]
    app_path = os.path.join(path, "xiaomiqiu")
    if len(authtoken) < 1:
        print("请新增变量xmq_authtoken.")
    else:
        create_conf(xmqserver, authtoken)
        check_os()
