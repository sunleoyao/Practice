# -*- coding: utf-8 -*-
import random
import math

how_many=6  #生产多少位的随机数
how_many_change=3 #按照从小到大的顺序有多少位需要做映射
log_path='C://Users//Administrator//Desktop//log//'  #日志路径，random.info为未处理随机数,change.info为映射后list

def write_file(filename,what_write=[]):
    filename=log_path+filename
    with open(filename,'w') as file_object:
        for temp in what_write:
            file_object.write(temp)
            file_object.write('\n')

#产生1个随机数，个十百位数不同
def make_num():
    num_list=[]
    num=random.randint((int(math.pow(10,how_many-1))), (int(math.pow(10,how_many)))-1)
    for temp in str(num):
        num_list.append(temp)
    for i in range(0,len(num_list)):
        for j in range(i+1,len(num_list)):
            if num_list[i]==num_list[j]:
                return make_num()
    return num_list

#按照要求产生x个随机数
def how_num_list(n):
    list_temp=[]
    for n in range(n):
        list_temp.append(change_char())
    return list_temp

#按照要求，针对一组list做对应关系
def change_char():
    list_num_input=make_num()
    key_value={0:')',1:'!',2:'@',3:'#',4:'$',5:'%',6:'^',7:'&',8:'*',9:'('}
    temp=''
    for i in list_num_input:
        temp=temp+i
    write_file('random.inf',temp)
    print(list_num_input)
    list_sort=list_num_input[:]
    list_sort.sort()
    for i in range(how_many_change):
        temp=list_num_input.index(list_sort[i])
        list_num_input[temp]=key_value[int(list_sort[i])]
    return list_num_input

if __name__=='__main__':
    chars_num_str=input("Please input how many number do you want?\n")
    chars_num=int(chars_num_str)
    print(how_num_list(chars_num))