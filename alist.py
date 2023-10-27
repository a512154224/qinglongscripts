# -*- coding: UTF-8 -*-
import os, json, time, socket, requests
from time import sleep

# 判断CPU架构
def check_os():
    r = os.popen('uname -m').read()
    if 'aarch64' in r:
        cpu = 'arm64'
    elif 'x86_64' in r or 'x64' in r:
        cpu = 'amd64'
    else:
        cpu = '非arm64'
        print('不是不支持当前架构，我懒得弄了，自己去https://github.com/alist-org/alist/releases下载吧')
        return
    print('获取CPU架构：' + r.replace('\n', ''))
    download_alist(cpu)

# 下载主程序
def download_alist(cpu):
    if not os.path.exists("/etc/alist/alist"):
        print("alist程序不存在，尝试安装...")
        res = requests.get(f"https://github.com/alist-org/alist/releases/download/v3.28.0/alist-linux-musl-{cpu}.tar.gz")
        with open("alist.tar.gz", "wb") as f:
            f.write(res.content)
        os.system("tar zxf alist.tar.gz>&1&&rm -f alist.tar.gz&&chmod +x alist&&mv alist /etc/alist/")
        print("alist安装成功，尝试运行")
    else:
        print("alist已安装，尝试运行")
    
# 进程守护
def process_daemon():
    n = os.popen("ps -ef | grep alist").read()
    command = "alist server"
    if command not in n:
        os.chdir("/etc/alist/")
        os.system(command + ">/dev/null 2>&1 &")
        n = os.popen("ps -ef | grep alist").read()
        if command not in n:
            print("启动Alist失败.")
            return "启动Alist失败."
        else:
            print("启动Alist成功.")
            return "启动Alist成功."
    else:
        print("Alist已运行中.")
        return "Alist已运行中."

# 查询本机ip地址
def get_host_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
    
#获取Alist端口
def get_alist_port():
    sleep(5)
    try:
        with open(config_path) as f:
            r = f.read()
            try:
                r = json.loads(r)
                return str(r["scheme"]["http_port"])
            except:
                return "转换Json失败."
    except:
        return "获取Alist端口号失败."

if __name__ == '__main__':
    check_os()
    os.system("mkdir /etc/alist>/dev/null 2>&1 &")
    config_path = "/etc/alist/data/config.json"
    if "失败" not in process_daemon():
        port = get_alist_port()
        sleep(3)
        if "失败" not in port:
            print("访问地址：http://" + get_host_ip() + ":" + port)
        else:
            print(port)