# -*- coding utf08 -*-
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
