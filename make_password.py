# -*- coding: utf-8 -*-
import random

#产生1个随机数，个十百位数不同
def make_num():
    num=random.randint(1000, 9990)
    no1=num//1000
    no2=num//100%10
    no3=num//10%10
    no4=num%10
    if((no1==no2)|(no2==no3)|(no3==no4)|(no2==no4)|(no1==no3)):
        return make_num()
    else:
        return num

#按照要求产生x个随机数
def make_num_list(x_temp):
    list_temp=[]
    x=int(x_temp)
    for n in range(0,x):
        temp=make_num()
        list_temp.append(temp)
    return list_temp

#按照要求，做对应关系
def change_char(list_num):
    #key_value={'0':')','1':'!','2':'@','3':'#','4':'$','5':'%','6':'^','7':'&','8':'*','9':'('}
    key_value={0:')',1:'!',2:'@',3:'#',4:'$',5:'%',6:'^',7:'&',8:'*',9:'('}
    list_num_sort=list_num[:]
    list_num_sort.sort()
    small1=list_num.index(list_num_sort[0])
    small2=list_num.index(list_num_sort[1])
    list_num[small1]=key_value[list_num[small1]]
    list_num[small2]=key_value[list_num[small2]]
    return list_num

if __name__=='__main__':
    chars_num_str=input("Please input how many number do you want?\n")
    chars_num=int(chars_num_str)
    print(change_char(make_num_list(chars_num)))
