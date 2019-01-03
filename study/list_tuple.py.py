# -*- coding: utf-8 -*-
#list
num=[1,2,3,4,5]
print(num)
print(num[1])
print(num[-1])

num.append(6)
print(num)
num.insert(1,1.5)
print(num)
num.pop()
print(num)
num.pop(1)
print(num)

#tuple
name=('a','b','c','d')
print(name)
print(name[0])
print(name[-1])
name_test_change=('a','b',['c','d'],'e')
print(name_test_change[2])
print(name_test_change[2][1])
name_test_change[2][1]='hahaha'
print(name_test_change)