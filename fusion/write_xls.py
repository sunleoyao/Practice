from mysql import mysql


# calc_mysql=mysql('localhost','yao','yao','mysql')
# calc_mysql.close()

def read_file(path):
    try:
        f = open(path, 'r')
        result=f.readlines()
        return result
    except:
        print("Please check file path!")
    finally:
        if f:
            f.close()

def list_to_lists(list,split):
    for i in list:
        



read_file('D:\\OneDrive\\code\\result.txt')