# Author：ton
# -*- coding: utf-8 -*-
import paramiko
import os
import threading
import shelve
import re
import time
import xlrd
import xlwt
import json
from conf import settings
from models import models
from core.db_handler import Db_handler
from core.color import Colors
from core import logger
from threading import Thread


# paramiko.util.log_to_file(os.path.join(settings.LOG_PATH, 'paramiko.log'))
class Ideploy(object):
    def __init__(self):
        self.initDb()
        self.logger = logger.logger('MyIdeploy.log')
        self.host_db = shelve.open(os.path.join(settings.HOST_TABLE_PATH, 'host'))
        self.group_db = shelve.open(os.path.join(settings.GROUP_TABLE_PATH, 'group'))
        self.g2h_db = shelve.open(os.path.join(settings.G2H_TABLE_PATH, 'group2Host'))
        # 默认有default主机组
        self.default_group_obj = Db_handler.getGroupObjByGroupName(self.group_db, 'default')
        if not self.default_group_obj:
            self.default_group_obj = models.Group('default')
            Db_handler.insert_group(self.group_db, self.default_group_obj)
        self.thread_list = []
        self.instructions()
        self.run()
        self.host_db.close()
        self.group_db.close()
        self.g2h_db.close()

    @staticmethod
    def exit():
        exit('Bye')

    @staticmethod
    def instructions():
        """使用说明"""
        msg = """
        1、在conf/setttings下配置好需要暴力尝试密码的password_list和host_list
        2、在Terminal终端运行工具:python bin/ideploy.py -t start
        3、输入violentCipher，回车，完成后提示"暴力尝试密码完毕!"
        4、输入manageHosts，回车，可以查看管理暴力尝试密码成功的主机列表，记住默认主机组(default)的groupId为1，输入b，退出
        5、输入executeCommand，回车，输入批量执行命令：batch_run -g 1 -cmd "hostname"，该hostname命令执行的主机对象为默认主机组(default)下的所有主机
        6、输入show_task，回车，可以看到批量执行命令的结果
        7、继续输入批量执行命令：batch_scp -g 1 -action put -local __init__.py -remote /tmp/target.py，把本地文件__init__.py上传至远端/tmp/下，并取名为target.py
        8、输入show_task，回车，可以看到批量执行上传文件的结果
        9、输入q，退出批量执行命令的界面，输入exit，退出程序
        """
        print(msg)

    @staticmethod
    def initDb():
        """初始化数据库、日志目录"""
        # 初始化各表目录及其自增长ID记录文件
        for table_name in settings.TABLE_LIST:
            table_path = os.path.join(settings.DATABASE_PATH, table_name)
            table_id_file = os.path.join(table_path, 'countId')
            if not os.path.isdir(table_path):  # 创建数据文件路径
                os.mkdir(table_path)
            if not os.path.isfile('%s.dat' % table_id_file):  # 创建自增长ID记录文件
                data_dic = shelve.open(table_id_file)
                data_dic['id'] = '0'
                data_dic.close()
        # 初始化日志目录
        if not os.path.isdir(os.path.join(settings.BASE_PATH, 'logs')):
            os.mkdir(os.path.join(settings.BASE_PATH, 'logs'))

    def run(self):
        while True:
            print("欢迎来到Ideploy".center(45, '-'))
            msg = """
                violentCipher暴力尝试密码
                createGroups创建主机组
                manageHosts管理主机
                executeCommand批量执行命令
                exportHostToExcel导出主机信息到excel表
                importHostFromExcel从excel表导入主机信息
                exit退出
            """
            print(Colors(msg))
            print('thread number:%s' % threading.active_count())
            print("".center(50, '-'))
            choice = input('输入命令>>').strip()
            if hasattr(self, choice):
                getattr(self, choice)()

    def violentCipher(self):
        """为每个主机分配线程尝试ssh密码"""
        for host in settings.host_list:
            # 多线程尝试ssh密码
            t = Thread(target=self.tryPasswordForHost, args=(host, settings.port, settings.user))
            t.setDaemon(True)
            self.thread_list.append(t)
            # 单线程尝试ssh密码
            # self.try_password_for_host(ip, settings.port, settings.user)
        for t in self.thread_list:
            t.start()
        for t in self.thread_list:
            t.join()
        self.thread_list = []
        print(Colors('暴力尝试密码完毕!输入"manageHosts"可以管理主机', 'green'))

    def tryPasswordForHost(self, host, port, user):
        """循环ssh密码列表尝试密码,并把正确密码保存文件"""
        password_list = settings.password_list
        for passwd in password_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, port=port, username=user, password=passwd, timeout=3)
                msg = 'correct ip:%s user:%s password:%s' % (host, user, passwd)
                print(Colors(msg, 'green'))
                # 更新host、g2h表
                host_obj = models.Host(host, port, user, passwd)
                Db_handler.update_host(self.host_db, host_obj)
                return_host_obj = Db_handler.check_unique_host(self.host_db, host_obj)
                if return_host_obj:
                    host_obj = return_host_obj
                Db_handler.insert_g2h(self.g2h_db, host_obj, self.default_group_obj)
                break
            except KeyError as e:
                raise e  # 调试
            except Exception as e:
                print(Colors(str(e), 'red'))
                msg = 'wrong ip:%s user:%s password:%s' % (host, user, passwd)
                print(Colors(msg, 'red'))
            finally:
                ssh.close()

    def checkPassword(self):
        """检查ssh密码和root密码的有效性"""
        pass

    def exportHostToExcel(self):
        """从数据库导出所有主机信息到excel表里"""
        # 创建workbook和sheet对象
        workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
        sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        # 向sheet页中写入列名数据
        column_names = ['host', 'groupName', 'user', 'password', 'port']
        for index, col in enumerate(column_names):
            sheet1.write(0, index, col)
        # 读取数据库，按group读取host
        group_list = []
        for key in self.group_db:
            group_list.append(self.group_db[key])
        group_list.sort(key=lambda group_obj: group_obj.groupId, reverse=False)  # 根据groupId排序
        for g_obj in group_list:
            # 根据主机组Id,获取该主机组所有主机Obj列表
            host_list = Db_handler.getHostObjListByGroupId(self.host_db, self.g2h_db, g_obj.groupId)
            host_list.sort(key=lambda obj: obj.host, reverse=False)  # 根据主机的ip排序
            # 向sheet页中写入host数据
            for row_num, host_obj in enumerate(host_list, 1):
                col_values = [host_obj.host, g_obj.groupName, host_obj.user, host_obj.password, host_obj.port]
                for col_num, col_val in enumerate(col_values):
                    sheet1.write(row_num, col_num, col_val)
        workbook.save(os.path.join(settings.BASE_PATH, 'hosts.xls'))
        print(Colors('导出成功!导出文件:%s' % os.path.join(settings.BASE_PATH, 'hosts.xls'), 'green'))

    def importHostFromExcel(self):
        """从excel表中导入主机信息并存入数据库"""
        # 打开一个workbook
        workbook = xlrd.open_workbook(os.path.join(settings.BASE_PATH, 'hosts.xls'))
        # 定位到sheet1
        sheet1 = workbook.sheets()[0]
        # 遍历sheet1中所有行row
        num_rows = sheet1.nrows
        for row_num in range(1, num_rows):
            row_val = sheet1.row_values(row_num)
            group_obj = Db_handler.getGroupObjByGroupName(self.group_db, row_val[1])
            if group_obj:
                host_obj = models.Host(row_val[0], int(row_val[4]), row_val[2], row_val[3])
                Db_handler.update_host(self.host_db, host_obj)
                return_host_obj = Db_handler.check_unique_host(self.host_db, host_obj)
                if return_host_obj:
                    host_obj = return_host_obj
                    Db_handler.insert_g2h(self.g2h_db, host_obj, group_obj)
            else:
                print(Colors('没有该主机组名[%s]' % row_val[1], 'red'))
        else:
            print(Colors("导入成功!请输入'manageHosts'查看导入的主机", 'green'))

    def createGroups(self):
        while True:
            create_groupName = input('请输入需要创建的主机组名(b退出):').strip()
            if not create_groupName: continue
            if create_groupName == 'b': break
            create_group = models.Group(create_groupName)
            result_code = Db_handler.insert_group(self.group_db, create_group)
            if result_code:
                print(Colors('创建主机组成功', 'green'))
            else:
                print(Colors('该主机组已存在', 'red'))

    def manageHosts(self):
        """分配主机到主机组"""
        # 解析分配的hostId和groupId,判断是否存在
        while True:
            print('所有主机信息如下:')
            self.displayHosts()
            choice_action = input('请输入要对主机组执行的操作(add添加,del删除,b退出):').strip()
            if choice_action == 'b':
                break
            elif choice_action != 'add' and choice_action != 'del':
                continue
            quit_flag = True
            while quit_flag:
                choice_hostIds = input('请输入hostId(用空格隔开)(b退出):').strip()
                if not choice_hostIds: continue
                if choice_hostIds == 'b': break
                hostId_list = choice_hostIds.split()
                exist_flag = True
                for hostId in hostId_list:
                    if hostId not in self.host_db:
                        exist_flag = False
                        print(Colors('输入要操作的hostId:%s 不存在' % hostId, 'red'))
                if not exist_flag: continue
                while quit_flag:
                    choice_groupId = input('请输入要操作的groupId(b退出):').strip()
                    if not choice_groupId: continue
                    if choice_groupId == 'b': break
                    if choice_groupId not in self.group_db:
                        print(Colors('输入的groupId:%s 不存在' % choice_groupId, 'red'))
                        continue
                    # 开始更新g2h表
                    for hostId in hostId_list:
                        if choice_action == 'add':
                            Db_handler.insert_g2h(self.g2h_db, self.host_db[hostId], self.group_db[choice_groupId])
                        else:
                            Db_handler.delete_g2h(self.g2h_db, self.host_db[hostId], self.group_db[choice_groupId])
                    print(Colors('配置成功', 'green'))
                    quit_flag = False

    def displayHosts(self):
        """展示管理的主机"""
        group_list = []
        for key in self.group_db:
            group_list.append(self.group_db[key])
        group_list.sort(key=lambda group_obj: group_obj.groupId, reverse=False)  # 根据groupId排序
        for g_obj in group_list:
            # 根据主机组Id,获取该主机组所有主机Obj列表
            host_list = Db_handler.getHostObjListByGroupId(self.host_db, self.g2h_db, g_obj.groupId)
            print(Colors(
                'Group:%s[%d](groupId:%s)' % (g_obj.groupName, len(host_list), g_obj.groupId), 'cyan'))
            host_list.sort(key=lambda obj: obj.host, reverse=False)  # 根据主机的ip排序
            for host_obj in host_list:
                print('\t%s' % host_obj)

    def executeCommand(self):
        """批量执行ssh命令"""
        SSHClient(self)


class TaskList(list):
    def __init__(self, item=()):
        super().__init__(item)
        self.logger = logger.logger('task_list')

    def append(self, p_object):
        if not isinstance(p_object, dict):
            raise TypeError
        super().append(p_object)
        # with open(os.path.join(settings.BASE_PATH, 'task_list'), 'a') as f:
        #     f.write(json.dumps(p_object) + '\n')
        self.logger.info(json.dumps(p_object))


class SSHClient(object):
    def __init__(self, ideploy_obj):
        self.ideploy_obj = ideploy_obj
        self.task_list = TaskList()
        self.interactive()

    @staticmethod
    def help_msg():
        """ssh命令帮助信息"""
        msg = """注意:-h 后为hostId，-g 后为groupId
        batch_run -h 1,2,3 -g 1,2 -cmd "df -h"
        batch_scp -h 1,2,3 -g 1,2 -action put -local test.py -remote /tmp/　
        show_task  查看ssh命令结果
        """
        print(msg)

    def interactive(self):
        while True:
            print('\n thread number:%s' % threading.active_count())
            cmd = input(Colors('批量执行命令>>', 'cyan')).strip()
            if not cmd: continue
            if cmd == 'q': break
            if hasattr(self, cmd[:9]):
                getattr(self, cmd[:9])(cmd[9:].strip())
            else:
                self.help_msg()

    @staticmethod
    def create_task_dic(hostId, host, command, result, date):
        task_dic = {
            'hostId': hostId,
            'host': host,
            'command': command,
            'result': result,
            'date': date,
        }
        return task_dic

    def show_task(self, cmd):
        for task_dic in self.task_list:
            print(
                '\033[36m(hostId:%s)host:\033[0m%s \033[36mcommand:\033[0m%s \033[36mresult:\033[0m\n%s \033[36mdate:\033[0m%s' % (
                    task_dic['hostId'], task_dic['host'], task_dic['command'], task_dic['result'], task_dic['date']))

    def batch_run(self, cmd):
        """批量执行batch_run命令"""
        argv_dic = self.parse_run_command(cmd)
        if argv_dic['cmd']:
            self.batch('batch_run', argv_dic)
        else:
            self.help_msg()

    def connect_batch_run(self, host_obj, argv_dic):
        """与ssh服务端通讯执行远程ssh命令"""
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host_obj.host, port=host_obj.port, username=host_obj.user, password=host_obj.password,
                        timeout=5)
            channel = ssh.invoke_shell()
            result = ''
            if host_obj.user != 'root':
                # channel.send("sudo su - \n")
                channel.send("su - \n")
                # 下面几行代码是发送 su - root命令时所需要输入的root密码,配置了/etc/sudoers NOPASSWD就不用密码了
                while not re.search(r'(P|p)assword: $', result):
                    result += channel.recv(8196).decode('utf-8')
                self.ideploy_obj.logger.info(b"++" + result.encode('utf-8') + b'++')
                result = ''
                channel.send('%s\n' % settings.root_pwd)
            while not re.search(r'#[^#]{0,13}$', result):
                result += channel.recv(8196).decode('utf-8')
            self.ideploy_obj.logger.info(b"++" + result.encode('utf-8') + b'++')
            result = ''
            channel.send('%s\n' % argv_dic['cmd'])
            while not re.search(r'#[^#]{0,13}$', result):
                result += channel.recv(8196).decode('utf-8')
            self.ideploy_obj.logger.info(b"++" + result.encode('utf-8') + b'++')
            result_list = re.findall(r".*\n", result)[1:]
            result = ''.join(result_list)
            channel.close()
            self.task_list.append(self.create_task_dic(host_obj.hostId, host_obj.host,
                                                       argv_dic['cmd'], result,
                                                       time.strftime("%Y-%m-%d %X", time.localtime())))
        except Exception as e:
            self.task_list.append(
                self.create_task_dic(host_obj.hostId, host_obj.host, argv_dic['cmd'], str(e),
                                     time.strftime("%Y-%m-%d %X", time.localtime())))
        finally:
            ssh.close()

    def connect_batch_scp(self, host_obj, argv_dic):
        """与ssh服务端建立sftp通道执行远程scp命令"""
        try:
            transport = paramiko.Transport((host_obj.host, host_obj.port))
            transport.connect(username=host_obj.user, password=host_obj.password, )
            sftp = paramiko.SFTPClient.from_transport(transport)
            if argv_dic['action'] == 'put':
                # 将location.py 上传至服务器 /tmp/test.py
                sftp.put(argv_dic['local'], argv_dic['remote'])
            else:
                # 将remove_path 下载到本地 local_path
                sftp.get(argv_dic['remote'], argv_dic['local'])
            self.task_list.append(
                self.create_task_dic(host_obj.hostId, host_obj.host,
                                     'action[%s] local[%s] remote[%s]' % (
                                         argv_dic['action'], argv_dic['local'], argv_dic['remote']), 'OK',
                                     time.strftime("%Y-%m-%d %X", time.localtime())))
        except Exception as e:
            self.task_list.append(
                self.create_task_dic(host_obj.hostId, host_obj.host,
                                     'action[%s] local[%s] remote[%s]' % (
                                         argv_dic['action'], argv_dic['local'], argv_dic['remote']), str(e),
                                     time.strftime("%Y-%m-%d %X", time.localtime())))
        finally:
            try:
                transport.close()
            except UnboundLocalError:
                pass

    def batch(self, batch_type, argv_dic):
        """为每个host分配一个线程去连接ssh服务端批量执行batch_run或batch_scp命令"""
        finished_hostId_list = []
        batch_type_func = 'connect_%s' % batch_type
        if argv_dic.get('group_list'):
            for groupId in argv_dic['group_list']:
                if groupId in self.ideploy_obj.group_db:
                    host_list = Db_handler.getHostObjListByGroupId(self.ideploy_obj.host_db, self.ideploy_obj.g2h_db,
                                                                   groupId)
                    for host_obj in host_list:
                        t = Thread(target=getattr(self, batch_type_func), args=(host_obj, argv_dic))
                        t.setDaemon(True)
                        t.start()
                        finished_hostId_list.append(host_obj.hostId)
                else:
                    self.task_list.append(self.create_task_dic("groupId[%s]" % groupId, None,
                                                               None, "groupId[%s] is not exist" % groupId,
                                                               time.strftime("%Y-%m-%d %X", time.localtime())))
        if argv_dic.get('host_list'):
            for hostId in argv_dic['host_list']:
                if hostId in self.ideploy_obj.host_db:
                    if hostId not in finished_hostId_list:
                        t = Thread(target=getattr(self, batch_type_func),
                                   args=(self.ideploy_obj.host_db[hostId], argv_dic))
                        t.setDaemon(True)
                        t.start()
                else:
                    self.task_list.append(self.create_task_dic(hostId, None,
                                                               None, "hostId[%s] is not exist" % hostId,
                                                               time.strftime("%Y-%m-%d %X", time.localtime())))

    def batch_scp(self, cmd):
        """批量执行batch_scp命令"""
        argv_dic = self.parse_scp_command(cmd)
        if argv_dic['action'] and argv_dic['local'] and argv_dic['remote']:
            self.batch('batch_scp', argv_dic)
        else:
            self.help_msg()

    @staticmethod
    def parse_target(cmd):  # -h h1,h2,h3 -g web_clusters,db_servers -cmd "df -h"
        """解析-h、-g参数，获取主机、主机组列表"""
        host_str = re.match(r"-h[ ]+[^-]+", cmd)
        host_list = host_str.group().strip()[2:].strip().replace(r" ", "").split(",") if host_str else None
        group_str = re.search(r"-g[ ]+[^-]+", cmd)
        group_list = group_str.group().strip()[2:].strip().replace(r" ", "").split(",") if group_str else None
        return host_list, group_list

    def parse_run_command(self, cmd):  # -h h1,h2,h3 -g web_clusters,db_servers -cmd "df -h"
        """解析batch_run命令参数"""
        host_list, group_list = self.parse_target(cmd)
        real_cmd_str = re.search(r"-cmd[ ]+(\'|\")(?P<cmd>.*)(\'|\")", cmd)
        if real_cmd_str:
            real_cmd_dic = real_cmd_str.groupdict()
            real_cmd_str = real_cmd_dic['cmd'].strip()
        else:
            real_cmd_str = None
        argv_dic = {
            'host_list': host_list,
            'group_list': group_list,
            'cmd': real_cmd_str
        }
        return argv_dic

    def parse_scp_command(self, cmd):  # -h h1,h2,h3 -g web_clusters,db_servers -action put -local test.py -remote /tmp/
        """解析batch_scp命令参数"""
        host_list, group_list = self.parse_target(cmd)
        action_str = re.search(r"-action[ ]+[^-]+", cmd)
        action_str = action_str.group().strip()[7:].strip() if action_str else None
        local_str = re.search(r"-local[ ]+[^-]+", cmd)
        local_str = local_str.group().strip()[6:].strip() if local_str else None
        remote_str = re.search(r"-remote[ ]+[^-]+", cmd)
        remote_str = remote_str.group().strip()[7:].strip() if remote_str else None
        argv_dic = {
            'host_list': host_list,
            'group_list': group_list,
            'action': action_str,
            'local': local_str,
            'remote': remote_str
        }
        return argv_dic
