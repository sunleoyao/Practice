# -*- coding: utf-8 -*-
###   dict   ###
#dict就是key-value存储
dict_test = {'a': 1, 'b': 2, 'c': 3}
print(dict_test['a'])
print(dict_test.get('a'))
print(dict_test.get('aa'))
print('aa' in dict_test)
###增
dict_test['d'] = 4
print(dict_test)
###改
dict_test['d'] = 666
print(dict_test)
###改增
dict_test_temp = {'dd': 888}
dict_test.update(dict_test_temp)
print(dict_test)
###删
dict_test.pop('dd')
print(dict_test)



###   set   ###
#set就是没有value的dict，由于key的唯一性，所以多用于去重
s=set([1,2,3,4,5,6])
print(s)
#增
s.add(1)
print(s)
s.add(7)
print(s)
s.remove(2)
print(s)
#交集并集
s1=set([1,2,3])
s2=set([2,3,4])
print(s1&s2)
print(s1|s2)
