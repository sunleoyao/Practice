import pymysql
import sys

class mysql(object):

    def __init__(self, ip, user_name, user_passwd, mysql_name):
        self.ip = ip
        self.user_name = user_name
        self.user_passwd = user_passwd
        self.mysql_name = mysql_name
        try:
            self.db = pymysql.connect(self.ip,self.user_name,self.user_passwd,self.mysql_name)
            self.cursor = self.db.cursor()
        except Exception as a:
            print('Please check mysql information!')
            sys.exit(0)
    
    def excute(self,sql):
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        return data

    def close(self):
        self.db.close()