import pymysql

class mysql(object):
    def __init__(self, ip, user_name, user_passwd, mysql_name):
        self.ip = ip
        self.user_name = user_name
        self.user_passwd = user_passwd
        self.mysql_name = mysql_name

    def connect(self):
        db = pymysql.connect(self.ip,self.user_name,self.user_passwd,self.mysql_name)
        cursor = db.cursor()
        return db,cursor
    
    def execute(self,cursor,sql):
        cursor.execute(sql)
        data=cursor.fetchone()
        return data

    def close(self,db):
        db.close()
        