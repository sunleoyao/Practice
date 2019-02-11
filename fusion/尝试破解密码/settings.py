# Author：ton
# -*- coding: utf-8 -*-
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_PATH, 'logs')
DATABASE_PATH = os.path.join(BASE_PATH, 'db')
HOST_TABLE_PATH = os.path.join(DATABASE_PATH, 'host')
GROUP_TABLE_PATH = os.path.join(DATABASE_PATH, 'group')
G2H_TABLE_PATH = os.path.join(DATABASE_PATH, 'group2Host')
TABLE_LIST = ['host', 'group', 'group2Host']


# 暴力破解配置项
user = 'sshusr'
password_list = ['123', 'sshusr123', '123456', ]
host_list = ['10.0.0.11', '10.0.0.12', '10.0.0.13', '10.0.0.14']
port = 22
root_pwd = '123456'

# 日志记录配置项
log_level = 'debug'
