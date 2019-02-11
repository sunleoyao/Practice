# -*- coding: utf-8 -*-
from lib import commons
from multiprocessing import Lock


class Host(object):
    MUTEX = Lock()

    def __init__(self, host, port, user, password):
        self.MUTEX.acquire()
        self.hostId = commons.create_id('host')
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.MUTEX.release()

    def __eq__(self, other):
        res = False
        if type(other) == type(self):
            if self.host == other.host:
                res = True
        return res

    def __str__(self):
        return 'hostId:%s host:%s' % (self.hostId, self.host)


class Group(object):
    MUTEX = Lock()

    def __init__(self, groupName):
        self.MUTEX.acquire()
        self.groupId = commons.create_id('group')
        self.groupName = groupName
        self.MUTEX.release()

    def __eq__(self, other):
        res = False
        if type(other) == type(self):
            if self.groupName == other.groupName:
                res = True
        return res

    def __str__(self):
        return 'groupId:%s group:%s' % (self.groupId, self.groupName)


class Group2Host(object):
    MUTEX = Lock()

    def __init__(self, hostId, groupId):
        self.MUTEX.acquire()
        self.g2hId = commons.create_id('group2Host')
        self.hostId = hostId
        self.groupId = groupId
        self.MUTEX.release()

    def __eq__(self, other):
        res = False
        if type(other) == type(self):
            if self.hostId == other.hostId and self.groupId == other.groupId:
                res = True
        return res

    def __str__(self):
        return 'g2hId:%s group2Host:%s' % (self.g2hId, (self.hostId, self.groupId),)
