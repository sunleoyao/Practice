# -*- coding: utf-8 -*-
import paramiko
# 服务器相关信息,下面输入你个人的用户名、密码、ip等信息
ip = "192.168.122.134"  
port =  22
user = "root"
password = "rootroot1"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 建立连接
try:
    ssh.connect(ip,port,user,password,timeout = 10)
except paramiko.ssh_exception.AuthenticationException:
    print("password is not right!")
else:
#输入linux命令
    stdin,stdout,stderr = ssh.exec_command("df -h")
# 输出命令执行结果
    result = stdout.read()
    print(result)
#关闭连接
    ssh.close()
