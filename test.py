# -*- coding: utf-8 -*-
import paramiko
# 创建SSH对象
ssh = paramiko.SSHClient()
# 把要连接的机器添加到known_hosts文件中
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='192.168.122.134', port=22,
            username='root', password='rootroot')
# cmd = 'ls -l;ifconfig'       #多个命令用;隔开
cmd = 'whoami'
stdin, stdout, stderr = ssh.exec_command(cmd)
print("stdin\n")
print(stdin)
print("stdout\n")
print(stdout)
print("stderr\n")
print(stderr)
result = stdout.read()
if not result:
    result = stderr.read()
ssh.close()
print(result.decode())
