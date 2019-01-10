# -*- coding: utf-8 -*-
import paramiko
import time
# 服务器相关信息,下面输入你个人的用户名、密码、ip等信息
#ips = ['192.168.122.134','192.168.122.134','192.168.122.134']
ips = ['192.168.122.134']
port =  22
user = "riil"
password = "riiladmin"
root_password=['rootroot1','rootroot2','rootroot','rootroot3']
#cmds=['whoami', 'pwd\n', 'df -h\n']
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 建立连接
for ip in ips:
    ssh.connect(ip,port,user,password)
    chan=ssh.invoke_shell()
    time.sleep(1)
    output=''
    chan.send('whoami'+'\n')
    time.sleep(1)
    output=chan.recv(2048)
    print(output)
    output=''
    chan.send('su - root'+'\n')
    time.sleep(1)
    output=chan.recv(2048)
    print(output)
    output=''
    chan.send('rootroot'+'\n')
    time.sleep(1)
    output=chan.recv(2048)
    print(output)
    output=''
    chan.send('whoami'+'\n')
    time.sleep(1)
    output=chan.recv(2048)
    print(output)
    output=''
    print(output)
    chan.close()
    ssh.close()
