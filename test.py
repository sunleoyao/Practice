import paramiko
import time

def verification_ssh(host,username,password,port,root_pwd,cmd):
    s=paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname = host,port=int(port),username=username, password=password)
    if username != 'root':
        ssh = s.invoke_shell()
        time.sleep(0.1)
        #先判断提示符，然后下一步在开始发送命令，这样大部分机器就都不会出现问题
        buff = ''
        while not buff.endswith('$ '):
            resp = ssh.recv(9999)
            buff += resp.decode('utf8')
            time.sleep(0.1)
        print('获取登录后的提示符：%s' %buff)
        ssh.send('export LANG=en_US.UTF-8 \n') #解决错误的关键，编码问题
        ssh.send('export LANGUAGE=en \n')
        ssh.send('su - \n')
        buff = ""
        while not buff.endswith('Password: '): #true
            resp = ssh.recv(9999)
            print(resp)
            buff +=resp.decode('utf8')
        print(buff)
        ssh.send(root_pwd)
        ssh.send('\n')
        buff = ""
        while not buff.endswith('# '):
            resp = ssh.recv(9999)
            print(resp)
            buff +=resp.decode('utf8')
        ssh.send('df -h') #放入要执行的命令
        ssh.send('\n')
        buff = ''
        while not buff.endswith('# '):
            resp = ssh.recv(9999).decode()
            buff +=resp
        print(buff)
        result  = buff
        s.close()

if __name__ == "__main__":
    verification_ssh('192.168.122.134', 'riil', 'riiladmin', '22', 'rootroot1', 'id')