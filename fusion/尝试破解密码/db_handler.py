import shelve
from models import models
from core.color import Colors
from multiprocessing import Lock


class Db_handler(object):
    HOST_MUTEX = Lock()
    GROUP_MUTEX = Lock()
    G2H_MUTEX = Lock()

    @staticmethod
    # 根据主机组名称,获取该主机组Obj
    def getGroupObjByGroupName(group_db, groupName):
        for key in group_db:
            if group_db[key].groupName == groupName:
                return group_db[key]
        return

    @staticmethod
    # 根据主机组Id,获取该主机组所有主机Obj列表
    def getHostObjListByGroupId(host_db, g2h_db, groupId):
        host_list = []
        for key in g2h_db:
            if g2h_db[key].groupId == groupId:
                host_list.append(host_db[g2h_db[key].hostId])
        return host_list

    # 检查主机表唯一性(host字段唯一)(判断一个host对象是否存在)
    @classmethod
    def check_unique_host(cls, host_db, host_obj):
        for key in host_db:
            if host_db[key] == host_obj:
                # print('存在host:%s'%host_db[key])
                return host_db[key]
        return

    # 检查主机组表唯一性(groupName字段唯一)(判断一个group对象是否存在)
    @classmethod
    def check_unique_group(cls, group_db, group_obj):
        for key in group_db:
            if group_db[key] == group_obj:
                # print('存在group:%s'%group_db[key])
                return group_db[key]
        return

    # 检查主机组-主机表唯一性(记录中存在重复的hostId和groupId)(判断一个group2Host对象是否存在)
    @classmethod
    def check_unique_g2h(cls, g2h_db, g2h_obj):
        for key in g2h_db:
            if g2h_db[key] == g2h_obj:
                # print('存在g2h:%s'%g2h_db[key])
                return g2h_db[key]
        return

    # update host table
    @classmethod
    def update_host(cls, host_db, host_obj):
        cls.HOST_MUTEX.acquire()
        return_host_obj = cls.check_unique_host(host_db, host_obj)
        if not return_host_obj:
            host_db[host_obj.hostId] = host_obj
            print(Colors('insert host table 1 row', bcolor='green'))
        else:
            host_obj.hostId = return_host_obj.hostId
            host_db[return_host_obj.hostId] = host_obj
            print(Colors('update host table 1 row', bcolor='cyan'))
        cls.HOST_MUTEX.release()

    # insert group table
    @classmethod
    def insert_group(cls, group_db, group_obj):
        result_code = False
        cls.GROUP_MUTEX.acquire()
        if not cls.check_unique_group(group_db, group_obj):
            group_db[group_obj.groupId] = group_obj
            result_code = True
            print(Colors('insert group table 1 row', bcolor='green'))
        cls.GROUP_MUTEX.release()
        return result_code

    # insert g2h table
    @classmethod
    def insert_g2h(cls, g2h_db, host_obj, group_obj):
        result_code = False
        cls.G2H_MUTEX.acquire()
        g2h_obj = models.Group2Host(host_obj.hostId, group_obj.groupId)
        if not cls.check_unique_g2h(g2h_db, g2h_obj):
            g2h_db[g2h_obj.g2hId] = g2h_obj
            result_code = True
            print(Colors('insert g2h table 1 row', bcolor='green'))
        cls.G2H_MUTEX.release()
        return result_code

    # delete g2h table
    @classmethod
    def delete_g2h(cls, g2h_db, host_obj, group_obj):
        result_code = False
        cls.G2H_MUTEX.acquire()
        for key in g2h_db:
            if g2h_db[key].hostId == host_obj.hostId and g2h_db[key].groupId == group_obj.groupId:
                g2h_db.pop(key)
                result_code = True
                print(Colors('delete g2h table 1 row', bcolor='yellow'))
        cls.G2H_MUTEX.release()
        return result_code

db_handler.py