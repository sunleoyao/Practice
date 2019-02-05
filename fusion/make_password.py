# -*- coding: utf-8 -*-
import random
import math

how_many=6  #生产多少位的随机数
how_many_change=3 #按照从小到大的顺序有多少位需要做映射
log_path='C://Users//Administrator//Desktop//log//'  #日志路径，random.info为未处理随机数,change.info为映射后list

def open_file(filename,list1=[],list2=[]):
     filename=log_path+filename
     with open(filename,'w') as file_object:
         for x in range(len(list1)):
            file_object.write(list1[x]+' : '+list2[x])
            file_object.write('\n')

def fusion_list_to_str(input_list=[]):
    out_str=''
    for x in input_list:
        out_str=out_str+x
    return out_str

#产生1个how_many位随机数
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

#针对随机list排序，最小的how_many_change位数做映射
def change_char(list_num_input=[]):
    key_value={0:')',1:'!',2:'@',3:'#',4:'$',5:'%',6:'^',7:'&',8:'*',9:'('}
    list_sort=list_num_input[:]
    list_sort.sort()
    for i in range(how_many_change):
        temp=list_num_input.index(list_sort[i])
        list_num_input[temp]=key_value[int(list_sort[i])]
    return list_num_input

#按照要求产生x个随机数
def how_num_list(n):
    list_nosort=[]
    list_sort=[]
    for x in range(n):
        temp=make_num()
        list_nosort.append(fusion_list_to_str(temp))
        list_sort.append(fusion_list_to_str(change_char(temp)))
    return list_nosort,list_sort

if __name__=='__main__':
    chars_num_str=input("Please input how many number do you want?\n")
    chars_num=int(chars_num_str)
    list_nosort,list_sort=how_num_list(chars_num)
    open_file('result.log',list_nosort,list_sort)