# -*- coding utf08 -*-
dict_test = {'a': 1, 'b': 2, 'c': 3}
print(dict_test['a'])
print(dict_test.get('a'))
print(dict_test.get('aa'))
print('aa' in dict_test)

dict_test['d'] = 4
print(dict_test)

dict_test['d'] = 666
print(dict_test)

dict_test_temp = {'dd': 888}
dict_test.update(dict_test_temp)
print(dict_test)

dict_test.pop('dd')
print(dict_test)
