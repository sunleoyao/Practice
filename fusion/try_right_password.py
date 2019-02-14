import paramiko
import time
import sys

def ssh_user(host,username,password,port):
    s=paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(hostname = host,port=int(port),username=username, password=password,timeout=1)
    except Exception as a:
        print('目标服务器异常!')
        sys.exit(0)
    if username != 'root':
        ssh = s.invoke_shell()
        time.sleep(0.1)
        #先判断提示符，然后下一步在开始发送命令，这样大部分机器就都不会出现问题
        buff = ''
        count=0
        while (not buff.endswith('$ ')|count<50):
            resp = ssh.recv(9999)
            buff += resp.decode('utf8')
            count += 1
            time.sleep(0.1)
        # print('获取登录后的提示符：%s' %buff)
        ssh.send('export LANG=en_US.UTF-8 \n') #解决错误的关键，编码问题
        ssh.send('export LANGUAGE=en \n')
    print('Successful login in '+host+' !!!')
    print('login as riil')
    return ssh

def ssh_su_root(ssh,root_pwd_list):
    for root_password in root_pwd_list:
        buff=''
        ssh.send('su - root'+'\n')
        time.sleep(0.1)
        resp = ssh.recv(9999)
        buff += resp.decode('utf8')
        count=0
        while True:
            resp = ssh.recv(9999)
            buff = resp.decode('utf8')
            if buff.endswith('assword: '):
                ssh.send(root_password+'\n')
                time.sleep(0.1)
                resp = ssh.recv(9999)
                buff = resp.decode('utf8')
                if 'failure' in buff:
                    break
                if '#' in buff:
                    return 0,root_password
                    break
            count += 1
            time.sleep(0.01)
            if count > 500:
                return 1,''
                break

def ssh_root_cmd(ssh,root_cmd):
    ssh.send(root_cmd) #放入要执行的命令
    ssh.send('\n')
    buff = ''
    while not buff.endswith('# '):
        resp = ssh.recv(9999).decode()
        buff +=resp
    print(buff)
    result  = buff

def ssh_close(ssh):
    ssh.close()

if __name__ == "__main__":
    a=ssh_user('192.168.122.134', 'riil', 'riiladmin', '22')
    root_password=['rootroot1','rootroot','rootroot3']
    result,right_root_passwd = ssh_su_root(a,root_password)
    print('right_root_passwd : '+right_root_passwd)
    # if right_root_passwd =='0':
    #     ssh_root_cmd(a,'whoami')
    #     ssh_root_cmd(a,'pwd')
    ssh_close(a)