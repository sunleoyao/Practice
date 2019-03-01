import sys

class file_format(object):
    def __init__(self,path,split_symbol='',need_split='Y'):
        self.path = path
        self.split_symbol = split_symbol
        self.need_split = need_split

    def read_file(self):
        try:
            f = open(self.path, 'r')
            result=f.readlines()
            f.close()
            return result
        except:
            print("Please check file path !")
            sys.exit(0)
        finally:
            if f:
                f.close()
        
    def file_split(self):
        unsplist_list=self.read_file()
        splist_result=[]
        if self.split_symbol=='':
            print ("Please input split_symbol !")
            sys.exit(0)
        else:
            for x in unsplist_list:
                splist=x.split(self.split_symbol)
                if self.need_split=='Y':
                    for i in range(len(splist)):
                        splist[i]=splist[i].strip()
                splist_result.append(splist)
            return splist_result